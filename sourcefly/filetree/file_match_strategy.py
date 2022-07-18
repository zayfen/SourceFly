# coding: utf-8

from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple


class FileMatchStrategy(metaclass=ABCMeta):
    @abstractmethod
    def possible_matches(self, tailpart: str) -> Optional[Tuple]:
        pass
