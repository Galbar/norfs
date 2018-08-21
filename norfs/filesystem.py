"""
:class:`norfs.filesystem.BaseFileSystemObject` represents any object in the filesystem. It is the most abstract
representation.

A :class:`norfs.filesystem.BaseFileSystemObject` exposes the following interface:
"""
from typing import (
    Any,
    List,
    Optional,
    cast,
)

from norfs.fs.base import (
    BaseFileSystem,
    DirListResult,
    FileSystemOperationError,
    NotAFileError,
    Path,
)
from norfs.copy.base import (
    CopyDirectory,
    CopyFile,
    CopyFileSystemObject,
)


class BaseFileSystemObject:
    _fs: BaseFileSystem
    _path: Path

    def __init__(self, filesystem: BaseFileSystem, path_str: Optional[str], *, _path: Optional[Path]=None) -> None:
        """ Constructor for BaseFileSystemObjects.
        One of `path_str` and `_path` **MUST** be present.
        """
        self._fs = filesystem
        self._path = _path or self._fs.parse_path(path_str or "")

    @property
    def path(self) -> str:
        """ The full, absolute, path of self in the file system. """
        return self._fs.path_to_string(self._path)

    @property
    def uri(self) -> str:
        """ The URI that points to self in the file system. """
        return self._fs.path_to_uri(self._path)

    @property
    def name(self) -> str:
        """ The name of self. """
        return self._path.basename

    def is_file(self) -> bool:
        """ Returns whether self is a File. """
        return False

    def is_dir(self) -> bool:
        """ Returns whether self is a Directory. """
        return False

    def as_file(self) -> 'File':
        """ Returns itself as a :class:`norfs.filesystem.File` instance or raises a
        :class:`norfs.fs.base.NotAFileError`.
        """
        raise NotAFileError()

    def as_dir(self) -> 'Directory':
        """ Returns itself as a Directory instance or raises a :class:`NotADirectoryError`. """
        raise NotADirectoryError()

    def exists(self) -> bool:
        """ Returns whether self exists in the file system. """
        return self._fs.path_exists(self._path)

    def remove(self) -> None:
        """ Tries to remove self from the file system.
        On failure it raises a :class:`norfs.fs.base.FileSystemOperationError`
        """
        raise FileSystemOperationError(f"Cannot remove {str(self)}")

    def parent(self) -> 'Directory':
        """ Return parent :class:`norfs.filesystem.Directory` of self. """
        return Directory(self._fs, None, _path=self._path.parent)

    def copy_object(self) -> CopyFileSystemObject:
        return CopyFileSystemObject(self._fs, self._path)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(fs={self._fs}, path={self.path})")

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            other_casted: 'BaseFileSystemObject' = cast(BaseFileSystemObject, other)
            return (self._path == other_casted._path and
                    self._fs == other_casted._fs)
        return False


class Directory(BaseFileSystemObject):

    def is_dir(self) -> bool:
        """ Returns whether self is a :class:`norfs.filesystem.Directory`. """
        return True

    def as_dir(self) -> 'Directory':
        """ Returns itself as a :class:`norfs.filesystem.Directory` instance or raises a :class:`NotADirectoryError`.
        """
        return self

    def list(self) -> List[BaseFileSystemObject]:
        """ Returns the contents of the :class:`norfs.filesystem.Directory` in the file system as a list of
        :class:`norfs.filesystem.BaseFileSystemObject` s.

        If the :class:`norfs.filesystem.Directory` does not exist the list will be empty.
        """
        contents: DirListResult = self._fs.dir_list(self._path)
        result: List[BaseFileSystemObject] = []
        for dir_path in contents.dirs:
            result.append(Directory(self._fs, None, _path=dir_path))
        for file_path in contents.files:
            result.append(File(self._fs, None, _path=file_path))
        for other_path in contents.others:
            result.append(BaseFileSystemObject(self._fs, None, _path=other_path))

        return result

    def remove(self) -> None:
        """ Tries to remove self from the file system.

        On failure it raises a :class:`norfs.fs.base.FileSystemOperationError`
        """
        self._fs.dir_remove(self._path)

    def subdir(self, path: str) -> 'Directory':
        """ Returns a :class:`norfs.filesystem.Directory` with its path as being the given path relative to the current
        directory.
        """
        return Directory(self._fs, None, _path=self._path.child(path))

    def file(self, path: str) -> 'File':
        """ Returns a :class:`norfs.filesystem.File` with its path as being the given `path` relative to the current
        directory.
        """
        return File(self._fs, None, _path=self._path.child(path))

    def copy_object(self) -> CopyFileSystemObject:
        return CopyDirectory(self._fs, self._path)


class File(BaseFileSystemObject):

    def is_file(self) -> bool:
        """ Returns whether self is a :class:`norfs.filesystem.File`. """
        return True

    def as_file(self) -> 'File':
        """ Returns itself as a :class:`norfs.filesystem.File` instance or raises a :class:`norfs.fs.base.NotAFileError`.
        """
        return self

    def remove(self) -> None:
        """ Tries to remove self from the file system.

        On failure it raises a :class:`norfs.fs.base.FileSystemOperationError`
        """
        self._fs.file_remove(self._path)

    def read(self) -> bytes:
        """ Returns the contents of the file.

        If it fails to read the file a :class:`norfs.fs.base.FileSystemOperationError` will be raised.
        """
        return self._fs.file_read(self._path)

    def write(self, content: bytes) -> None:
        """ Sets the contents of the file. If the parent directory does not exist it is created.

        If it fails to write the file a :class:`norfs.fs.base.FileSystemOperationError` will be raised.
        """
        self._fs.file_write(self._path, content)

    def copy_object(self) -> CopyFileSystemObject:
        return CopyFile(self._fs, self._path)
