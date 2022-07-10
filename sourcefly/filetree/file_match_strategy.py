# coding: utf-8

from abc import ABCMeta, abstractmethod
from typing import Text


class FileMatchStrategy(metaclass=ABCMeta):
    @abstractmethod
    def possible_matches(self, tailpart: Text):
        pass
