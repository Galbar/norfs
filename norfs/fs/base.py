from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Tuple,
    Optional,
)
from enum import Enum, auto

from norfs.permissions import Policy


class NotAFileError(Exception):
    pass


class FileSystemOperationError(Exception):
    pass


class Path:
    _drive: str
    _tail: Tuple[str, ...]

    def __init__(self, drive: str, *tail: str) -> None:
        self._drive = drive
        self._tail = tail

    @property
    def drive(self) -> str:
        return self._drive

    @property
    def tail(self) -> Tuple[str, ...]:
        return self._tail

    @property
    def basename(self) -> str:
        return self._tail[-1]

    @property
    def parent(self) -> 'Path':
        return Path(self._drive, *self._tail[:-1])

    def child(self, name: str) -> 'Path':
        return Path(self._drive, *self._tail, name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(drive={self._drive.__repr__()}, tail={self._tail})"

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Path):
            return self._drive == other.drive and self._tail == other.tail
        return False


class FSObjectType(Enum):
    FILE = auto()
    DIR = auto()
    OTHER = auto()


class FSObjectPath:
    _type: FSObjectType
    _path: Path

    def __init__(self, type: FSObjectType, path: Path) -> None:
        self._type = type
        self._path = path

    @property
    def type(self) -> FSObjectType:
        return self._type

    @property
    def path(self) -> Path:
        return self._path

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self._type}, path={self._path})"


class BaseFileSystem:
    ERROR_MESSAGE = "BaseFileSystem: operation not implemented"

    # General operations
    def parse_path(self, path: str) -> Path:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    def path_exists(self, path: Path) -> bool:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    def path_to_string(self, path: Path) -> str:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    def path_to_uri(self, path: Path) -> str:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    # File operations
    def file_read(self, path: Path) -> bytes:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    def file_write(self, path: Path, content: bytes) -> None:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    def file_remove(self, path: Path) -> None:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    def file_set_perms(self, path: Path, policies: List[Policy]) -> None:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    def file_set_properties(self, path: Path,
                            content_type: Optional[str] = None,
                            tags: Optional[Dict[str, str]] = None,
                            metadata: Optional[Dict[str, str]] = None) -> None:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    # Directory operations
    def dir_list(self, path: Path) -> Iterable[FSObjectPath]:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    def dir_remove(self, path: Path) -> None:
        raise FileSystemOperationError(self.ERROR_MESSAGE)

    # Other
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash(id(self))
