#!/usr/bin/env python3

from pathlib import Path
from sourcefly.filetree.mod import FileTree, TreeNode, split_path
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

    FileTree.insert_path_to_tree_node(root_node, paths[1:])
