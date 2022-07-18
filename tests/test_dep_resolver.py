#!/usr/bin/env python3

from pathlib import Path
from sourcefly.dep_resolver.cpp_dep_resolver import CppDepResolver
from sourcefly.filetree.mod import FileTree
from sourcefly.common.logger import zlogger


def test_dep_resolver():
    cpp_entry = "/home/zayfen/github.com/SourceFly/tests/cpp/main.cpp"
    cpp_entry_file = Path(
        cpp_entry
        # "/home/zayfen/github.com/SourceFly/tests/main.cpp"
    )

    filetree = FileTree("**/*")
    filetree.build_file_tree(Path("tests/cpp"))

    cdr = CppDepResolver(filetree)
    cdr.set_entry(cpp_entry_file)
    file_deps = cdr.deps_tree()

    zlogger.debug(file_deps)

    if file_deps is not None:
        assert file_deps.file == Path(cpp_entry)
        assert len(file_deps.deps) == 3
    else:
        assert False, "file_deps shouldn't be None"
