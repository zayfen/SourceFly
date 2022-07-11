from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict

from sourcefly.filetree.file_match_strategy import FileMatchStrategy


class FileDeps(object):
    def __init__(self, file: Path) -> None:
        self.file = file
        self.deps: list[FileDeps] = list()


class DepResolver(ABC):
    def __init__(self, entry: Path):
        self.entry = entry

        self._resolved: Dict[
            Path, bool
        ] = dict()  # cache resolved file, prevent file from parsing again
        self._root: Optional[FileDeps] = None

    @abstractmethod
    def parse_deps(self, file: Path) -> list[Path]:
        """
        parse depencies of file

        """
        pass

    @abstractmethod
    def match_strategy(self) -> FileMatchStrategy:
        pass

    def __cache_file(self, file: Path):
        """
        Cache already parsed file
        """
        self._resolved[file] = True

    def path_cached(self, file: Path) -> bool:
        return self._resolved.get(file, False)

    def find_file_deps(self, file: Path) -> Optional[FileDeps]:
        return None

    def gen_file_deps(self, file: Path) -> Optional[FileDeps]:

        if file is None or self.path_cached(file):
            return None

        fd = FileDeps(file)

        # cache file first
        self.__cache_file(file)

        deps_paths: list[Path] = self.parse_deps(fd.file)

        optional_deps_iter = map(
            lambda dep_path: self.gen_file_deps(dep_path), deps_paths
        )

        # remove None deps
        fd.deps = [x for x in optional_deps_iter if x is not None]

        return fd

    def deps_tree(self) -> Optional[FileDeps]:
        file_deps = self.gen_file_deps(self.entry)

        # if resovled already, file_deps is None
        if file_deps is not None:
            self._root = file_deps

        return self._root
