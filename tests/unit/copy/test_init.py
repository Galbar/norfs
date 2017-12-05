from typing import (
    Any,
    Generic,
    TypeVar,
    Type,
)
from unittest import (
    TestCase,
    mock,
)

from norfs.copy import (
    CopyDirectory,
    CopyError,
    CopyFile,
    CopyFileSystemObject,
    CopyHandler,
    GenericCopier,
)
from norfs.fs import (
    BaseFileSystem,
    Path,
)
from norfs.fs.memory import (
    MemoryDirectory,
    MemoryFileSystem,
)

from tests.tools import (
    randstr,
    random_path,
)


T = TypeVar('T', bound=CopyFileSystemObject)


class BaseTestCopyFileSystemObject(Generic[T]):
    filesystem: Any
    path: Path
    sut: T
    CLASS: Type[T]

    def setUp(self) -> None:
        self.filesystem = mock.Mock(spec=BaseFileSystem)
        input_drive: str = mock.Mock(spec=str)
        input_tail: str = mock.Mock(spec=str)
        self.path = Path(input_drive, input_tail)
        self.sut = self.CLASS(self.filesystem, self.path)

    def test_fs(self) -> None:
        assert self.sut.fs == self.filesystem

    def test_path(self) -> None:
        assert self.sut.path == self.path


class TestCopyFileSystemObject(BaseTestCopyFileSystemObject[CopyFileSystemObject], TestCase):
    CLASS = CopyFileSystemObject

    def test_copy(self) -> None:
        with self.assertRaises(TypeError):
            self.sut.copy(mock.Mock(spec=CopyFileSystemObject), mock.Mock(spec=GenericCopier))

    def test_copy_from_file(self) -> None:
        with self.assertRaises(TypeError):
            self.sut.copy_from_file(mock.Mock(spec=CopyFile), mock.Mock(spec=GenericCopier))

    def test_copy_from_dir(self) -> None:
        with self.assertRaises(TypeError):
            self.sut.copy_from_dir(mock.Mock(spec=CopyDirectory), mock.Mock(spec=GenericCopier))

    def test_eq(self) -> None:
        other_filesystem: BaseFileSystem = mock.Mock(spec=BaseFileSystem)
        other_path: Path = mock.Mock(spec=Path)
        assert self.sut == self.sut
        assert self.sut == CopyFileSystemObject(self.filesystem, self.path)
        assert self.sut != CopyFileSystemObject(other_filesystem, self.path)
        assert self.sut != CopyFileSystemObject(self.filesystem, other_path)
        assert self.sut != CopyFile(self.filesystem, self.path)
        assert self.sut != CopyDirectory(self.filesystem, self.path)
        assert self.sut != mock.Mock()


class TestCopyFile(BaseTestCopyFileSystemObject[CopyFile], TestCase):
    CLASS = CopyFile

    def test_copy(self) -> None:
        dst: Any = mock.Mock(spec=CopyFileSystemObject)
        copier: Any = mock.Mock(spec=GenericCopier)
        self.sut.copy(dst, copier)

        dst.copy_from_file.assert_called_once_with(self.sut, copier)

    def test_copy_from_file(self) -> None:
        src: CopyFile = mock.Mock(spec=CopyFile)
        copier: Any = mock.Mock(spec=GenericCopier)
        self.sut.copy_from_file(src, copier)

        copier.copy_file_to_file.assert_called_once_with(src, self.sut)

    def test_copy_from_dir(self) -> None:
        with self.assertRaises(TypeError):
            self.sut.copy_from_dir(mock.Mock(spec=CopyDirectory), mock.Mock(spec=GenericCopier))

    def test_eq(self) -> None:
        other_filesystem: BaseFileSystem = mock.Mock(spec=BaseFileSystem)
        other_path: Path = mock.Mock(spec=Path)
        assert self.sut == self.sut
        assert self.sut == CopyFile(self.filesystem, self.path)
        assert self.sut != CopyFile(other_filesystem, self.path)
        assert self.sut != CopyFile(self.filesystem, other_path)
        assert self.sut != CopyFileSystemObject(self.filesystem, self.path)
        assert self.sut != CopyDirectory(self.filesystem, self.path)
        assert self.sut != mock.Mock()


