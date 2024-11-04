import json
import yaml
import shutil
import traceback
from copy import deepcopy
from pathlib import Path
from .text import current_time
from .fast_types import valid_path, is_string, is_array, is_list
from typing import Any, Literal, Optional, Union, Sequence, List, Tuple, Dict


def scan_dir(
    path: Path,
    pattern: str,
    expected_dir: Literal["file", "path", "any"] = "any",
) -> list[Path]:
    path = Path(path)
    if expected_dir == "file":
        fn_checker = lambda path: Path.is_file(path)
    else:
        fn_checker = lambda path: Path.is_dir(path)
    expected_dir
    return [x for x in Path(path).glob(pattern) if fn_checker(x)]


def get_folders(
    path: str | Path,
    pattern: str = "*",
    *args,
    **kwargs,
) -> list[Path] | list:
    if is_list(path):
        results = []
        paths = [x for x in path if valid_path(x, expected_dir="path")]
        if not paths:
            return []
        [
            results.extend(scan_dir(x, pattern=pattern, expected_dir="path"))
            for x in paths
        ]
        return list(sorted(results))
    if not valid_path(path, "path"):
        return []
    return scan_dir(path, pattern=pattern, expected_dir="path")


def _get_files_ext_set(extension: str):
    if extension.startswith("*."):
        return extension
    if extension.startswith("."):
        return "*" + extension
    return "*." + extension


def get_files(
    path: Union[List[Union[str, Path]], str, Path],
    extensions: str | list[str] | tuple[str, ...] | None = None,
    *args,
    **kwargs,
) -> list[Path] | list:
    results = []
    if is_list(path):
        paths = [Path(x) for x in path if valid_path(x, expected_dir="path")]
        if not paths:
            return results
        [results.extend(get_files(_path, extensions=extensions)) for _path in paths]
        return list(sorted(results))
    else:
        if not valid_path(path, expected_dir="path"):
            return results
        if is_array(extensions):
            [
                results.extend(
                    scan_dir(
                        path,
                        pattern=_get_files_ext_set(extension),
                        expected_dir="file",
                    )
                )
                for extension in extensions
            ]
        elif is_string(extensions):
            results.extend(
                scan_dir(
                    path,
                    pattern=_get_files_ext_set(extensions),
                    expected_dir="file",
                )
            )
        return list(sorted(results))


scan_files = get_files
"""Alias for get_files"""

scan_paths = get_folders
"""Alias for 'get_folders'"""


def path_to_string(path: Path):
    assert isinstance(path, (Path, str, bytes)), "Invalid path format"
    return str(Path(path)).replace("\\", "/")


def mkdir(
    *paths: Path | str,
):
    Path(*[x for x in paths if isinstance(x, (bytes, str, Path))]).mkdir(
        parents=True, exist_ok=True
    )


def create_path(
    *paths: Path | str,
):
    """alias for mkdir, temporary"""
    mkdir(*paths)


def set_path(
    *paths: str | Path,
    mkdir: bool = False,
    mkdir_parent: bool = True,
    return_string: bool = True,
):
    path = Path(*[x for x in paths if isinstance(x, (bytes, str, Path))])
    if mkdir:
        mkdir(path.parent if mkdir_parent else path)
    return str(path).replace("\\", "/") if return_string else path


def load_json(
    path: str | Path,
    default_value: Any | None = None,
    encoding: str = "utf-8",
    errors="ignore",
    *args,
    **kwargs,
) -> list | dict | None:
    """
    Load JSON/JSONL data from a file.

    Args:
        path (Union[str, Path]): The path to the JSON file.

    Returns:
        Union[list, dict, None]: The loaded JSON data as a list, dictionary, or None if any error occurs.
    """

    if not valid_path(path, expected_dir="file"):
        return default_value
    path = Path(path)
    file = path.read_text(encoding=encoding, errors=errors)
    if path.name.endswith(".jsonl"):
        results = []
        for line in file.splitlines():
            try:
                results.append(json.loads(line))
            except:
                pass
        return results
    try:
        return json.loads(file)
    except:
        return default_value


def save_json(
    path: str | Path,
    content: list | dict,
    encoding: str = "utf-8",
    indent: int = 4,
    errors="ignore",
    append: bool = False,
    *args,
    **kwargs,
) -> None:
    """
    Save JSON data to a file.

    Args:
        path (Union[str, Path]): The path to save the JSON file.
        content (Union[list, dict]): The content to be saved as JSON.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".
        indent (int, optional): The indentation level in the saved JSON file. Defaults to 4.
    """

    if not isinstance(path, (str, bytes, Path)):
        path = current_time() + ".json"
    path = Path(path)
    if not path.name.endswith((".json", ".jsonl")):
        path = Path(path.parent, f"{path.name}.json")
    mkdir(Path(path).parent)
    if path.name.endswith(".jsonl"):
        content = json.dumps(content)
        if append and path.exists():
            older_content = path.read_text(encoding=encoding, errors=errors)
            content = older_content.rstrip() + "\n" + content
    else:
        if append and path.exists():
            old_content = json.loads(path.read_text(encoding=encoding, errors=errors))
            if isinstance(old_content, dict) and isinstance(content, dict):
                old_content.update(content)
                content = deepcopy(old_content)
            elif isinstance(old_content, list):
                if isinstance(content, dict):
                    old_content.append(content)
                    content = deepcopy(old_content)
                elif isinstance(old_content, list):
                    old_content.extend(old_content)
                    content = deepcopy(old_content)
        content = json.dumps(content, indent=indent)
    path.write_text(content, encoding=encoding, errors=errors)


