#!/usr/bin/env python3

from typing import Text
from sourcefly.filetree.file_match_strategy import FileMatchStrategy


class CppFileMatchStrategy(FileMatchStrategy):
    def possible_matches(self, tailpart: Text):
        """
        Params:
        tailpart

        Returns:
        Cell of string

        """
        extend_dot_index = tailpart.rfind(".")

        noextends = tailpart
        if extend_dot_index < 0:
            raise ValueError("tailpart must contain extend, e.g.: header.h")

        noextends = tailpart[0:extend_dot_index]

        return (tailpart, noextends + ".cpp")
