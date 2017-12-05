import traceback

from typing import (
    Any,
    Dict,
    Tuple,
    cast,
)

from ..fs import (
    BaseFileSystem,
    DirListResult,
    Path,
)


class CopyError(Exception):
    pass


class CopyFileSystemObject:
    _fs: BaseFileSystem
    _path: Path

    def __init__(self, fs: BaseFileSystem, path: Path) -> None:
        self._fs = fs
        self._path = path

    @property
    def fs(self) -> BaseFileSystem:
        return self._fs

    @property
    def path(self) -> Path:
        return self._path

    def copy(self, dst: 'CopyFileSystemObject', copier: 'GenericCopier') -> None:
        raise TypeError("Cannot copy from filesystem object that is not file or directory")

    def copy_from_file(self, src: 'CopyFile', copier: 'GenericCopier') -> None:
        raise TypeError("Cannot copy to filesystem object that is not file or directory")

    def copy_from_dir(self, src: 'CopyDirectory', copier: 'GenericCopier') -> None:
        raise TypeError("Cannot copy to filesystem object that is not file or directory")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            other_casted: 'CopyFileSystemObject' = cast(CopyFileSystemObject, other)
            return self._fs == other_casted._fs and self._path == other_casted._path

        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(fs={self._fs}, path={self._path})"


class CopyFile(CopyFileSystemObject):

    def copy(self, dst: 'CopyFileSystemObject', copier: 'GenericCopier') -> None:
        dst.copy_from_file(self, copier)

    def copy_from_file(self, src: 'CopyFile', copier: 'GenericCopier') -> None:
        copier.copy_file_to_file(src, self)

    def copy_from_dir(self, src: 'CopyDirectory', copier: 'GenericCopier') -> None:
        raise TypeError("Cannot copy Directory into a File.")


class CopyDirectory(CopyFileSystemObject):

    def file(self, suffix: str) -> 'CopyFile':
        return CopyFile(self._fs, self._path.child(suffix))

    def subdir(self, suffix: str) -> 'CopyDirectory':
        return CopyDirectory(self._fs, self._path.child(suffix))

    def copy(self, dst: 'CopyFileSystemObject', copier: 'GenericCopier') -> None:
        dst.copy_from_dir(self, copier)

    def copy_from_file(self, src: 'CopyFile', copier: 'GenericCopier') -> None:
        copier.copy_file_to_file(src, self.file(self.path.basename))

    def copy_from_dir(self, src: 'CopyDirectory', copier: 'GenericCopier') -> None:
        copier.copy_dir_to_dir(src, self)


class GenericCopier:

    def copy_dir_to_dir(self, src: CopyDirectory, dst: CopyDirectory) -> None:
        contents: DirListResult = src.fs.dir_list(src.path)

        for file_ in contents.files:
            src_child_file: CopyFile = src.file(file_.basename)
            dst_child_file: CopyFile = dst.file(file_.basename)
            self.copy_file_to_file(src_child_file, dst_child_file)

        for dir_ in contents.dirs:
            src_child_dir: CopyDirectory = src.subdir(dir_.basename)
            dst_child_dir: CopyDirectory = dst.subdir(dir_.basename)
            self.copy_dir_to_dir(src_child_dir, dst_child_dir)

    def copy_file_to_file(self, src: CopyFile, dst: CopyFile) -> None:
        dst.fs.file_write(dst.path, src.fs.file_read(src.path))


class CopyHandler:
    _copiers: Dict[Tuple[BaseFileSystem, BaseFileSystem], GenericCopier]
    _default: GenericCopier

    def __init__(self, default_copier: GenericCopier) -> None:
        self._copiers = {}
        self._default = default_copier

    def set_copy_policy(self, src_fs: BaseFileSystem, dst_fs: BaseFileSystem, copier: GenericCopier) -> None:
        self._copiers[(src_fs, dst_fs)] = copier

    def copy(self, src: CopyFileSystemObject, dst: CopyFileSystemObject) -> None:
        copier: GenericCopier = self._copiers.get((src.fs, dst.fs), self._default)

        try:
            src.copy(dst, copier)
        except Exception:
            raise CopyError(traceback.format_exc())
