import re
import nltk
import math
import random
import difflib
import textwrap
import pyperclip
import markdown2
import subprocess
from copy import deepcopy
from .fast_types import *
from datetime import datetime
from textblob import TextBlob, Word
from collections import Counter
from nltk.tag import PerceptronTagger
from nltk.stem import WordNetLemmatizer
from markdownify import markdownify as md
from string import whitespace, punctuation
from textblob.exceptions import MissingCorpusError
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Union, Tuple, AnyStr, Literal, Sequence, Any
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from .backbones.texts.txt_requoter import requoter
from .backbones.texts.txt_splitter import ProcessSplit

TLSTRINGS = list(whitespace) + list(punctuation)


class NLTKInitCheck:
    """To not use the global variables here, we will use this to check if the nltk was initialized when a function that requires it is called"""

    def __init__(self):
        self.is_initialized = False


nltk_inst = NLTKInitCheck()

_WT_REPLACERS = {
    "``": '"',
    "`": '"',
}


def _run_nltk_downloader():
    if nltk_inst.is_initialized:
        return
    for _nllib in [
        "stopwords",
        "wordnet",
        "cmudict",
        "punkt",
        "punkt_tab",
        "averaged_perceptron_tagger",
        "maxent_ne_chunker",
        "words",
        "maxent_ne_chunker_tab",
    ]:
        nltk.download(_nllib, quiet=True)
    nltk_inst.is_initialized = True


def tokenize_text(
    text: str,
    by: Literal["word", "sentence"] = "word",
    language: str = "english",
    preserve_line: bool = False,
) -> List[str]:
    """Tokenize text by words or sentences.

    Args:
        text (str): The input text to tokenize.
        by (Literal["word", "sentence"], optional): The level of tokenization ("word" or "sentence"). Defaults to "word".

    Returns:
        List[str]: A list of tokens based on the specified level.
    """
    assert by in ["word", "sentence"], "Invalid tokenization type"
    _run_nltk_downloader()
    if by == "word":
        return [
            recursive_replacer(x, _WT_REPLACERS)
            for x in nltk.word_tokenize(
                text,
                language=language,
                preserve_line=preserve_line,
            )
        ]
    return nltk.sent_tokenize(text, language=language)


def text_entropy(text: str) -> float:
    """Calculate the entropy of a text to gauge its randomness.

    Args:
        text (str): The input text whose entropy is to be calculated.

    Returns:
        float: The entropy value of the text, indicating its level of randomness.
    """
    text = text.lower()
    counter = Counter(text)
    total_count = len(text)
    return -sum(
        (count / total_count) * math.log2(count / total_count)
        for count in counter.values()
    )


def scramble_text(text: str) -> str:
    """Randomly shuffle the words in a text.

    Args:
        text (str): The input text to be scrambled.

    Returns:
        str: The text with its words randomly shuffled.
    """
    words = text.split()
    random.shuffle(words)
    return " ".join(words)


def compare_texts(text1: str, text2: str) -> List[str]:
    """Compare two texts and highlight the differences.

    Args:
        text1 (str): The first text to compare.
        text2 (str): The second text to compare.

    Returns:
        List[str]: A list of lines that differ between the two texts, prefixed with '- ' for deletions and '+ ' for additions.
    """
    differ = difflib.Differ()
    result = list(differ.compare(text1.splitlines(), text2.splitlines()))
    return [line for line in result if line.startswith("- ") or line.startswith("+ ")]


def stem_text(
    text: str,
    language: str = "english",
) -> str:
    """Reduce words in the text to their stem or root form.

    Args:
        text (str): The input text to be stemmed.

    Returns:
        str: The text with words reduced to their stems.
    """

    tokens = tokenize_text(
        text,
        by="word",
        language=language,
        preserve_line=False,
    )
    stemmer = nltk.PorterStemmer()

    return " ".join([stemmer.stem(token) for token in tokens])


def lemmatize_text(
    text: str,
) -> str:
    """Reduce words in the text to their base or dictionary form.

    Args:
        text (str): The input text to be lemmatized.

    Returns:
        str: The text with words reduced to their base forms.
    """
    return " ".join(
        [
            word.lemmatize()
            for word in TextBlob(text=text).words
            if isinstance(word, Word)
        ]
    )


