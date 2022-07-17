from pathlib import Path
from sourcefly.dep_resolver.dep_resolver import DepResolver
from sourcefly.dep_resolver.cpp_dep_resolver import CppDepResolver
from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy
from sourcefly.sourcefly_factory.sourcefly_factory import SourceflyFactory
from sourcefly.filetree.file_match_strategy import FileMatchStrategy
from sourcefly.filetree.mod import FileTree


class CppSourceFactory(SourceflyFactory):
    def build_dep_resolver(self, project_root_dir: Path) -> DepResolver:
        return CppDepResolver(self._build_file_tree(project_root_dir))

    def provide_glob_pattern(self) -> str:
        return "**/*"
