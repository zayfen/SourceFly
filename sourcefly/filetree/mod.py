# coding: utf-8

from pathlib import Path
from typing import Any, List, Text
from sourcefly.filetree.file_match_strategy import FileMatchStrategy


def some(fn, iterable):
    for item in iterable:
        if fn(item):
            return True
    return False


def list_files(dir: str) -> list[Path]:
    """
    list all files in directory, including files in subdirectories
    @params dir {string} - target directory
    @returns list<string>
    """
    p = Path(dir)
    paths_iter = p.glob("**/*")
    paths_iter = filter(lambda file: file.is_file(), paths_iter)
    # files = map(lambda file: str(file), files)
    return list(paths_iter)


def find_files_by_tailpart(
    path_list: List[Path], tailpart: str, match_strategy: FileMatchStrategy
) -> list[Path]:
    """
    find file by tail part, e.g.: tail: dir/abc.txt, files: [dir/dir/abc.txt, dir/abc.txt, def.txt]

    @params tailpart { string }
    @params startage
    @returns: full path of file or None
    """
    matches = match_strategy.possible_matches(tailpart)
    matched_files = filter(
        lambda path: some(lambda match_file: path.match(match_file), matches),
        path_list,
    )

    return list(matched_files)


class FileTree:
    def __init__(self, dir: Text):
        pass