def generate_ngrams(
    inputs: str | Sequence[Any],
    n: int,
    text_language: str = "english",
    split_text_by: Literal["word", "sentence"] = "word",
    split_ngram_text_by: Literal["char", "full"] = "char",
) -> List[Any]:
    """Generate n-grams (sequences of n items) from the text.

    Args:
        inputs (str | Sequence[Any]): The input text or a list of components from which to
                generate n-grams.
        n (int): The number of items in each n-gram.
        text_language (str, optional): Used only when the input is a string.
                It will be used to split the words/sentences properly.
        split_text_by (Literal["word", "sentence"], optional): Used only when the input is a string.
                If set to words the split will be word by word, otherwise will be the sentence.
        split_ngram_text_by (Literal["char", "full"], optional):  Used only when the input is a string.
                If set to 'char' it will split char by char, otherwise will do the n-grams for the entire
                words or sentences.
    Returns:
        List[Any]: A list of n-grams generated from the inputs.
    """
    if is_array(inputs, True):
        return [x for x in nltk.ngrams(inputs, n)]
    elif is_string(inputs, False, True):
        assert split_ngram_text_by in [
            "char",
            "full",
        ], f'Invalid option for "split_ngram_text_by": {split_ngram_text_by}, it must be either "char" or "full"'
        tokens = tokenize_text(
            inputs,
            by=split_text_by,
            language=text_language,
            preserve_line=False,
        )

        if split_ngram_text_by == "char":
            return [[x for x in nltk.ngrams(word, n)] for word in tokens]
        return [x for x in nltk.ngrams(tokens, n)]


def text_similarity(text1: str, text2: str) -> float:
    """Compute similarity between two texts using cosine similarity.

    Args:
        text1 (str): The first text for comparison.
        text2 (str): The second text for comparison.

    Returns:
        float: The cosine similarity score between the two texts.
    """
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]


def extract_named_entities(
    text: str,
    language: str = "english",
) -> List[str]:
    """Extract named entities from the text.

    Args:
        text (str): The input text from which to extract named entities.

    Returns:
        List[str]: A list of named entities found in the text.
    """
    _run_nltk_downloader()
    tokens = tokenize_text(
        text,
        by="word",
        language=language,
        preserve_line=False,
    )
    tagged = nltk.pos_tag(tokens)
    chunked = nltk.ne_chunk(tagged)
    return list(
        set([chunk.label() for chunk in chunked if isinstance(chunk, nltk.Tree)])
    )


def text_chunker(text: str, delimiter: str) -> List[str]:
    """Chunk text into parts based on a delimiter.

    Args:
        text (str): The input text to be chunked.
        delimiter (str): The delimiter to use for splitting the text.

    Returns:
        List[str]: A list of text chunks.
    """
    return text.split(delimiter)


def find_repeated_words(text: str, language: str = "english") -> Dict[str, int]:
    """Find and count repeated words in a text.

    Args:
        text (str): The input text to search for repeated words.

    Returns:
        Dict[str, int]: A dictionary where keys are repeated words and values are their counts.
    """

    words = [
        tokenize_text(
            text.lower(),
            by="word",
            language=language,
            preserve_line=False,
        )
    ]
    return dict(Counter(word for word in words if words.count(word) > 1))


def split_by_paragraph(text: str) -> List[str]:
    """Split text into paragraphs.

    Args:
        text (str): The input text to split.

    Returns:
        List[str]: A list of paragraphs from the text.
    """
    text = text.replace("\n\n\n", "\n\n")
    return text.split("\n\n")


def remove_stop_words(
    text: str,
    language: str = "english",
    preserve_line: bool = True,
) -> str:
    """Remove common stop words from a text.

    Args:
        text (str): The input text to process.

    Returns:
        str: The text with stop words removed.
    """
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = tokenize_text(
        text,
        by="word",
        language=language,
        preserve_line=preserve_line,
    )
    return " ".join([word for word in tokens if word.lower() not in stop_words])


def normalize_text(text: str) -> str:
    """Convert text to lowercase and remove extra whitespace.

    Args:
        text (str): The input text to normalize.

    Returns:
        str: The normalized text.
    """
    return " ".join(text.lower().split())


def remove_non_alphanumeric(text: str) -> str:
    """Remove non-alphanumeric characters from a text.

    Args:
        text (str): The input text to clean.

    Returns:
        str: The text with non-alphanumeric characters removed.
    """
    return re.sub(r"[^a-zA-Z0-9\s\n]", "", text)


def extract_hashtags(text: str) -> list[str]:
    """Extract hashtags from a text.

    Args:
        text (str): The input text from which to extract hashtags.

    Returns:
        list[str]: A list of hashtags found in the text.
    """
    return re.findall(r"#\w+", text)


