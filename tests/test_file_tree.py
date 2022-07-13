#!/usr/bin/env python3

from pathlib import Path
from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy
from sourcefly.filetree.mod import (
    FileTree,
    TreeNode,
    find_files_by_tailpart,
    list_files,
    split_path,
)
from sourcefly.common.logger import zlogger


def test_list_files():
    path_list = list_files(Path("./tests/cpp/"))
    print(path_list)
    assert len(path_list) == 6


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
    filetree = FileTree("**/*", CppFileMatchStrategy())

    tree = filetree.build_file_tree(Path("tests/cpp/"))

    zlogger.debug(tree)

    assert tree is not None


def test_insert_path_to_tree_node():
    paths = split_path(Path("tests/cpp"))
    root_p = paths[0]
    root_node = TreeNode(root_p, None)

    FileTree.insert_path_to_tree_node(root_node, paths[1:])
