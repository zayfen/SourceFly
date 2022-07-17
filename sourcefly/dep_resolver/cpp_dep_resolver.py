#!/usr/bin/env python3

from pathlib import Path
import re
from sourcefly.dep_resolver.dep_resolver import DepResolver
from sourcefly.filetree.file_match_strategy import FileMatchStrategy
from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy
from sourcefly.filetree.mod import FileTree


class CppDepResolver(DepResolver):
    def __init__(self, filetree: FileTree):
        super().__init__(filetree)

    def parse_deps(self, file: Path) -> list[Path]:
        cpp_include_pattern = re.compile(
            r"^\s*?#include\s*?[\<\"](.*?)\s*?[\>\"]\s*$", re.MULTILINE
        )

        file_content = ""
        if not file.exists():
            return []

        with open(file.absolute(), "r") as f:
            file_content = f.read()

        matched_list: list[str] = cpp_include_pattern.findall(file_content)

        print("cpp_dep_resolver.py: matched_list: ", matched_list)
        # use match strategy to match more related files

        return [
            Path(p)
            for sublist in list(
                map(
                    lambda f: self.dep_file_match_strategy().possible_matches(f),
                    matched_list,
                )
            )
            for p in sublist
        ]

    def dep_file_match_strategy(self) -> FileMatchStrategy:
        return CppFileMatchStrategy()
