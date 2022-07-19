import os
from typing import List
from pathlib import Path
from sourcefly.filetree.mod import split_path
from sourcefly.common.logger import zlogger


def same_path_root(splited_files: List[List[str]]) -> bool:
    files_len = len(splited_files)

    for i in range(files_len - 1):
        f = [p for sublist in splited_files[i : i + 1] for p in sublist]
        next_f = [p for sublist in splited_files[(i + 1) : (i + 2)] for p in sublist]

        f_root = f[0:1]
        next_f_root = next_f[0:1]

        zlogger.debug(
            "f_root: {f_root};  next_f_root: {next_f_root}".format(
                f_root=f_root, next_f_root=next_f_root
            )
        )

        if not (f_root and next_f_root):
            return False

        if f_root != next_f_root:
            return False

    return True


def public_path_of_files(files: List[Path]) -> str:
    if not files:
        return ""

    splited_files = list(map(lambda file: split_path(file), files))
    zlogger.debug(splited_files)

    root_idx = 0
    while same_path_root(
        list(map(lambda splited_file: splited_file[root_idx:], splited_files))
    ):
        root_idx = root_idx + 1

    l = splited_files[0][0:root_idx]
    zlogger.debug(
        "{files}[{root_idx}] is {l}", files=splited_files[0], root_idx=root_idx, l=l
    )
    return "/" + os.path.sep.join(l)


def migrate(files: List[Path], target_dir: Path):
    """to migrate files to target directory
    we will remove public prefix of files.

    Args:
        files List[Path]:
        target_dir Path:
    Returns:
        None

    Example:

    """
    pass
