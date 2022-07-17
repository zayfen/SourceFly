# coding: utf-8

import os
import json
from pathlib import Path
from typing import List, Optional, TypeVar, Dict
from sourcefly.common.logger import zlogger
from sourcefly.filetree.file_match_strategy import FileMatchStrategy


def some(fn, iterable):
    for item in iterable:
        if fn(item):
            return True
    return False


def list_files(dir: Path, glob_pattern: str = "**/*") -> list[Path]:
    """
    list all files in directory, including files in subdirectories
    @params dir {string} - target directory
    @returns list<string>
    """
    p = dir
    paths_iter = p.glob(glob_pattern)
    paths_iter = filter(lambda file: file.is_file(), paths_iter)
    # files = map(lambda file: str(file), files)
    return list(paths_iter)


def find_files_by_tailpart(
    path_list: List[Path], tailpart: str, match_strategy: FileMatchStrategy
) -> list[Path]:
    """
    find file by tail part, e.g.: tail: dir/abc.txt, files: [dir/dir/abc.txt, dir/abc.txt, def.txt]

    @params tailpart { string }
    @params startage
    @returns: full path of file or None
    """
    matches = match_strategy.possible_matches(tailpart)

    zlogger.debug(matches)

    matched_files = filter(
        lambda path: some(lambda match_file: path.match(match_file), matches),
        path_list,
    )

    return list(matched_files)


def split_path(p: Path) -> list[str]:
    if not p.exists():
        return []

    abs_path_str = str(p.absolute())
    zlogger.debug(abs_path_str)

    sep = os.path.sep

    paths = abs_path_str.split(sep)
    paths = list(filter(lambda p: p != "", paths))

    zlogger.debug("pruned paths: " + str(paths))
    return paths


def split_str_path(p: str) -> list[str]:
    if p is None:
        return []

    sep = os.path.sep
    paths = p.split(sep)
    paths = list(filter(lambda p: p != "", paths))
    return paths


Self = TypeVar("Self", bound="TreeNode")


class TreeNode:
    def __init__(
        self,
        value: str,
        parent: Optional[Self] = None,
        children={},
    ):
        self.value: str = value
        self.parent = parent
        self.children: Dict[str, TreeNode] = children  # dict better find performance

    def set_children(self, children: Dict[str, "TreeNode"]):
        self.children = children

    @staticmethod
    def __display(node: Self) -> str:

        if node is None:
            return "None"

        return node.tojson()

    def todict(self):
        d = dict()
        d[self.value] = list(
            map(
                lambda item: item[1].todict(),
                self.children.items(),
            )
        )

        # d["value"] = self.value
        # d["children"] = list(
        #     map(
        #         lambda item: item[1].todict(),
        #         self.children.items(),
        #     )
        # )

        return d

    def tojson(self) -> str:
        return json.dumps(self.todict(), indent=2)

    def __str__(self) -> str:
        return TreeNode.__display(self)

    # def __repr__(self) -> str:
    #     return TreeNode.__display(self)


class FileTree:
    def __init__(self, glob_pattern: str):
        self.glob_pattern = glob_pattern
        self.tree_nodes = {}  # dict[str, TreeNode]
        self.__root = None

        # leaf nodes of FileTree, can hava better performance of searching
        # __leaf_nodes type: Dict[str, list[TreeNode]]
        self.__leaf_nodes: Dict[str, list[TreeNode]] = dict()

    def __root_tree_node(self) -> Optional[TreeNode]:
        if self.__root is None:
            self.__root = TreeNode("", parent=None, children=self.tree_nodes)

        return self.__root

    def __insert_path_to_tree_nodes(self, p: Path):
        if not p.exists():
            return

        paths = split_path(p)

        if len(paths) > 0:
            root_p = paths[0]

            # handle root path
            if self.tree_nodes.get(root_p) is None:
                self.tree_nodes[root_p] = TreeNode(root_p, None)

            self.__insert_path_to_tree_node(self.tree_nodes[root_p], paths[1:])

    def __insert_path_to_tree_node(self, node: TreeNode, children_paths: list[str]):
        zlogger.debug(node.value)
        zlogger.debug(children_paths)
        zlogger.debug(len(node.children))
        zlogger.debug(list(map(lambda c: c.value, node.children.values())))

        _parent = node

        if len(children_paths) == 0 or node is None:
            self.__save_leaf_node(_parent)
            return

        for cp in children_paths:
            zlogger.info(cp)
            if _parent.children.get(cp) is None:
                zlogger.info(" is None")
                new_node = TreeNode(cp, _parent, dict())
                _parent.children[cp] = new_node

            _parent = _parent.children[cp]

        zlogger.debug(list(map(lambda c: c.value, node.children.values())))

        # now _parent is leaf node (save it)
        self.__save_leaf_node(_parent)

    def __save_leaf_node(self, node: TreeNode):
        if self.__leaf_nodes.get(node.value) is None:
            self.__leaf_nodes[node.value] = []
        self.__leaf_nodes[node.value].append(node)

    def build_file_tree(self, dir: Path) -> Optional[TreeNode]:
        files = list_files(dir)

        for file_p in files:
            self.__insert_path_to_tree_nodes(file_p)

        return self.__root_tree_node()

    def leaf_node_to_abs_path(self, node: TreeNode) -> str:
        if node is None:
            return ""

        paths: list[str] = []
        _node: Optional[TreeNode] = node

        while _node is not None:
            paths.append(_node.value)
            _node = _node.parent

        paths.reverse()

        return os.path.sep.join(paths)

    def try_find_file(self, tailpart: str) -> list[str]:

        paths = split_str_path(tailpart)
        paths.reverse()

        zlogger.debug(paths)

        if len(paths) <= 0:
            return []

        zlogger.debug(self.__leaf_nodes)
        zlogger.debug(paths[0])

        if self.__leaf_nodes.get(paths[0]) is None:
            return []

        list_tree_nodes = self.__leaf_nodes[paths[0]]
        zlogger.debug(list_tree_nodes)

        for p in paths[1:]:
            zlogger.debug(p)

            list_tree_nodes = list(
                filter(lambda node: node.parent.value == p, list_tree_nodes)
            )

            zlogger.debug(list(list_tree_nodes))
            zlogger.debug(list(list_tree_nodes)[0].parent)

            list_tree_nodes = list(map(lambda node: node.parent, list_tree_nodes))
            zlogger.debug(list(list_tree_nodes))

        return list(
            map(
                lambda node: self.leaf_node_to_abs_path(node.parent)
                + os.path.sep
                + tailpart,
                list_tree_nodes,
            )
        )
