import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, List, Any, TypeVar
from sourcefly.filetree.mod import FileTree
from sourcefly.filetree.file_match_strategy import FileMatchStrategy
from sourcefly.common.logger import zlogger


Self = TypeVar("Self", bound="FileDeps")


class FileDeps(object):
    def __init__(self, file: Path) -> None:
        self.file = file
        self.deps: list[FileDeps] = list()

    def todict(self) -> Dict[str, Any]:
        d = dict()
        d["file"] = str(self.file)
        d["deps"] = list(map(lambda dep: dep.todict(), self.deps))
        return d

    def tojson(self) -> str:
        return json.dumps(self.todict(), indent=2)

    @staticmethod
    def __display(node: Self) -> str:
        if node is None:
            return "None"

        return node.tojson()

    def __str__(self):
        return FileDeps.__display(self)


class DepResolver(ABC):
    def __init__(self, filetree: FileTree, entry=None):
        self.entry = entry

        self._resolved: Dict[
            Path, FileDeps
        ] = dict()  # cache resolved file, prevent file from parsing again
        self._root: Optional[FileDeps] = None

        self._filetree = filetree

    @abstractmethod
    def parse_deps(self, file: Path) -> list[Path]:
        """
        parse depencies of file

        """
        pass

    @abstractmethod
    def dep_file_match_strategy(self) -> FileMatchStrategy:
        pass

    def __cache_file(self, file: Path, fd: FileDeps):
        """
        Cache already parsed file
        """
        self._resolved[file.absolute()] = fd

    def __retrive_cache_file(self, file: Path) -> FileDeps:
        return self._resolved[file.absolute()]

    def set_entry(self, entry: Path):
        self.entry = entry

    def __check_entry(self):
        if self.entry is None:
            raise ValueError("self.entry is None, please set entry first")

    def path_cached(self, file: Path) -> bool:
        return self._resolved.get(file) != None

    def gen_file_deps(self, file: Path) -> Optional[FileDeps]:

        if file is None:
            raise ValueError("file can't be None!")

        if self.path_cached(file):
            return self.__retrive_cache_file(file)

        fd = FileDeps(file)

        # cache file first
        self.__cache_file(file, fd)

        deps_paths: list[Path] = self.parse_deps(fd.file)

        zlogger.debug(deps_paths)

        abs_dep_paths = [
            Path(p)
            for sublist in list(
                map(
                    lambda dep_path: self._filetree.try_find_file(str(dep_path)),
                    deps_paths,
                )
            )
            for p in sublist
        ]

        zlogger.debug(abs_dep_paths)

        optional_deps_iter = map(
            lambda dep_path: self.gen_file_deps(dep_path), abs_dep_paths
        )

        # remove None deps
        fd.deps = [x for x in optional_deps_iter if x is not None]

        return fd

    def deps_tree(self) -> Optional[FileDeps]:
        self.__check_entry()
        if self.entry is None:
            return None

        file_deps = self.gen_file_deps(self.entry)

        # if resovled already, file_deps will be None
        if file_deps is not None:
            self._root = file_deps

        return self._root


def filedeps_walker(filedeps: FileDeps):
    if filedeps is None:
        raise ValueError("filedeps can't be None")
    stack: List[FileDeps] = []
    stack.append(filedeps)

    def walk() -> Optional[FileDeps]:
        nonlocal stack
        if len(stack) <= 0:
            stack = None  # mark stack be None, when len(stack) calling, will raise exception
            return None

        current = stack.pop(0)

        if current is not None:
            for dep in current.deps:
                if dep is not None:
                    stack.append(dep)

        return current

    return walk
