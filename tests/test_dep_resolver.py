#!/usr/bin/env python3

from pathlib import Path
from sourcefly.dep_resolver.cpp_dep_resolver import CppDepResolver


def test_dep_resolver():
    cpp_entry_file = Path(
        # "/home/zhangyunfeng@pudu.com/github.com/SourceFly/tests/main.cpp"
        "/home/zayfen/github.com/SourceFly/tests/main.cpp"
    )
    cdr = CppDepResolver(cpp_entry_file)
    file_deps = cdr.deps_tree()

    print("file_deps.file: ", file_deps.file if file_deps is not None else "None")
    print(
        "file-deps.depends: ",
        len(file_deps.deps if file_deps is not None else []),
        file_deps.deps if file_deps is not None else "None",
    )

    assert file_deps is None
