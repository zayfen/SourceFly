# coding: utf-8

from abc import ABCMeta, abstractmethod


class FileMatchStrategy(metaclass=ABCMeta):
    @abstractmethod
    def possible_matches(self, tailpart: str):
        pass
