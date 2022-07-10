from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy


def test_cpp():
    cfms = CppFileMatchStrategy()
    matches = cfms.possible_matches("header.abc.h")
    assert matches[0] == "header.abc.h"
    assert matches[1] == "header.abc.cpp"