def extract_mentions(text: str) -> list[str]:
    """Extract mentions (e.g., @user) from a text.

    Args:
        text (str): The input text from which to extract mentions.

    Returns:
        list[str]: A list of mentions found in the text.
    """
    return re.findall(r"@\w+", text)


def count_sentences(text: str) -> int:
    """Count the number of sentences in a text.

    Args:
        text (str): The input text to analyze.

    Returns:
        int: The number of sentences in the text.
    """
    split_text = blob_split(text)
    return len(split_text)


def extract_keywords(text_list: list[str] | str, top_n: int = 5) -> List[str]:
    """Extract keywords from a text based on their importance.

    Args:
        text_list (list[str] | str): A list of texts or a single text to extract keywords from.
        top_n (int, optional): The number of top keywords to return. Defaults to 5.

    Returns:
        List[str]: A list of the top keywords.

    Exceptions:
        ValueError: Raised when there is an empty vocabulary (e.g., from an empty or too short input text).
    """
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
    if isinstance(text_list, str):
        text_list = [text_list]
    try:
        tfidf_matrix = vectorizer.fit_transform(text_list)
    except ValueError:
        return []  # happens with empty vocabulary, so returns empty
    return vectorizer.get_feature_names_out()


def text_formatter(text: str, width: int) -> str:
    """Format text to fit a certain width.

    Args:
        text (str): The input text to format.
        width (int): The maximum width of each line in the formatted text.

    Returns:
        str: The formatted text.
    """
    return textwrap.fill(text, width)


def count_words(text: str, language: str = "english") -> int:
    """Count the number of words in a text.

    Args:
        text (str): The input text to analyze.

    Returns:
        int: The total word count in the text.
    """
    tokenized_text = tokenize_text(
        text, by="word", language=language, preserve_line=False
    )
    return len(tokenized_text)


def extract_keys(string: str) -> list | list[str]:
    # Use a regular expression to find all occurrences of {key} in the string
    keys = re.findall(r"\{(\w+)\}", string)
    return keys


def current_time():
    """
    Returns the current date and time in a 'YYYY-MM-DD-HHMMSS' format.

    Returns:
        str: The current date and time.
    """
    return f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"


def recursive_replacer(text: str, dic: dict[str, str]) -> str:
    """
    Recursively replaces all keys of the dictionary with their corresponding values within a given string.

    Args:
        text (str): The original text.
        replacements (Dict[str, str]): A dictionary where keys are what to replace and values is what they will be replaced by

    Returns:
        str: The final modified text
    """
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def clipboard(text: str):
    """
    Set the clipboard to the given text.
    """
    pyperclip.copy(text)


def unescape(entry: Union[str, bytes]) -> str:
    """
    Unescapes the given string by encoding it to bytes and then decoding with 'unicode-escape' errors ignored.

    Args:
        entry (str, bytes): The input string.

    Raises:
        Assertion: If entry is not a valid string or bytes.

    Returns:
        str: The unescaped string.

    Example:

        ```python

        results = unescape("This is the first line.\\\\n\\\\nThis is the last line!")
        # results = "This is the first line.\\n\\nThis is the last line!"

        ```
    """
    assert isinstance(
        entry, (str, bytes)
    ), "The input should be a valid string or bytes."
    if isinstance(entry, bytes):
        return entry.decode(encoding="unicode-escape", errors="ignore")
    return entry.encode(encoding="utf-8", errors="ignore").decode(
        encoding="unicode-escape", errors="ignore"
    )


def escape(entry: Union[str, bytes]) -> str:
    """
    Escapes the given string by encoding it to bytes then converting it to string directly, finally removing the "b'" and "'" from the results.

    Args:
        entry (str, bytes): The input string.

    Raises:
        Assertion: If entry is not a valid string or bytes.

    Returns:
        str: The escaped entry.

    Example:

        ```python

        results = escape("This is the first line.\\n\\nThis is the last line!")
        # results = "This is the first line.\\\\n\\\\nThis is the last line!"

        ```
    """
    assert isinstance(
        entry, (str, bytes)
    ), "The input should be a valid string or bytes."
    if isinstance(entry, str):
        entry = entry.encode(encoding="utf-8", errors="ignore")

    entry = str(entry)
    if entry.startswith(("b'", 'b"')):
        return entry[2:-1]
    return entry


