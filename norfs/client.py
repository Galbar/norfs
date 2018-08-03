from norfs.filesystem import (
    BaseFileSystemObject,
    Directory,
    File,
)
from norfs.fs.base import BaseFileSystem
from norfs.copy.base import Copier


class FileSystemClient:
    _fs: BaseFileSystem

    def __init__(self, fs: BaseFileSystem) -> None:
        self._fs = fs

    @property
    def fs(self) -> BaseFileSystem:
        return self._fs

    def dir(self, path: str) -> Directory:
        return Directory(self.fs, path)

    def file(self, path: str) -> File:
        return File(self.fs, path)


class CopyClient:
    _copier: Copier

    def __init__(self, copier: Copier) -> None:
        self._copier = copier

    @property
    def copier(self) -> Copier:
        return self._copier

    def copy(self, src: BaseFileSystemObject, dst: BaseFileSystemObject) -> None:
        self._copier.copy(src.copy_object(), dst.copy_object())
