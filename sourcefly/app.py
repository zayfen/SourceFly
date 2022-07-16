from pathlib import Path
from sourcefly.filetree.mod import FileTree, TreeNode, split_path
from sourcefly.sourcefly_factory.sourcefly_factory import SourceflyFactory
from sourcefly.dep_resolver.dep_resolver import filedeps_walker
from sourcefly.common.logger import zlogger


class App:
    def __init__(self, factory: SourceflyFactory):
        self.factory = factory

    def fly(self, project_root_dir: Path, entry: Path) -> list[str]:
        strategy = self.factory.create_match_strategy()
        dep_resolver = self.factory.create_dep_resolver()
        glob_pattern = self.factory.create_glob_pattern()

        filetree = FileTree(glob_pattern, strategy)
        root_tree_node = filetree.build_file_tree(project_root_dir)

        # resolve project entry file, to get all project files
        opt_file_deps = dep_resolver.gen_file_deps(entry)

        walk = filedeps_walker(opt_file_deps)

        # match every dep file in filetree, copy matched file to dst directory
        final_paths = []

        while True:
            dep = walk()
            if dep is None:
                break

            zlogger.debug(dep)

            final_paths.extend(filetree.try_find_file(str(dep.file)))

        zlogger.debug(final_paths)

        return final_paths