def keys_in_text(
    sources: str,
    has_any: str | list[str],
    force_lower_case: bool = False,
):
    """Basically the reverse of **in** function, it can be used to locate if **sources** contains anything from the **has_any** into it.

    Args:
        sources (str):
            Target string to be checked if has any of the provided keys.
        has_any (str | list[str]):
            The string or list of strings to be checked if they are or not in the text.
            If its a string each letter will be checked, if its a list of string, then each word in the list will be checked instead.
        force_lower_case (bool, optional):
            If true will set everything to lower-case (both source and has_any).
            This is useful for tasks that dont require a case-sensitive scan. Defaults to False.

    Returns:
        bool: If any key was found will be returned as true, otherwise False.
    """
    if not is_string(sources, False) or not isinstance(has_any, (str, Sequence)):
        return False

    if is_array(has_any):
        has_any = [
            x.lower() if force_lower_case else x for x in has_any if is_string(x, False)
        ]
        if not has_any:
            return False

    if force_lower_case:
        sources = sources.lower()
        if is_string(has_any):
            has_any = has_any.lower()  # type: ignore

    for elem in has_any:
        if elem in sources:
            return True
    return False


def blob_split(text: str) -> List[str]:
    """
    Splits the input text into sentences using TextBlob.

    Args:
        text (str): The input text to split.

    Returns:
        list[str]: A list of the detected sentences in the provided text.
    """
    try:
        return [x for x in TextBlob(text).raw_sentences]
    except MissingCorpusError:
        subprocess.run(
            f"python -m textblob.download_corpora",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        return [x for x in TextBlob(text).raw_sentences]


def max_rfinder(txt: str, items_to_find: Union[List[str], Tuple[str, ...]]):
    """
    Finds the last occurrence of any item in a list or tuple within a string.

    Args:
        txt (str): The input string.
        items_to_find (Union[list[str], tuple[str]]): A list or tuple containing strings to find in 'txt'.

    Returns:
        int: The index of the last found item, -1 if no item is found.
    """
    highest_results = -1
    for item in items_to_find:
        current = txt.rfind(item)
        if current > highest_results:
            highest_results = current
    return highest_results


def check_next_string(
    text: str,
    current_id: int,
    text_to_match: str | list[str] | None = None,
    is_out_of_index_valid: bool = False,
):
    """
    Checks if the next character in a string matches one or more possibilities.

    Args:
        text (str): The input string.
        current_id (int): The index of the current character within the string.
        text_to_match (Union[str, list[str], None]): A single character to match or a list/tuple of characters.
                        If not provided and is_out_of_index_valid will be used as a result. Defaults to None.
        is_out_of_index_valid (bool): Whether returning True when the index is out of bounds should be valid. Defaults to False.

    Returns:
        bool: True, if any condition is met; False otherwise.
    """
    try:
        if is_array(text_to_match):
            return text[current_id + 1] in text_to_match
        return text[current_id + 1] == text_to_match
    except IndexError:
        return is_out_of_index_valid


def check_previous_string(
    text: str,
    current_id: int,
    text_to_match: str | list[str] | None = None,
    is_out_of_index_valid: bool = False,
):
    """
    Checks if the previous character in a string matches one or more possibilities.

    Args:
        text (str): The input string.
        current_id (int): The index of the current character within the string.
        text_to_match (Union[str, list[str], None]): A single character to match or a list/tuple of characters.
                        If not provided and is_out_of_index_valid will be used as a result. Defaults to None.
        is_out_of_index_valid (bool): Whether returning True when the index is out of bounds should be valid. Defaults to False.

    Returns:
        bool: True, if any condition is met; False otherwise.
    """

    try:
        if is_array(text_to_match):
            return text[current_id - 1] in text_to_match
        return text[current_id - 1] == text_to_match
    except IndexError:
        return is_out_of_index_valid


def trimincompletesentence(txt: str) -> str:
    """
    Tries to trim an incomplete sentence to the nearest complete one. If it fails returns the original sentence back.

    Args:
        txt (str): The original string containing sentences.
            If not complete, it will be trimmed to end with a valid punctuation mark.

    Returns:
        str: The finalized string.

    Example:

        >>> trimincompletesentence("Hello World! How are you doing?")
        "Hello World!"

        >>> trimincompletesentence("I like programming.")
        "I like programming." # Returns the sentence as it was.
        >>> trimincompletesentence("Hello there. This sentence is incomplete")
        "Hello there." # Returns the latest complete sequence.
        >>> trimincompletesentence("Hello there This sentence is incomplete")
        "Hello there This sentence is incomplete" # Returns the entire sentence if no cutting point was found.
    """
    possible_ends = (".", "?", "!", '."', '?"', '!"')
    txt = str(txt).rstrip()
    lastpunc = max_rfinder(txt, possible_ends)
    ln = len(txt)
    lastpunc = max(txt.rfind("."), txt.rfind("!"), txt.rfind("?"))
    if lastpunc < ln - 1:
        if txt[lastpunc + 1] == '"':
            lastpunc = lastpunc + 1
    if lastpunc >= 0:
        txt = txt[: lastpunc + 1]
    return txt


def simplify_quotes(txt: str) -> str:
    """
    Replaces special characters with standard single or double quotes.

    Args:
        txt (str): The input string containing special quote characters.

    Returns:
        str: The simplified string without the special quote characters.
    """
    assert is_string(txt, True), f"The input '{txt}' is not a valid string"
    return requoter(txt, True)


def clear_empty(text: str, clear_empty_lines: bool = True) -> str:
    """
    Clear empty lines (optional) and empty spaces on a given text.
    """
    return "\n".join(
        [
            re.sub(r"\s+", " ", x.strip())
            for x in text.splitlines()
            if not clear_empty_lines or x.strip()
        ]
    )


def txtsplit(
    text: str,
    desired_length=100,
    max_length=200,
    simplify_quote: bool = False,
) -> list[str]:
    text = clear_empty(text, True)
    if simplify_quote:
        text = simplify_quotes(text)
    processor = ProcessSplit(text, desired_length, max_length)
    return processor.run()


# .,!?;&$#@*(){}[]-_=+-/\:/%§'"``´´~^ºªAz09\t\n
def remove_special_characters(text: str) -> str:
    """
    Remove special characters from the given text using regular expressions.
    This version will keep alphanumeric characters, spaces, and common punctuations.
    """
    pattern = r"[^a-zA-Z0-9\s.,!?;']"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def html_to_markdown(html: AnyStr) -> str:
    """
    Converts HTML content to Markdown format.

    Args:
        html (str): The HTML string that needs to be converted.
                    Example - "<h1>Hello, World!</h1>"

    Returns:
        str: The corresponding markdown version of the inputted HTML
             Example - "# Hello, World!"
    """
    return md(html)


def markdown_to_html(markdown: AnyStr) -> str:
    """
    Converts Markdown text to HTML.

    Args:
        markdown (Union[str, bytes]): The input Markdown text. Can be either a string or bytes object.

    Returns:
        str: The converted HTML.
    """
    return markdown2.markdown(markdown)


def replace_pos_tags(
    text: str,
    target_pos_tags: List[str],
    replacer: str,
    language: str = "english",
    preserve_line: bool = True,
) -> str:
    """
    Replace words in `text` that match specific POS tags with `replacer`.

    Args:
        text (str): The input text containing words.
        target_pos_tags (List[str]): List of POS tags to replace.
        replacer (str): The string to replace the words with.

    Returns:
        str: The modified text with the specified words replaced.
    """
    # Remove f-strings to avoid conflicts
    filtered_text = text.replace("{}", "")

    all_fstrings = extract_keys(text)
    if all_fstrings:
        filtered_text = recursive_replacer(
            filtered_text, {key: "" for key in all_fstrings}
        )

    # Tokenize and tag parts of speech
    tokens = tokenize_text(
        filtered_text,
        by="word",
        language=language,
        preserve_line=preserve_line,
    )
    tagged_tokens = PerceptronTagger().tag(tokens)

    # Replace words based on POS tags
    replacers = {
        f"{start_txt}{word}{end_txt}": f"{start_txt}{replacer}{end_txt}"
        for word, pos in tagged_tokens
        if pos in target_pos_tags
        for start_txt in TLSTRINGS
        for end_txt in TLSTRINGS
    }

    return recursive_replacer(text, replacers) if replacers else text


__all__ = [
    "current_time",
    "max_rfinder",
    "check_next_string",
    "keys_in_text",
    "check_previous_string",
    "recursive_replacer",
    "clipboard",
    "unescape",
    "escape",
    "blob_split",
    "trimincompletesentence",
    "clear_empty",
    "txtsplit",
    "html_to_markdown",
    "remove_special_characters",
    "markdown_to_html",
    "replace_pos_tags",
    "extract_keywords",
    "generate_ngrams",
    "simplify_quotes",
    "find_repeated_words",
    "extract_mentions",
    "text_chunker",
    "extract_hashtags",
    "tokenize_text",
    "remove_non_alphanumeric",
    "remove_stop_words",
    "normalize_text",
    "extract_named_entities",
    "text_entropy",
    "stem_text",
    "scramble_text",
    "compare_texts",
    "split_by_paragraph",
    "text_similarity",
    "text_formatter",
    "count_words",
    "count_sentences",
    "extract_keys",
    "lemmatize_text",
    "requoter",
]
