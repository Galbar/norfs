import os
import shutil
import stat
import traceback

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
    Path,
)
from norfs.permissions import Policy, Perm, Scope


_local_fs_perms = {
    (Scope.OWNER, Perm.READ): stat.S_IRUSR,
    (Scope.OWNER, Perm.WRITE): stat.S_IWUSR,
    (Scope.OWNER, Perm.EXECUTE): stat.S_IXUSR,
    (Scope.GROUP, Perm.READ): stat.S_IRGRP,
    (Scope.GROUP, Perm.WRITE): stat.S_IWGRP,
    (Scope.GROUP, Perm.EXECUTE): stat.S_IXGRP,
    (Scope.OTHERS, Perm.READ): stat.S_IROTH,
    (Scope.OTHERS, Perm.WRITE): stat.S_IWOTH,
    (Scope.OTHERS, Perm.EXECUTE): stat.S_IXOTH,
}


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

    def file_set_perms(self, path: Path, policies: List[Policy]) -> None:
        """ Set permissions for a file.

        This works as expected on a unix file system. `Perm.WRITE_PERMS` and `Perm.READ_PERMS` are ignored.
        """
        mode = 0
        for policy in policies:
            for perm in policy.perms:
                mode |= _local_fs_perms.get((policy.scope, perm), 0)
        os.chmod(self.path_to_string(path), mode)

    def file_set_properties(self, path: Path,
                            content_type: Optional[str] = None,
                            tags: Optional[Dict[str, str]] = None,
                            metadata: Optional[Dict[str, str]] = None) -> None:
        """ Has no effect.
        """
        ...

    # Directory operations
    def dir_list(self, path: Path) -> Iterable[FSObjectPath]:
        path_str: str = self.path_to_string(path)
        items: List[str]
        try:
            items = os.listdir(path_str)
        except FileNotFoundError:
            return

        for item in items:
            full_path: str = os.path.join(path_str, item)
            item_path: Path = path.child(item)
            if os.path.isfile(full_path):
                yield FSObjectPath(FSObjectType.FILE, item_path)
            elif os.path.isdir(full_path):
                yield FSObjectPath(FSObjectType.DIR, item_path)
            else:
                yield FSObjectPath(FSObjectType.OTHER, item_path)

    def dir_remove(self, path: Path) -> None:
        try:
            shutil.rmtree(self.path_to_string(path))
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())
