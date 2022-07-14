#!/usr/bin/env python3

from pathlib import Path
from sourcefly.filetree.mod import FileTree, TreeNode, split_path
from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy
from sourcefly.sourcefly_factory.sourcefly_factory import SourceflyFactory


class App:
    def __init__(self, factory: SourceflyFactory):
        self.factory = factory

    def fly(self, project_root_dir: Path, entry: Path):
        strategy = self.factory.create_match_strategy()
        dep_resolver = self.factory.create_dep_resolver()

        # FileTree()


if __name__ == '__main__':
    paths = split_path(Path("./tests/cpp"))
    root_p = paths[0]
    root_node = TreeNode(root_p, None)

    tree = FileTree("**/*", CppFileMatchStrategy())
    tree.build_file_tree(Path("./tests/cpp"))
    tree.try_find_file(Path("tests/cpp/helper.h"))

