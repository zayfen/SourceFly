#!/usr/bin/env python3

from pathlib import Path
import re
from sourcefly.dep_resolver.dep_resolver import DepResolver


class CppDepResolver(DepResolver):
    def __init__(self):
        super().__init__()

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
        # to get all include files(tailpart)
        return list(map(lambda f: Path(f), matched_list))
