from typing import (
    Any,
    List,
    cast,
)

from .fs import (
    BaseFileSystem,
    DirListResult,
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

    def __init__(self, filesystem: BaseFileSystem, path_str: str, copy_handler: CopyHandler, *,
                 _path: Path=None) -> None:
        self._copy_handler = copy_handler
        self._fs = filesystem
        self._path = _path or self._fs.parse_path(path_str)

    @property
    def path(self) -> str:
        return self._fs.path_to_string(self._path)

    @property
    def uri(self) -> str:
        return self._fs.path_to_uri(self._path)

    @property
    def name(self) -> str:
        return self._path.basename

    def is_file(self) -> bool:
        return False

    def is_dir(self) -> bool:
        return False

    def as_file(self) -> 'File':
        raise NotAFileError()

    def as_dir(self) -> 'Directory':
        raise NotADirectoryError()

    def exists(self) -> bool:
        return self._fs.path_exists(self._path)

    def remove(self) -> None:
        raise NotImplementedError()

    def parent(self) -> 'Directory':
        return Directory(self._fs, None, self._copy_handler, _path=self._path.parent)

    def copy(self, destination: 'BaseFileSystemObject') -> None:
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
        return True

    def as_dir(self) -> 'Directory':
        return self

    def list(self) -> List[BaseFileSystemObject]:
        contents: DirListResult = self._fs.dir_list(self._path)
        result: List[BaseFileSystemObject] = []
        for dir_path in contents.dirs:
            result.append(Directory(self._fs, None, self._copy_handler, _path=dir_path))
        for file_path in contents.files:
            result.append(File(self._fs, None, self._copy_handler, _path=file_path))
        for other_path in contents.others:
            result.append(BaseFileSystemObject(self._fs, None, self._copy_handler, _path=other_path))

        return result

    def subdir(self, path: str) -> 'Directory':
        return Directory(self._fs, None, self._copy_handler, _path=self._path.child(path))

    def file(self, path: str) -> 'File':
        return File(self._fs, None, self._copy_handler, _path=self._path.child(path))

    def remove(self) -> None:
        self._fs.dir_remove(self._path)

    def _copy_object(self) -> CopyFileSystemObject:
        return CopyDirectory(self._fs, self._path)


class File(BaseFileSystemObject):

    def is_file(self) -> bool:
        return True

    def as_file(self) -> 'File':
        return self

    def read(self) -> bytes:
        return self._fs.file_read(self._path)

    def write(self, content: bytes) -> None:
        self._fs.file_write(self._path, content)

    def remove(self) -> None:
        self._fs.file_remove(self._path)

    def _copy_object(self) -> CopyFileSystemObject:
        return CopyFile(self._fs, self._path)
