#coding: utf-8

from abc import ABCMeta, abstractmethod
from typing import AnyStr


class FileMatchStrategy(metaclass=ABCMeta):
    @abstractmethod
    def possible_matches(self, tailpart: AnyStr):
        pass
