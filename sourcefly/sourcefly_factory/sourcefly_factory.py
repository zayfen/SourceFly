from pathlib import Path
from abc import ABC, abstractmethod
from sourcefly.dep_resolver.dep_resolver import DepResolver
from sourcefly.filetree.file_match_strategy import FileMatchStrategy
from sourcefly.filetree.mod import FileTree


class SourceflyFactory(ABC):
    @abstractmethod
    def build_dep_resolver(self, project_root_dir: Path) -> DepResolver:
        pass

    def _build_file_tree(self, project_root_dir: Path) -> FileTree:
        filetree = FileTree(self.provide_glob_pattern())
        filetree.build_file_tree(project_root_dir)
        return filetree

    @abstractmethod
    def provide_glob_pattern(self) -> str:
        pass
