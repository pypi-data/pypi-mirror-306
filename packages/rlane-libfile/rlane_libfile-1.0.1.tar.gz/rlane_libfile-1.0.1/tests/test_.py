import os
import sys

import pytest
from loguru import logger

from libfile import File

# from tests.fixtures import atfile

logger.remove(0)
logger.add(sys.stdout, level="TRACE")


def test_enoent():
    f = File("bobo")
    assert not f.exists
    assert not f.isdir
    assert not f.isfile


def test_enoent_never_raise():
    f = File("bobo", ignore_stat_errors=False)
    assert not f.exists
    assert not f.isdir
    assert not f.isfile


def test_eperm():
    f = File("/proc/1/cwd")
    assert not f.exists
    assert not f.isdir
    assert not f.isfile


def _disabled_test_eperm_raise():
    with pytest.raises(PermissionError):
        # _ = File("/proc/1/cwd", ignore_stat_errors=False)
        _ = File("/tmp/no-perms/bobo", ignore_stat_errors=False)


def test_dot():
    f = File(".")
    assert f.exists
    assert f.isdir
    assert not f.isfile


def test_self():
    f = File(__file__)
    assert f.exists
    assert not f.isdir
    assert f.isfile


# -------------------------------------------------------------------------------
# def mkparent(self, mode=0o777, parents=False, exist_ok=False, raise_errors=False):


def _disabled_test_mkparent_no_action():
    print()
    File.NO_ACTION = True
    f = File(".test.dir/bob/ralpha/sally/file.txt")
    assert f.mkparent(parents=True)


def _disabled_test_mkparent():
    print()
    File.NO_ACTION = False
    f = File(".test.dir/bob/ralpha/sally/file.txt")
    assert f.mkparent(parents=True)


def test_rmdir_enoent_no_action():
    print()
    File.NO_ACTION = True
    f = File(".test.dir/bobo")
    assert f.rmdir(missing_ok=True)


def test_rmdir_enoent():
    print()
    File.NO_ACTION = False
    f = File(".test.dir/bobo")
    assert f.rmdir(missing_ok=True)


def test_rmdir_eperm_no_action():
    print()
    File.NO_ACTION = True
    f = File("/proc/1")
    assert f.rmdir()


def _disabled_test_rmdir_eperm():
    print()
    File.NO_ACTION = False
    with pytest.raises(PermissionError):
        File("/tmp/no-perms/bobo").rmdir(raise_errors=True)


def test_rmdir_no_action():
    print()
    f = File(".test.dir/bob/ralpha/sally/file.txt")
    File.NO_ACTION = True
    File(f.path.parent).rmdir()
    File(f.path.parent.parent).rmdir()
    File(f.path.parent.parent.parent).rmdir()
    File(f.path.parent.parent.parent.parent).rmdir()


def test_rmdir():
    print()
    f = File(".test.dir/bob/ralpha/sally/file.txt")
    File.NO_ACTION = False
    File(f.path.parent).rmdir()
    File(f.path.parent.parent).rmdir()
    File(f.path.parent.parent.parent).rmdir()
    File(f.path.parent.parent.parent.parent).rmdir()


def test_expand_atfiles_1():
    print()
    paths = ["red", "yellow", "blue"]
    assert paths == list(File.expand_atfiles(paths))


@pytest.fixture(name="atfile")
def fixture_atfile():
    name = "yellow"
    with open(name, "w", encoding="utf-8") as fp:
        print("lemon\n@norecurse\ngoldenrod", file=fp)
    yield "@" + name
    os.unlink(name)


def test_expand_atfiles_2(atfile):
    print()
    paths = ["red", atfile, "blue"]
    assert ["red", "lemon", "@norecurse", "goldenrod", "blue"] == list(
        File.expand_atfiles(paths)
    )


def test_walk_1(atfile):
    print()
    for f in File.walk([atfile, "ttree"]):
        print(f)
