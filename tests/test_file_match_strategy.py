from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy


def test_cpp():
    cfms = CppFileMatchStrategy()
    matches = cfms.possible_matches("header.abc.h")
    assert matches != None and matches[0] == "header.abc.h"
    assert matches != None and matches[1] == "header.abc.cpp"

    matches = cfms.possible_matches("iostream")
    assert matches != None and matches[0] == "iostream"

    matches = cfms.possible_matches("")
    assert matches is None
