#!/usr/bin/env python3

from typing import Optional, Tuple

from sourcefly.common.logger import zlogger
from sourcefly.filetree.file_match_strategy import FileMatchStrategy


class CppFileMatchStrategy(FileMatchStrategy):
    def possible_matches(self, tailpart: str) -> Optional[Tuple]:
        """
        Params:
        tailpart

        Returns:
        two string items cell
        """
        zlogger.debug(tailpart)

        if tailpart == "":
            return None

        extend_dot_index = tailpart.rfind(".")

        if extend_dot_index < 0:
            return (tailpart,)

        extends = tailpart[extend_dot_index + 1 :]

        zlogger.debug(extends)

        # maybe standard header, so no .h[pp] extends
        if extends != "h" and extends != "hpp":
            return (tailpart,)

        noextends = tailpart
        noextends = tailpart[0:extend_dot_index]

        zlogger.info("extends: ", extends)
        return (tailpart, noextends + ".cpp")
