from sourcefly.dep_resolver.dep_resolver import DepResolver
from sourcefly.dep_resolver.cpp_dep_resolver import CppDepResolver
from sourcefly.filetree.cpp_file_match_strategy import CppFileMatchStrategy
from sourcefly.sourcefly_factory.sourcefly_factory import SourceflyFactory
from sourcefly.filetree.file_match_strategy import FileMatchStrategy


class CppSourceFactory(SourceflyFactory):
    def create_dep_resolver(self) -> DepResolver:
        return CppDepResolver()

    def create_match_strategy(self) -> FileMatchStrategy:
        return CppFileMatchStrategy()
