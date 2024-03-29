#!/usr/bin/env python3

from pathlib import Path
from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy
from sourcefly.filetree.mod import (
    FileTree,
    find_files_by_tailpart,
    list_files,
    split_path,
)
from sourcefly.common.logger import zlogger


def test_list_files():
    path_list = list_files(Path("./tests/cpp/"))
    assert len(path_list) == 7


def test_find_files_by_tailpart():
    path_list = list_files(Path("./tests/cpp/"))
    strategy = CppFileMatchStrategy()

    zlogger.debug(path_list)

    files = find_files_by_tailpart(path_list, "helper.h", strategy)

    # now files is helper.h helper.cpp
    # print("test_find_files_by_tailpart: ", files)
    zlogger.debug(files)

    assert Path("./tests/cpp/helper.h") in files
    assert Path("./tests/cpp/helper.cpp") in files


def test_split_path():
    paths = split_path(Path("./tests/cpp//helper.h"))
    assert paths[-3:] == ["tests", "cpp", "helper.h"]


def test_filetree():
    filetree = FileTree("**/*")

    tree = filetree.build_file_tree(Path("tests/cpp/"))

    zlogger.debug(tree)

    assert tree is not None

    assert tree.value == ""

    assert len(tree.children.values()) == 1

    l = tree.children.values()

    assert len(l) == 1

    files = filetree.try_find_file("helper.h")
    zlogger.debug(files)
    assert len(files) == 2
