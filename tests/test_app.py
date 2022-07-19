from pathlib import Path
from sourcefly.sourcefly_factory.cpp_sourcefly_factory import CppSourceFactory
from sourcefly.app import App
from sourcefly.common.logger import zlogger


def test_app():
    factory = CppSourceFactory(Path("tests"))
    app = App(factory)

    list = app.fly(Path("tests/cpp/main.cpp"))

    zlogger.debug(list)
    assert len(list) > 0
