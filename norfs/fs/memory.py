import traceback

from collections import deque
from typing import (
    Dict,
    Iterable,
    List,
    Optional,
)

from norfs.fs.base import (
    BaseFileSystem,
    FSObjectPath,
    FSObjectType,
    FileSystemOperationError,
    NotAFileError,
    Path,
)
from norfs.permissions import Policy


class MemoryDirectory:
    _subdirs: Dict[str, 'MemoryDirectory']
    _files: Dict[str, 'MemoryFile']

    def __init__(self) -> None:
        self._subdirs = {}
        self._files = {}

    def list_dirs(self) -> List[str]:
        return list(self._subdirs.keys())

    def list_files(self) -> List[str]:
        return list(self._files.keys())

    def put_dir(self, name: str, dir_: 'MemoryDirectory') -> None:
        self._subdirs[name] = dir_

    def put_file(self, name: str, file_: 'MemoryFile') -> None:
        self._files[name] = file_

    def get_dir(self, name: str) -> 'MemoryDirectory':
        try:
            return self._subdirs[name]
        except KeyError:
            raise NotADirectoryError()

    def get_file(self, name: str) -> 'MemoryFile':
        try:
            return self._files[name]
        except KeyError:
            raise NotAFileError()

    def remove_dir(self, name: str) -> None:
        try:
            del self._subdirs[name]
        except KeyError:
            raise NotADirectoryError()

    def remove_file(self, name: str) -> None:
        try:
            del self._files[name]
        except KeyError:
            raise NotADirectoryError()


class MemoryFile:
    _contents: bytes

    def __init__(self, contents: bytes) -> None:
        self._contents = contents

    @property
    def contents(self) -> bytes:
        return self._contents


class MemoryFileSystem(BaseFileSystem):
    _root: MemoryDirectory
    _separator: str

    def __init__(self, root: MemoryDirectory, *, separator: str="/") -> None:
        self._root = root
        self._separator = separator

    def _get_dir(self, path: Path) -> MemoryDirectory:
        current_dir: MemoryDirectory = self._root
        for dir_name in path.tail:
            current_dir = current_dir.get_dir(dir_name)
        return current_dir

    # General operations
    def parse_path(self, path: str) -> Path:
        tail: List[str] = path.split(self._separator)
        return Path("", *tail)

    def path_exists(self, path: Path) -> bool:
        try:
            parent_dir: MemoryDirectory = self._get_dir(path.parent)
        except NotADirectoryError:
            return False
        else:
            return path.basename in (parent_dir.list_dirs() + parent_dir.list_files())

    def path_to_string(self, path: Path) -> str:
        return self._separator.join(path.tail)

    def path_to_uri(self, path: Path) -> str:
        return f"memory://{self.path_to_string(path)}"

    # File operations
    def file_read(self, path: Path) -> bytes:
        parent_dir: MemoryDirectory
        try:
            parent_dir = self._get_dir(path.parent)
            return parent_dir.get_file(path.basename).contents
        except (NotADirectoryError, NotAFileError):
            raise FileSystemOperationError(traceback.format_exc())

    def file_write(self, path: Path, content: bytes) -> None:
        parent_dir: MemoryDirectory = self._root
        dir_name: str
        new_dir: MemoryDirectory

        queue = deque(path.parent.tail)
        while queue:
            dir_name = queue.popleft()
            try:
                parent_dir = parent_dir.get_dir(dir_name)
            except NotADirectoryError:
                new_dir = MemoryDirectory()
                parent_dir.put_dir(dir_name, new_dir)
                parent_dir = new_dir
                break

        while queue:
            dir_name = queue.popleft()
            new_dir = MemoryDirectory()
            parent_dir.put_dir(dir_name, new_dir)
            parent_dir = new_dir

        parent_dir.put_file(path.basename, MemoryFile(content))

    def file_remove(self, path: Path) -> None:
        try:
            parent_dir: MemoryDirectory = self._get_dir(path.parent)
            parent_dir.remove_file(path.basename)
        except (NotADirectoryError, NotAFileError):
            raise FileSystemOperationError(traceback.format_exc())

    def file_set_perms(self, path: Path, policies: List[Policy]) -> None:
        """ Has no effect. MemoryFileSystem has no concept of permissions.
        """
        ...

    def file_set_properties(self, path: Path,
                            content_type: Optional[str] = None,
                            tags: Optional[Dict[str, str]] = None,
                            metadata: Optional[Dict[str, str]] = None) -> None:
        """ Has no effect.
        """
        ...

    # Directory operations
    def dir_list(self, path: Path) -> Iterable[FSObjectPath]:
        files: List[Path]
        dirs: List[Path]
        current_dir: MemoryDirectory
        try:
            current_dir = self._get_dir(path)
        except NotADirectoryError:
            pass
        else:
            for file_ in current_dir.list_files():
                yield FSObjectPath(FSObjectType.FILE, path.child(file_))
            for dir_ in current_dir.list_dirs():
                yield FSObjectPath(FSObjectType.DIR, path.child(dir_))

    def dir_remove(self, path: Path) -> None:
        try:
            current_dir: MemoryDirectory = self._get_dir(path.parent)
            current_dir.remove_dir(path.basename)
        except NotADirectoryError:
            raise FileSystemOperationError(traceback.format_exc())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(root={self._root})"
