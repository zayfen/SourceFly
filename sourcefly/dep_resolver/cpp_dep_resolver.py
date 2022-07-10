#!/usr/bin/env python3

from pathlib import Path
import re
from sourcefly.dep_resolver.dep_resolver import DepResolver


class CppDepResolver(DepResolver):
    def __init__(self, entry: Path):
        super().__init__(entry)


   def parse_deps(self, file: Path) -> list[Path]:
       cpp_include_pattern = re.compile(r'^\s*?#include\s*?\<(.?)\s*?\>\s*$', re.MULTILINE)

       m = cpp_include_pattern.match(str(file))

       # to get all include files(tailpart)
       return []
