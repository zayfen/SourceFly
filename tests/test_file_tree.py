#!/usr/bin/env python3


from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy
from sourcefly.filetree.mod import find_files_by_tailpart, list_files


def test_list_files():
    path_list = list_files("./tests/")
    print(path_list)
    assert len(path_list) == 6


def test_find_files_by_tailpart():
    path_list = list_files("./tests/")
    strategy = CppFileMatchStrategy()

    files = find_files_by_tailpart(path_list, "test_file_tree.py", strategy)
    print("test_find_files_by_tailpart: ", files)

    assert str(files[0].absolute()).endswith("tests/test_file_tree.py")
