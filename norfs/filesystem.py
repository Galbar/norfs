from typing import (
    Any,
    List,
    Optional,
    cast,
)

from .fs import (
    BaseFileSystem,
    DirListResult,
    FileSystemOperationError,
    NotAFileError,
    Path,
)
from .copy import CopyHandler
from .copy import (
    CopyDirectory,
    CopyFile,
    CopyFileSystemObject,
)


class BaseFileSystemObject:
    _copy_handler: CopyHandler
    _fs: BaseFileSystem
    _path: Path

    def __init__(self, filesystem: BaseFileSystem, path_str: Optional[str], copy_handler: CopyHandler, *,
                 _path: Optional[Path]=None) -> None:
        """ Constructor for BaseFileSystemObjects.
        One of `path_str` and `_path` **MUST** be present.
        """
        self._copy_handler = copy_handler
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
        """ Returns wether self is a File. """
        return False

    def is_dir(self) -> bool:
        """ Returns wether self is a Directory. """
        return False

    def as_file(self) -> 'File':
        """ Returns itself as a File instance or raises a NotAFileError. """
        raise NotAFileError()

    def as_dir(self) -> 'Directory':
        """ Returns itself as a Directory instance or raises a NotADirectoryError. """
        raise NotADirectoryError()

    def exists(self) -> bool:
        """ Returns whether self exists in the file system. """
        return self._fs.path_exists(self._path)

    def remove(self) -> None:
        """ Tries to remove self from the file system.
        On failure it raises a FileSystemOperationError
        """
        raise FileSystemOperationError(f"Cannot remove {str(self)}")

    def parent(self) -> 'Directory':
        """ Return parent Directory of self. """
        return Directory(self._fs, None, self._copy_handler, _path=self._path.parent)

    def copy(self, destination: 'BaseFileSystemObject') -> None:
        """ Copy this to `destination`. """
        self._copy_handler.copy(self._copy_object(), destination._copy_object())

    def _copy_object(self) -> CopyFileSystemObject:
        return CopyFileSystemObject(self._fs, self._path)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(fs={self._fs}, path={self.path}, copy_handler={self._copy_handler})")

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            other_casted: 'BaseFileSystemObject' = cast(BaseFileSystemObject, other)
            return (self._path == other_casted._path and
                    self._fs == other_casted._fs and
                    self._copy_handler == other_casted._copy_handler)
        return False


class Directory(BaseFileSystemObject):

    def is_dir(self) -> bool:
        """ Returns wether self is a Directory. """
        return True

    def as_dir(self) -> 'Directory':
        """ Returns itself as a Directory instance or raises a NotADirectoryError. """
        return self

    def list(self) -> List[BaseFileSystemObject]:
        """ Returns the contents of the Directory in the file system as a list of BaseFileSystemObjects.

        If the Directory does not exist the list will be empty.
        """
        contents: DirListResult = self._fs.dir_list(self._path)
        result: List[BaseFileSystemObject] = []
        for dir_path in contents.dirs:
            result.append(Directory(self._fs, None, self._copy_handler, _path=dir_path))
        for file_path in contents.files:
            result.append(File(self._fs, None, self._copy_handler, _path=file_path))
        for other_path in contents.others:
            result.append(BaseFileSystemObject(self._fs, None, self._copy_handler, _path=other_path))

        return result

    def remove(self) -> None:
        """ Tries to remove self from the file system.

        On failure it raises a FileSystemOperationError
        """
        self._fs.dir_remove(self._path)

    def subdir(self, path: str) -> 'Directory':
        """ Returns a Directory with its path as being the given path relative to the current Directory. """
        return Directory(self._fs, None, self._copy_handler, _path=self._path.child(path))

    def file(self, path: str) -> 'File':
        """ Returns a File with its path as being the given `path` relative to the current Directory. """
        return File(self._fs, None, self._copy_handler, _path=self._path.child(path))

    def _copy_object(self) -> CopyFileSystemObject:
        return CopyDirectory(self._fs, self._path)


class File(BaseFileSystemObject):

    def is_file(self) -> bool:
        """ Returns wether self is a File. """
        return True

    def as_file(self) -> 'File':
        """ Returns itself as a File instance or raises a NotAFileError. """
        return self

    def remove(self) -> None:
        """ Tries to remove self from the file system.

        On failure it raises a FileSystemOperationError
        """
        self._fs.file_remove(self._path)

    def read(self) -> bytes:
        """ Returns the contents of the File.

        If it fails to read the file a FileSystemOperationError will be raised.
        """
        return self._fs.file_read(self._path)

    def write(self, content: bytes) -> None:
        """ Sets the contents of the File. If the parent directory does not exist it is created.

        If it fails to read the file a FileSystemOperationError will be raised.
        """
        self._fs.file_write(self._path, content)

    def _copy_object(self) -> CopyFileSystemObject:
        return CopyFile(self._fs, self._path)
