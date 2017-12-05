import random

from unittest import (
    TestCase,
    mock,
)
from typing import (
    Any,
    Generic,
    List,
    Type,
    TypeVar,
)

from norfs.filesystem import (
    BaseFileSystemObject,
    Directory,
    File,
)
from norfs.fs import (
    BaseFileSystem,
    DirListResult,
    NotAFileError,
    Path,
)
from norfs.copy import CopyHandler

from tests.tools import (
    random_path,
    randstr,
)


T = TypeVar("T", bound=BaseFileSystemObject)


class FileSystemObjectTestCase(Generic[T], TestCase):
    CLASS_UNDER_TEST: Type[T]

    filesystem: Any
    path: Any
    copy_handler: Any
    sut: T

    def setUp(self) -> None:
        self.filesystem = mock.Mock(spec=BaseFileSystem)
        self.path = mock.Mock(spec=Path)
        self.copy_handler = mock.Mock(spec=CopyHandler)
        self.sut = self.CLASS_UNDER_TEST(self.filesystem, None, self.copy_handler, _path=self.path)

    def test_public_constructor_and_internal_constructor_build_the_same_object(self) -> None:
        path_str: str = mock.Mock(spec=str)
        public: T = self.CLASS_UNDER_TEST(self.filesystem, path_str, self.copy_handler)
        internal: T = self.CLASS_UNDER_TEST(self.filesystem, None, self.copy_handler,
                                            _path=self.filesystem.parse_path.return_value)
        assert public == internal
        self.filesystem.parse_path.assert_called_once_with(path_str)

    def test_path(self) -> None:
        assert self.sut.path == self.filesystem.path_to_string.return_value
        self.filesystem.path_to_string.assert_called_once_with(self.path)

    def test_uri(self) -> None:
        assert self.sut.uri == self.filesystem.path_to_uri.return_value
        self.filesystem.path_to_uri.assert_called_once_with(self.path)

    def test_name(self) -> None:
        assert self.sut.name == self.path.basename

    def test_is_file(self) -> None:
        assert self.sut.is_file() is False

    def test_is_dir(self) -> None:
        assert self.sut.is_dir() is False

    def test_as_file(self) -> None:
        with self.assertRaises(NotAFileError):
            self.sut.as_file()

    def test_as_dir(self) -> None:
        with self.assertRaises(NotADirectoryError):
            self.sut.as_dir()

    def test_exists(self) -> None:
        assert self.sut.exists() == self.filesystem.path_exists.return_value
        self.filesystem.path_exists.assert_called_once_with(self.path)

    def test_remove(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.sut.remove()

    def test_parent(self) -> None:
        assert self.sut.parent() == Directory(self.filesystem, None, self.copy_handler, _path=self.path.parent)

    def test_copy(self) -> None:
        dst: BaseFileSystemObject = mock.Mock(spec=BaseFileSystemObject)
        self.sut.copy(dst)
        self.copy_handler.copy.assert_called_once_with(self.sut._copy_object(), dst._copy_object())

    def test_repr(self) -> None:
        assert self.sut.__repr__() == (f"{self.CLASS_UNDER_TEST.__name__}(fs={self.filesystem}, "
                                       f"path={self.sut.path}, copy_handler={self.copy_handler})")

    def test_eq(self) -> None:
        other_filesystem: BaseFileSystem = mock.Mock(spec=BaseFileSystem)
        other_path: Path = mock.Mock(spec=Path)
        other_copy_handler: CopyHandler = mock.Mock(spec=CopyHandler)

        assert mock.Mock() != self.sut
        assert self.sut == self.sut
        assert self.sut == self.CLASS_UNDER_TEST(self.filesystem, None, self.copy_handler, _path=self.path)
        assert self.sut != self.CLASS_UNDER_TEST(other_filesystem, None, self.copy_handler, _path=self.path)
        assert self.sut != self.CLASS_UNDER_TEST(self.filesystem, None, other_copy_handler, _path=self.path)
        assert self.sut != self.CLASS_UNDER_TEST(self.filesystem, None, self.copy_handler, _path=other_path)

        other: BaseFileSystemObject = BaseFileSystemObject(other_filesystem, None, other_copy_handler, _path=self.path)
        file_: File = File(other_filesystem, None, other_copy_handler, _path=self.path)
        dir_: Directory = Directory(other_filesystem, None, other_copy_handler, _path=self.path)

        assert other != file_
        assert other != dir_
        assert file_ != dir_


class TestBaseFileSystemObject(FileSystemObjectTestCase[BaseFileSystemObject]):
    CLASS_UNDER_TEST = BaseFileSystemObject


class TestDirectory(FileSystemObjectTestCase[Directory]):
    CLASS_UNDER_TEST = Directory

    def test_is_dir(self) -> None:
        assert self.sut.is_dir() is True

    def test_as_dir(self) -> None:
        assert self.sut.as_dir() is self.sut

    def test_remove(self) -> None:
        self.sut.remove()
        self.filesystem.dir_remove.assert_called_once_with(self.path)

    def test_list(self) -> None:
        files: List[Path] = [random_path() for _ in range(random.randint(1, 5))]
        dirs: List[Path] = [random_path() for _ in range(random.randint(1, 5))]
        others: List[Path] = [random_path() for _ in range(random.randint(1, 5))]

        self.filesystem.dir_list.return_value = DirListResult(files, dirs, others)

        actual: List[BaseFileSystemObject] = self.sut.list()
        expected: List[BaseFileSystemObject] = (
            [BaseFileSystemObject(self.filesystem, None, self.copy_handler, _path=path) for path in others] +
            [File(self.filesystem, None, self.copy_handler, _path=path) for path in files] +
            [Directory(self.filesystem, None, self.copy_handler, _path=path) for path in dirs]
        )
        assert set(actual) == set(expected)

    def test_subdir(self) -> None:
        child_name: str = randstr()
        assert self.sut.subdir(child_name) == Directory(self.filesystem, None, self.copy_handler,
                                                        _path=self.path.child.return_value)
        self.path.child.assert_called_once_with(child_name)

    def test_file(self) -> None:
        child_name: str = randstr()
        assert self.sut.file(child_name) == File(self.filesystem, None, self.copy_handler,
                                                 _path=self.path.child.return_value)
        self.path.child.assert_called_once_with(child_name)


class TestFile(FileSystemObjectTestCase[File]):
    CLASS_UNDER_TEST = File

    def test_is_file(self) -> None:
        assert self.sut.is_file() is True

    def test_as_file(self) -> None:
        assert self.sut.as_file() is self.sut

    def test_remove(self) -> None:
        self.sut.remove()
        self.filesystem.file_remove.assert_called_once_with(self.path)

    def test_read(self) -> None:
        assert self.sut.read() == self.filesystem.file_read.return_value
        self.filesystem.file_read.assert_called_once_with(self.path)

    def test_write(self) -> None:
        contents: bytes = mock.Mock(spec=bytes)
        self.sut.write(contents)
        self.filesystem.file_write.assert_called_once_with(self.path, contents)


del FileSystemObjectTestCase