def load_text(
    path: Path | str,
    encoding: str = "utf-8",
    errors="ignore",
    default_value: Any = "",
    *args,
    **kwargs,
) -> str:
    """Load text content from a file. If not exists it returns a empty string."""
    if not valid_path(path):
        return default_value
    return Path(path).read_text(encoding, errors=errors)


def save_text(
    path: Path | str,
    content: str,
    encoding: str = "utf-8",
    append: bool = False,
    errors="ignore",
    *args,
    **kwargs,
) -> None:
    """Save a text file to the provided path."""
    path = Path(path)
    mkdir(Path(path).parent)
    text = content
    if append and valid_path(path, expected_dir="file"):
        text = load_text(path=path, encoding=encoding, errors=errors) + content
    path.write_text(text, encoding=encoding, errors=errors)


def load_yaml(
    path: Union[Path, str],
    unsafe_loader: bool = True,
    default_value: Any | None = None,
    *args,
    **kwargs,
) -> Optional[Union[List[Any], Dict[str, Any]]]:
    """
    Loads YAML content from a file.

    Args:
        path (Union[Path, str]): The path to the file.
        unsafe_loader (bool): If False, it will use the safe_load instead.
        default_value (Any | None): If something goes wrong, this value will be returned instead.

    Returns:
        Optional[Union[List[Any], Dict[str, Any]]]: The loaded YAML data.
    """
    if not valid_path(path, expected_dir="file"):
        return default_value
    loader = yaml.safe_load if not unsafe_loader else yaml.unsafe_load
    try:
        return loader(Path(path).read_bytes())
    except Exception as e:
        print(f"YAML load error: {e}")
        traceback.print_exc()
    return default_value


def save_yaml(
    path: Union[Path, str],
    content: Union[List[Any], Tuple[Any, Any], Dict[Any, Any]],
    encoding: str = "utf-8",
    safe_dump: bool = False,
    errors: str = "ignore",
    *args,
    **kwargs,
) -> None:
    """Saves a YAML file to the provided path.

    Args:
        path (Union[Path, str]): The path where the file will be saved.
        content (Union[List[Any], Tuple[Any, Any], Dict[Any, Any]]): The data that will be written into the file.
        encoding (str, optional): The encoding of the output. Default is 'utf-8'. Defaults to "utf-8".
        safe_dump (bool, optional): If True, it uses the safe_dump method instead. Defaults to False.
    """
    mkdir(Path(path).parent)
    save_func = yaml.safe_dump if safe_dump else yaml.dump
    try:
        with open(path, "w", encoding=encoding, errors=errors) as file:
            save_func(data=content, stream=file, encoding=encoding)
    except Exception as e:
        print(f"An exception occurred while saving {path}. Exception: {e}")
        traceback.print_exc()


def move_to(
    source_path: Union[str, Path],
    destination_path: Union[str, Path],
    *args,
    **kwargs,
):
    """
    Moves a file or directory from one location to another.

    Args:
        source_path (Union[str, Path]): The path of the file/directory to be moved.
        destination_path (Union[str, Path]): The new location for the file/directory.

    Raises:
        AssertionError: If the source path does not exist or is invalid
    """
    assert (
        str(source_path).strip() and Path(source_path).exists()
    ), "Source path does not exists!"
    source_path = Path(source_path)
    assert valid_path(source_path), "Source path does not exists!"
    destination_path = Path(destination_path)
    mkdir(destination_path)
    try:
        shutil.move(source_path, destination_path)
    except Exception as e:
        print(f"Failed to move the destination path! {e}")
        traceback.print_exc()


def delete_path(
    files: str | Path | tuple[str | Path, ...],
    verbose=False,
    *args,
    **kwargs,
):
    if is_string(files) and Path(files).exists():
        try:
            shutil.rmtree(files)
            if verbose:
                print("'{files}' deleted")
        except Exception as e:
            if verbose:
                print(f"Failed to delete {files}, Exception: {e}")
                traceback.print_exc()
    elif is_array(files):
        [delete_path(path) for path in files if is_string(path) or is_array(path)]


__all__ = [
    "get_folders",
    "get_files",
    "mkdir",
    "create_path",
    "load_json",
    "save_json",
    "load_text",
    "save_text",
    "load_yaml",
    "save_yaml",
    "move_to",
    "delete_path",
    "set_path",
    "scan_dir",
    "scan_files",
    "scan_paths",
]
