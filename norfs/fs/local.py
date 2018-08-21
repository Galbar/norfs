import os
import shutil
import traceback

from typing import List

from norfs.fs.base import (
    BaseFileSystem,
    DirListResult,
    FileSystemOperationError,
    Path,
)


class LocalFileSystem(BaseFileSystem):

    # General operations
    def parse_path(self, path: str) -> Path:
        abs_path: str = os.path.abspath(os.path.normpath(path))
        drive: str
        tail_str: str
        drive, tail_str = os.path.splitdrive(abs_path)
        tail: List[str] = tail_str.split(os.sep)
        return Path(drive, *tail)

    def path_exists(self, path: Path) -> bool:
        return os.path.exists(self.path_to_string(path))

    def path_to_string(self, path: Path) -> str:
        return os.path.join(path.drive, os.sep.join(path.tail))

    def path_to_uri(self, path: Path) -> str:
        return "file:///{}/{}".format(path.drive, os.path.join(*path.tail))

    # File operations
    def file_read(self, path: Path) -> bytes:
        try:
            with open(self.path_to_string(path), "rb") as f:
                return f.read()
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    def file_write(self, path: Path, content: bytes) -> None:
        try:
            parent_path: str = self.path_to_string(path.parent)
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
            with open(self.path_to_string(path), "wb") as f:
                f.write(content)
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    def file_remove(self, path: Path) -> None:
        try:
            os.remove(self.path_to_string(path))
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    # Directory operations
    def dir_list(self, path: Path) -> DirListResult:
        path_str: str = self.path_to_string(path)
        items: List[str]
        try:
            items = os.listdir(path_str)
        except FileNotFoundError:
            items = []
        files: List[Path] = []
        dirs: List[Path] = []
        others: List[Path] = []
        for item in items:
            full_path: str = os.path.join(path_str, item)
            item_path: Path = path.child(item)
            if os.path.isfile(full_path):
                files.append(item_path)
            elif os.path.isdir(full_path):
                dirs.append(item_path)
            else:
                others.append(item_path)

        return DirListResult(files, dirs, others)

    def dir_remove(self, path: Path) -> None:
        try:
            shutil.rmtree(self.path_to_string(path))
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())