class TestCopyDirectory(BaseTestCopyFileSystemObject[CopyDirectory], TestCase):
    CLASS = CopyDirectory

    def test_copy(self) -> None:
        dst: Any = mock.Mock(spec=CopyFileSystemObject)
        copier: Any = mock.Mock(spec=GenericCopier)
        self.sut.copy(dst, copier)

        dst.copy_from_dir.assert_called_once_with(self.sut, copier)

    def test_copy_from_file(self) -> None:
        src: CopyFile = mock.Mock(spec=CopyFile)
        copier: Any = mock.Mock(spec=GenericCopier)
        self.sut.copy_from_file(src, copier)

        copier.copy_file_to_file.assert_called_once_with(src, self.sut.file(self.path.basename))

    def test_copy_from_dir(self) -> None:
        src: CopyDirectory = mock.Mock(spec=CopyFile)
        copier: Any = mock.Mock(spec=GenericCopier)
        self.sut.copy_from_dir(src, copier)

        copier.copy_dir_to_dir.assert_called_once_with(src, self.sut)

    def test_subdir(self) -> None:
        sub_name: str = mock.Mock(spec=str)
        sub_path: Path = self.path.child(sub_name)

        output: CopyDirectory = self.sut.subdir(sub_name)

        assert output == CopyDirectory(self.filesystem, sub_path)

    def test_file(self) -> None:
        sub_name: str = mock.Mock(spec=str)
        sub_path: Path = self.path.child(sub_name)

        output: CopyFile = self.sut.file(sub_name)

        assert output == CopyFile(self.filesystem, sub_path)


class TestGenericCopier(TestCase):
    sut: GenericCopier
    src_root: MemoryDirectory
    src_fs: MemoryFileSystem
    dst_root: MemoryDirectory
    dst_fs: MemoryFileSystem

    def setUp(self) -> None:
        self.sut = GenericCopier()
        self.src_root = MemoryDirectory()
        self.src_fs = MemoryFileSystem(self.src_root)
        self.dst_root = MemoryDirectory()
        self.dst_fs = MemoryFileSystem(self.dst_root)

    def test_copy_dir_to_dir(self) -> None:
        src_path: Path = random_path()
        dst_path: Path = random_path()
        content1: bytes = randstr().encode()
        content2: bytes = randstr().encode()

        self.src_fs.file_write(src_path.child("file1"), content1)
        self.src_fs.file_write(src_path.child("subdir").child("file2"), content2)
        assert self.src_fs.file_read(src_path.child("file1")) == content1
        assert self.src_fs.file_read(src_path.child("subdir").child("file2")) == content2

        self.sut.copy_dir_to_dir(CopyDirectory(self.src_fs, src_path), CopyDirectory(self.dst_fs, dst_path))

        assert self.dst_fs.file_read(dst_path.child("file1")) == content1
        assert self.dst_fs.file_read(dst_path.child("subdir").child("file2")) == content2

    def test_copy_file_to_file(self) -> None:
        src_path: Path = Path("", "/some/file")
        dst_path: Path = Path("", "/another/file/name")
        content: bytes = b"random content"

        self.src_fs.file_write(src_path, content)

        self.sut.copy_file_to_file(CopyFile(self.src_fs, src_path), CopyFile(self.dst_fs, dst_path))

        assert self.dst_fs.file_read(dst_path) == content


class TestCopyHandler(TestCase):
    copier_default: GenericCopier
    sut: CopyHandler

    def setUp(self) -> None:
        self.copier_default = GenericCopier()
        self.sut = CopyHandler(self.copier_default)

    def test_copy_default(self) -> None:
        src: Any = mock.Mock(spec=CopyDirectory)
        dst: CopyDirectory = mock.Mock(spec=CopyDirectory)

        self.sut.copy(src, dst)

        src.copy.assert_called_once_with(dst, self.copier_default)

    def test_copy_policy(self) -> None:
        src: Any = mock.Mock(spec=CopyDirectory)
        dst: CopyDirectory = mock.Mock(spec=CopyDirectory)
        mock_copier: GenericCopier = mock.Mock(spec=GenericCopier)

        self.sut.set_copy_policy(src.fs, dst.fs, mock_copier)

        self.sut.copy(src, dst)

        src.copy.assert_called_once_with(dst, mock_copier)

    def test_copy_error(self) -> None:
        src: Any = mock.Mock(spec=CopyDirectory)
        dst: CopyDirectory = mock.Mock(spec=CopyDirectory)
        mock_copier: GenericCopier = mock.Mock(spec=GenericCopier)
        src.copy.side_effect = Exception()

        self.sut.set_copy_policy(src.fs, dst.fs, mock_copier)

        with self.assertRaises(CopyError):
            self.sut.copy(src, dst)

        src.copy.assert_called_once_with(dst, mock_copier)
