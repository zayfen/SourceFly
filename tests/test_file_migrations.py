#!/usr/bin/env python3

from pathlib import Path
from sourcefly.file_migrations.file_migrations import (
    public_path_of_files,
    same_path_root,
    target_path_of_files,
)
from sourcefly.filetree.mod import list_files
from sourcefly.common.logger import zlogger


def test_same_path_root():
    ll = [["home", "zayfen", "github.com"], ["home", "zayfen", "codeup.com"]]

    same = same_path_root(ll)

    lll = [["home2", "zayfen", "github.com"], ["home", "zayfen", "codeup.com"]]
    same = same_path_root(lll)
    assert same == False

    llll = [[], ["home"]]
    same = same_path_root(llll)
    assert same == False

    lllll = [[], []]
    same = same_path_root(lllll)
    assert same == False


def test_public_path_of_files():
    lp = [
        Path.joinpath(Path.home(), "github.com"),
        Path.joinpath(Path.home(), "codeup.aliyun.com"),
    ]
    pp = public_path_of_files(lp)

    assert pp == str(Path.home())

    llp = [
        Path.joinpath(Path.home(), "github.com"),
        Path.joinpath(Path.home(), "github.com"),
    ]
    pp = public_path_of_files(llp)

    assert pp == str(Path.joinpath(Path.home(), "github.com"))


def test_target_path_of_files():
    files = list_files(Path("tests/cpp"))
    target_files = target_path_of_files(files, Path("src/"))

    assert target_files is not None
