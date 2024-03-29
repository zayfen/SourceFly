import os
from typing import List
from pathlib import Path
from sourcefly.filetree.mod import split_path
from sourcefly.common.logger import zlogger
from shutil import copyfile
from sourcefly.common.fs_ops import create_file


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

    if len(files) == 1:
        return str(files[0].parent.resolve())

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


def target_path_of_files(files: List[Path], target_dir: Path) -> List[Path]:
    """
    Assume target_dir is existed directory
    Assume PUBLIC_PATH is public_path_of_files(files),
    target file is target_dir join {PUBLIC_PATH}
    """
    public_path = public_path_of_files(files)

    target_abs_dir = target_dir.absolute()

    zlogger.debug(target_abs_dir)

    len_public_path = len(public_path)

    files_prune_public_path = list(
        map(lambda f: str(f.absolute())[len_public_path:], files)
    )

    zlogger.debug(files_prune_public_path)

    target_file_paths = []
    zlogger.debug("skdfk")
    zlogger.debug(len(files_prune_public_path))

    zlogger.debug(target_dir)

    for p in files_prune_public_path:
        target_file_paths.append(Path(str(target_dir) + p).absolute())

    zlogger.debug(target_file_paths)

    return target_file_paths


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
    public_path = public_path_of_files(files)
    len_of_public_path = len(public_path)

    for p in files:
        # +1 ignore /
        tail_path = str(p.resolve())[(len_of_public_path + 1) :]

        zlogger.debug("target_dir is {}".format(target_dir.resolve()))
        zlogger.debug("tail_path is {}".format(tail_path))

        dst_path = target_dir.resolve().joinpath(tail_path)

        zlogger.debug("from {p} to {new_path}".format(p=p, new_path=dst_path))

        create_file(dst_path)
        copyfile(p, dst_path)
