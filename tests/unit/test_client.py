from unittest import (
    TestCase,
    mock,
)

from norfs import client
from norfs import fs
from norfs import copy
from norfs import filesystem


class TestFileSystemClient(TestCase):

    def setUp(self) -> None:
        self.fs = mock.Mock(spec=fs.base.BaseFileSystem)
        self.sut = client.FileSystemClient(self.fs)

    def test_fs(self) -> None:
        assert self.sut.fs is self.fs

    def test_dir(self) -> None:
        result = self.sut.dir("some/path")
        assert result._fs is self.fs
        assert result._path == self.fs.parse_path.return_value
        self.fs.parse_path.assert_called_once_with("some/path")

    def test_file(self) -> None:
        result = self.sut.dir("some/path")
        assert result._fs is self.fs
        assert result._path == self.fs.parse_path.return_value
        self.fs.parse_path.assert_called_once_with("some/path")


class TestCopyClient(TestCase):

    def setUp(self) -> None:
        self.copier = mock.Mock(spec=copy.base.Copier)
        self.sut = client.CopyClient(self.copier)

    def test_copier(self) -> None:
        assert self.sut.copier is self.copier

    def test_copy(self) -> None:
        copy_src = mock.Mock(spec=copy.base.CopyFileSystemObject)
        src = mock.Mock(spec=filesystem.BaseFileSystemObject)
        src.copy_object.return_value = copy_src
        copy_dst = mock.Mock(spec=copy.base.CopyFileSystemObject)
        dst = mock.Mock(spec=filesystem.BaseFileSystemObject)
        dst.copy_object.return_value = copy_dst

        self.sut.copy(src, dst)

        self.copier.copy.assert_called_once_with(copy_src, copy_dst)
