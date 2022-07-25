from pathlib import Path
from sourcefly.file_migrations.file_migrations import migrate
from sourcefly.sourcefly_factory.cpp_sourcefly_factory import CppSourceFactory
from sourcefly.app import App
from sourcefly.common.logger import zlogger


def test_app():
    factory = CppSourceFactory(Path("tests"))
    app = App(factory)

    file_list = app.fly(Path("tests/cpp/main.cpp"))

    zlogger.debug(file_list)
    assert len(file_list) > 0

    migrate(list(map(lambda item: Path(item), file_list)), Path("tmp"))
