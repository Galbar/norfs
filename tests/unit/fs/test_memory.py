import random

from typing import Set
from unittest import (
    TestCase,
    mock,
)

from norfs.fs import Path
from norfs.fs import NotAFileError
from norfs.fs.memory import (
    MemoryDirectory,
    MemoryFile,
    MemoryFileSystem,
)

from tests.tools import (
    randstr,
    random_path,
)


class TestMemoryDirectory(TestCase):
    sut: MemoryDirectory

    def setUp(self) -> None:
        self.sut = MemoryDirectory()

    def test_no_subdirs_when_created(self) -> None:
        assert [] == self.sut.list_dirs()

    def test_no_files_when_created(self) -> None:
        assert [] == self.sut.list_files()

    def test_subdirs_are_properly_listed_when_added(self) -> None:
        names: Set[str] = {mock.Mock(spec=str) for _ in range(random.randint(1, 10))}

        for name in names:
            self.sut.put_dir(name, mock.Mock(spec=MemoryDirectory))

        assert names == set(self.sut.list_dirs())
        assert [] == self.sut.list_files()

    def test_files_are_properly_listed_when_added(self) -> None:
        names: Set[str] = {mock.Mock(spec=str) for _ in range(random.randint(1, 10))}

        for name in names:
            self.sut.put_file(name, mock.Mock(spec=MemoryFile))

        assert names == set(self.sut.list_files())
        assert [] == self.sut.list_dirs()

    def test_get_dir(self) -> None:
        with self.assertRaises(NotADirectoryError):
            self.sut.get_dir(mock.Mock(spec=str))

        name: str = mock.Mock(spec=str)
        dir_: MemoryDirectory = mock.Mock(spec=MemoryDirectory)
        self.sut.put_dir(name, dir_)

        assert self.sut.get_dir(name) == dir_

    def test_get_file(self) -> None:
        with self.assertRaises(NotAFileError):
            self.sut.get_file(mock.Mock(spec=str))

        name: str = mock.Mock(spec=str)
        file_: MemoryFile = mock.Mock(spec=MemoryFile)
        self.sut.put_file(name, file_)

        assert self.sut.get_file(name) == file_

    def test_remove_dir(self) -> None:
        name: str = mock.Mock(spec=str)
        dir_: MemoryDirectory = mock.Mock(spec=MemoryDirectory)
        self.sut.put_dir(name, dir_)

        assert [name] == self.sut.list_dirs()
        assert dir_ == self.sut.get_dir(name)

        self.sut.remove_dir(name)

        assert [] == self.sut.list_dirs()

        with self.assertRaises(NotADirectoryError):
            self.sut.get_dir(name)

    def test_remove_file(self) -> None:
        name: str = mock.Mock(spec=str)
        file_: MemoryFile = mock.Mock(spec=MemoryFile)
        self.sut.put_file(name, file_)

        assert [name] == self.sut.list_files()
        assert file_ == self.sut.get_file(name)

        self.sut.remove_file(name)

        assert [] == self.sut.list_files()

        with self.assertRaises(NotAFileError):
            self.sut.get_file(name)


class TestMemoryFile(TestCase):
    contents: bytes
    sut: MemoryFile

    def setUp(self) -> None:
        self.contents = mock.Mock(spec=bytes)
        self.sut = MemoryFile(self.contents)

    def test_contents(self) -> None:
        assert self.sut.contents == self.contents


class TestMemoryFileSystem(TestCase):
    separator: str
    fs: MemoryFileSystem

    def setUp(self) -> None:
        self.separator = randstr(3)
        self.fs = MemoryFileSystem(None, separator=self.separator)

    def test_parse_path(self) -> None:
        expected_path: Path = random_path("")
        abs_input_path_str: str = self.separator.join(expected_path.tail)
        assert self.fs.parse_path(abs_input_path_str) == expected_path

    def test_path_to_string(self) -> None:
        path: Path = random_path("")
        path_str: str = self.separator.join(path.tail)
        result: str = self.fs.path_to_string(path)
        assert result == path_str

    def test_path_to_uri(self) -> None:
        path: Path = random_path("")
        path_str: str = self.separator.join(path.tail)
        assert self.fs.path_to_uri(path) == "memory://{}".format(path_str)
