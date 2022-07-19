from pathlib import Path
from abc import ABC, abstractmethod
from sourcefly.dep_resolver.dep_resolver import DepResolver
from sourcefly.filetree.file_match_strategy import FileMatchStrategy
from sourcefly.filetree.mod import FileTree


class SourceflyFactory(ABC):
    def __init__(self, project_root_dir: Path):
        self.project_root_dir = project_root_dir

    @abstractmethod
    def build_dep_resolver(self) -> DepResolver:
        pass

    def _build_file_tree(self) -> FileTree:
        filetree = FileTree(self.provide_glob_pattern())
        filetree.build_file_tree(self.project_root_dir)
        return filetree

    @abstractmethod
    def provide_glob_pattern(self) -> str:
        pass
