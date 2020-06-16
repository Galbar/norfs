import random

from unittest import (
    TestCase,
    mock,
)
from typing import List

from norfs.fs.base import (
    BaseFileSystem,
    FileSystemOperationError,
    Path,
)


class TestPath(TestCase):
    drive: str
    tail: List[str]
    sut: Path

    def setUp(self) -> None:
        self.drive = mock.Mock(spec=str)
        self.tail = [mock.Mock(spec=str) for _ in range(random.randint(1, 10))]
        self.sut = Path(self.drive, *self.tail)

    def test_drive(self) -> None:
        assert self.sut.drive == self.drive

    def test_tail(self) -> None:
        assert self.sut.tail == tuple(self.tail)

    def test_basename(self) -> None:
        assert self.sut.basename == self.tail[-1]

    def test_parent(self) -> None:
        assert self.sut.parent == Path(self.drive, *self.tail[:-1])

    def test_child(self) -> None:
        child_name: str = mock.Mock(spec=str)
        assert self.sut.child(child_name) == Path(self.drive, *self.tail, child_name)

    def test_repr(self) -> None:
        assert self.sut.__repr__() == f"Path(drive={self.drive}, tail={tuple(self.tail)})"


class TestBaseFileSystem(TestCase):
    sut: BaseFileSystem
    path: Path

    def setUp(self) -> None:
        self.sut = BaseFileSystem()
        self.path = mock.Mock(spec=Path)

    def test_parse_path(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.parse_path(mock.Mock(spec=str))

    def test_path_exists(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.path_exists(mock.Mock(spec=str))

    def test_path_to_string(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.path_to_string(mock.Mock(spec=str))

    def test_path_to_uri(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.path_to_uri(mock.Mock(spec=str))

    def test_file_read(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.file_read(mock.Mock(spec=str))

    def test_file_write(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.file_write(mock.Mock(spec=str), mock.Mock(spec=bytes))

    def test_file_remove(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.file_remove(mock.Mock(spec=str))

    def test_dir_list(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.dir_list(mock.Mock(spec=str))

    def test_dir_remove(self) -> None:
        with self.assertRaises(FileSystemOperationError):
            self.sut.dir_remove(mock.Mock(spec=str))

    def test_repr(self) -> None:
        assert self.sut.__repr__() == "BaseFileSystem()"

    def test_eq(self) -> None:
        assert self.sut == self.sut
        assert self.sut != BaseFileSystem()
        assert self.sut != mock.Mock()

    def test_hash(self) -> None:
        assert hash(self.sut) == hash(id(self.sut))
