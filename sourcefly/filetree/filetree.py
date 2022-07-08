#!/usr/bin/env python3

# coding: utf-8

from pathlib import Path
from typing import AnyStr


def list_dir(dir: AnyStr):
    """
    list all files in directory, including files in subdirectories
    @params dir {string} - target directory
    @returns list<string>
    """
    pass


def find_file_by_tailpart(tailpart: AnyStr, match_strategy: FileMatchStrategy):
    """
    find file by tail part, e.g.: tail: dir/abc.txt, files: [dir/dir/abc.txt, dir/abc.txt, def.txt]

    @params tailpart { string }
    @params startage
    @returns: full path of file or None
    """
    pass
