from pathlib import Path
from sourcefly.sourcefly_factory.sourcefly_factory import SourceflyFactory
from sourcefly.dep_resolver.dep_resolver import filedeps_walker
from sourcefly.common.logger import zlogger


class App:
    def __init__(self, factory: SourceflyFactory):
        self.factory = factory

    def fly(self, project_root_dir: Path, entry: Path) -> list[str]:
        dep_resolver = self.factory.build_dep_resolver(project_root_dir)

        # resolve project entry file, to get all project files
        opt_file_deps = dep_resolver.gen_file_deps(entry)
        zlogger.debug(opt_file_deps)

        if opt_file_deps is None:
            return []

        walk = filedeps_walker(opt_file_deps)

        # match every dep file in filetree, copy matched file to dst directory
        final_paths = []

        while True:
            dep = walk()
            if dep is None:
                break

            zlogger.debug(dep)

            final_paths.append(str(dep.file))

        zlogger.debug(final_paths)

        return final_paths
