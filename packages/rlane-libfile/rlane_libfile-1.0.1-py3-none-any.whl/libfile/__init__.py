"""Libfile.

This module offers a class that combines pathlib.Path, os.walk,
cached os.struct_stat, debug/trace logging, and the ability to execute
a --dry-run through 'most' of the code without changing the filesystem.

File(object) represents a filesystem item, such as a file or folder, which
may or may not exist when the object is initialized.  This differs
from os.DirEntry(object), which is only instantiated for an existing item.

File has nothing to do with input/output... yet.

For you old unix cats like me, a 'folder' is a 'directory', and this
module enjoys the 50% reduction in the number of syllables required,
the 3-fewer keystrokes for singular, 4 for plural, and non-collision
with python built-in 'dir'. Embrace the technology!

"""

import stat
from pathlib import Path

from loguru import logger

__all__ = ["File"]


class File:
    """Represent a filesystem item such as a file or folder.

    The path argument to the constructor, and other methods that take a
    path argument, accept either a string, or an object implementing the
    os.PathLike interface which returns a string, or another path object.

    See: https://docs.python.org/3/library/pathlib.html#pure-paths
    """

    # Don't change anything; for options like --no-action or --dry-run
    NO_ACTION = False

    def __init__(self, path, ignore_stat_errors=True):
        """Initialize a filesystem item, such as a file or folder, at `path`.

        If the item exists, cache the results of os.stat(2).
        The item may or may not exist.

        Arguments:
            path                string or os.PathLike

            ignore_stat_errors  Handle any exceptions raised trying to stat(2) the
                                item the same way FileNotFoundError is handled,
                                which is never raised.

        Attributes:
            pathname    pathname(str); same as str(self.path)
            path        pathlib.Path(object)
            exists      bool
            stats       os.struct_stat(object) if self.exists else None

        Cached state:
            `exists` and `stats` are the cached results of self.path.stat()
            when this object was created. Only access self.stats when self.exists.

        Current state:
            Use self.path.stat().

        Side effects:
            stat(2) is called once.

        """

        if isinstance(path, Path):
            self.path = path
        elif hasattr(path, "path") and isinstance(path.path, Path):
            self.path = path.path
        else:
            self.path = Path(str(path))

        try:
            self.stats = self.path.stat()
            self.exists = True
            return
        except FileNotFoundError:
            pass
        except Exception:  # noqa:
            if not ignore_stat_errors:
                raise

        self.stats = None
        self.exists = False

    @property
    def pathname(self):
        """str(self.path)."""
        return str(self.path)

    @property
    def isfile(self):
        """True if this is a regular file (or a symlink to one)."""
        return self.exists and stat.S_ISREG(self.stats.st_mode)

    @property
    def isfolder(self):
        """True if this is a folder (or a symlink to one)."""
        return self.exists and stat.S_ISDIR(self.stats.st_mode)

    isdir = isfolder

    def __eq__(self, other):

        return other and self.pathname == other.pathname

    def __repr__(self):

        return (
            f"{type(self).__name__}("
            + ", ".join(
                [
                    f"path={self.pathname!r}",
                    f"exists={self.exists}",
                    f"stats={self.stats})",
                ]
            )
            + ")"
        )

    @classmethod
    def walk(cls, paths):
        """Walk.

        Recursively walk `paths` generating a File(object) for each
        file found.  `paths` may be a single path or a list.  A single
        path may be a string or a File(object); `paths` may contain both.

        "@PATH" expansion.  Any path that begins with an AT-SIGN '@',
        is replaced with the list of paths read from the path; once, no recursion.

        After expansion, paths are ordered like /bin/ls orders its command
        line arguments: files before folders, each group sorted alphabetically.
        An error is logged for any path that does not exist.

        After ordering, all files are generated.

        After all files are generated, recurse into each folder,
        and repeat everything except for @PATH expansion.

        stat(2) is only called once, results are cached.

        Arguments:
            paths:              list of string or os.PathLike
        """

        # create a File(object) for each path, and separate files from folders.
        files = []
        folders = []

        for path in cls.expand_atfiles(paths):
            if not isinstance(path, cls):
                path = cls(path)

            if path.isfile:
                files.append(path)
            elif path.isdir:
                folders.append(path)
            else:
                logger.error("FileNotFoundError {!r}", path)

        # files
        yield from sorted(files, key=lambda _: _.pathname)

        # folders
        for folder in sorted(folders, key=lambda _: _.pathname):
            yield from folder.walker()

    def walker(self):
        """Docstring."""

        assert self.isdir
        files, folders = [], []

        for path in self.path.iterdir():

            path = type(self)(str(path))  # maybe don't use iterdir? use scandir?

            if path.isfile:
                files.append(path)
            elif path.isdir:
                folders.append(path)
            else:
                logger.error("FileNotFoundError {!r}", path)

        # files
        yield from sorted(files, key=lambda _: _.pathname)

        # folders
        for folder in sorted(folders, key=lambda _: _.pathname):
            yield from folder.walker()

    @staticmethod
    def expand_atfiles(items):
        """Expand @files.

        Yield the item, or each item in the list of items, expanding
        any @PATH's.  Any item that begins with an AT-SIGN '@', is
        replaced with items read from the PATH; once, no nesting.
        """

        for item in items if isinstance(items, list) else [items]:
            if isinstance(item, str) and item[0] == "@":
                with open(item[1:], encoding="utf-8") as atfile:
                    yield from [line.strip() for line in atfile]
            else:
                yield item

    # -------------------------------------------------------------------------------
    # Wrap some filesystem primitives to implement "--no-action".

    def mkdir(self, mode=0o777, parents=False, exist_ok=False, raise_errors=False):
        """Create directory.

        Wraps: pathlib.Path.mkdir(mode=0o777, parents=False, exist_ok=False)

        See: https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir

        Additional arguments:
            raise_errors        XXX
        """

        if self.exists:
            if self.isdir:
                if exist_ok:
                    logger.opt(depth=1).trace("already exists {!r}", self.pathname)
                    return True
                logger.opt(depth=1).error("already exists {!r}", self.pathname)
                if raise_errors:
                    raise FileExistsError
                return False

            logger.opt(depth=1).error("exists but not folder {!r}", self.pathname)
            if raise_errors:
                raise NotADirectoryError
            return False

        if self.NO_ACTION:
            logger.opt(depth=1).warning("not mkdir {!r}", self.pathname)
        else:
            logger.opt(depth=1).info("mkdir {!r}", self.pathname)
            self.path.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)

        return True

    mkfolder = mkdir

    def mkparent(self, mode=0o777, parents=False, exist_ok=False, raise_errors=False):
        """Create this path's parent folder."""

        return self.__class__(self.path.parent).mkfolder(
            mode=mode, parents=parents, exist_ok=exist_ok, raise_errors=raise_errors
        )

    def rmdir(self, missing_ok=True, raise_errors=False):
        """Remove directory.

        Wraps: pathlib.Path.rmdir()

        See: https://docs.python.org/3/library/pathlib.html#pathlib.Path.rmdir

        Additional arguments:
            missing_ok          If True, FileNotFoundError exceptions will be
                                ignored (same behavior as the POSIX rm -f command).

            raise_errors        XXX
        """

        if not self.exists:
            if missing_ok:
                logger.opt(depth=1).trace("already does not exist {!r}", self.pathname)
                return True
            logger.opt(depth=1).error("does not exist {!r}", self.pathname)
            if raise_errors:
                raise FileNotFoundError
            return False

        if not self.isdir:
            logger.opt(depth=1).error("exists but not folder {!r}", self.pathname)
            if raise_errors:
                raise NotADirectoryError
            return False

        if self.NO_ACTION:
            logger.opt(depth=1).warning("not rmdir {!r}", self.pathname)
        else:
            logger.opt(depth=1).info("rmdir {!r}", self.pathname)

            try:
                self.path.rmdir()
            except Exception:  # noqa:
                logger.opt(depth=1).error("rmdir {!r}", self.pathname)
                if raise_errors:
                    raise

        self.exists = False
        self.stats = None
        return True

    rmfolder = rmdir

    def rename(self, target):
        """Rename this file or folder.

        Wraps: pathlib.Path.rename(target)

        See: https://docs.python.org/3/library/pathlib.html#pathlib.Path.rename

        Arguments:
            target:             string or os.PathLike
        """

        if self == target:
            logger.opt(depth=1).trace("already named {!r}", self.pathname)

        elif self.NO_ACTION:
            logger.opt(depth=1).warning(
                "not rename {!r} -> {!r}", self.pathname, target.pathname
            )

        else:
            logger.opt(depth=1).info("rename {!r} -> {!r}", self.pathname, target.pathname)
            self.path.rename(target)

    def unlink(self, missing_ok=False):
        """Remove this file.

        Wraps: pathlib.Path.unlink(missing_ok=False)

        See: https://docs.python.org/3/library/pathlib.html#pathlib.Path.unlink
        """

        if not self.exists:
            if missing_ok:
                logger.opt(depth=1).trace("already does not exist {!r}", self.pathname)
                return
            raise FileNotFoundError

        if self.NO_ACTION:
            logger.opt(depth=1).warning("not unlink {!r}", self.pathname)

        else:
            logger.opt(depth=1).info("unlink {!r}", self.pathname)
            self.path.unlink(missing_ok)

        self.exists = False
        self.stats = None

    def symlink(self, path, parents=False):
        """Create symbolic link at path that points to this file.

        Similar to: pathlib.Path.symlink_to(target, target_is_directory=False)
        See: https://docs.python.org/3/library/pathlib.html#pathlib.Path.symlink_to

        Similar to: os.symlink(src, dst, target_is_directory=False, *, dir_fd=None)
        See: https://docs.python.org/3/library/os.html#os.symlink

        Arguments:
            path:       string or os.PathLike to the symbolic link to create.
                        The link created will point to this (self) file or folder.

            parents:    If parents is true, any missing parents of this
                        path are created as needed; they are created with
                        the default permissions without taking mode into
                        account (mimicking the POSIX mkdir -p command).
        """

        if isinstance(path, Path):
            linkpath = path
        elif hasattr(path, "pathname"):
            linkpath = Path(path.pathname)
        else:
            linkpath = Path(path)

        link = Path(linkpath)

        if parents:
            File(link).path.parent.mkdir(parents=parents, exist_ok=True)

        if self.NO_ACTION:
            logger.opt(depth=1).warning("not symlink {!r} -> {!r}", str(link), self.pathname)

        else:
            logger.opt(depth=1).info("symlink {!r} -> {!r}", str(link), self.pathname)
            link.symlink_to(self.path)

        return File(link)


if __name__ == "__main__":

    import sys

    class xFile(File):  # noqa:
        def __init__(self, *args, **kwargs):  # noqa:
            super().__init__(*args, **kwargs)
            self.digest = str(*args).upper()

        def __repr__(self):
            return super().__repr__()[:-1] + f", digest={self.digest!r})"

    # logger.remove(0)
    # logger.add(sys.stdout, level='TRACE')

    for file in xFile.walk(sys.argv[1:]):
        # print(file.path.absolute())
        print(file.pathname)
        # print(file.pathname)
