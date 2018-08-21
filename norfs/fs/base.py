from typing import (
    Any,
    List,
    Tuple,
)


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


class DirListResult:
    _files: List[Path]
    _dirs: List[Path]
    _others: List[Path]

    def __init__(self, files: List[Path], dirs: List[Path], others: List[Path]) -> None:
        self._files = files
        self._dirs = dirs
        self._others = others

    @property
    def files(self) -> List[Path]:
        return self._files

    @property
    def dirs(self) -> List[Path]:
        return self._dirs

    @property
    def others(self) -> List[Path]:
        return self._others

    def __eq__(self, other: Any) -> bool:
        if other is self:
            return True
        if not isinstance(other, DirListResult):
            return False
        if set(other.files) != set(self.files):
            return False
        if set(other.dirs) != set(self.dirs):
            return False
        if set(other.others) != set(self.others):
            return False
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(files={self._files}, dirs={self._dirs}, others={self._others})"


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

    # Directory operations
    def dir_list(self, path: Path) -> DirListResult:
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
