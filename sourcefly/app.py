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
