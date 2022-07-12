from abc import ABC, abstractmethod
from sourcefly.dep_resolver.dep_resolver import DepResolver
from sourcefly.filetree.file_match_strategy import FileMatchStrategy


class SourceflyFactory(ABC):
    @abstractmethod
    def create_match_strategy(self) -> FileMatchStrategy:
        pass

    @abstractmethod
    def create_dep_resolver(self) -> DepResolver:
        pass
