#!/usr/bin/env python3

from pathlib import Path
import re
from sourcefly.dep_resolver.dep_resolver import DepResolver
from sourcefly.filetree.file_match_strategy import FileMatchStrategy
from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy
from sourcefly.common.singleton_class import SingletonClass


class CppDepResolver(SingletonClass, DepResolver):
    def __init__(self, entry: Path):
        super().__init__(entry)

    def parse_deps(self, file: Path) -> list[Path]:
        cpp_include_pattern = re.compile(
            r"^\s*?#include\s*?\<(.*?)\s*?\>\s*$", re.MULTILINE
        )

        file_content = ""
        if not file.exists():
            return []

        with open(file.absolute(), "r") as f:
            file_content = f.read()

        matched_list: list[str] = cpp_include_pattern.findall(file_content)

        # to get all include files(tailpart)
        return list(map(lambda f: Path(f), matched_list))

    def match_strategy(self) -> FileMatchStrategy:
        return CppFileMatchStrategy()
