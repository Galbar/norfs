from norfs.filesystem import (
    BaseFileSystemObject,
    Directory,
    File,
)
from norfs.fs.base import BaseFileSystem
from norfs.copy.base import Copier


class FileSystemClient:
    """
    :class:`norfs.client.FileSystemClient` provides a way to access the file system objects of a given file system. It
    is a handy class that provides easy access to :class:`norfs.filesystem.File` and
    :class:`norfs.filesystem.Directory` instances. It is usually obtained using :mod:`norfs.helpers`::

        import norfs.helpers

        local_fs_client = norfs.helpers.local()

        memory_fs_client = norfs.helpers.memory()

        import boto3
        s3_fs_client = norfs.helpers.s3(s3_client=boto3.client('s3'))

    A :class:`norfs.client.FileSystemClient` exposes the following interface:
    """
    _fs: BaseFileSystem

    def __init__(self, fs: BaseFileSystem) -> None:
        """ Constructor for :class:`norfs.client.FileSystemClient` s. """
        self._fs = fs

    @property
    def fs(self) -> BaseFileSystem:
        """ The :class:`norfs.filesystem.BaseFileSystemObject` the client is managing. """
        return self._fs

    def dir(self, path: str) -> Directory:
        """ Returns a :class:`norfs.filesystem.Directory` instance for the given path in the managed file system. """
        return Directory(self.fs, path)

    def file(self, path: str) -> File:
        """ Returns a :class:`norfs.filesystem.File` instance for the given path in the managed file system. """
        return File(self.fs, path)


class CopyClient:
    """
    :class:`norfs.client.CopyClient` provides a unified simple copy API for any :class:`norfs.filesystem.File` or
    :class:`norfs.filesystem.Directory` from any file system.  It is usually accessed by using
    :func:`norfs.helpers.get_copy_client`::

        import norfs.helpers

        local = norfs.helpers.local() cp_local_only = norfs.helpers.get_copy_client(local)

        cp_local_only.copy(local.file('source_file.txt'), local.file('target_file.txt'))


        memory = norfs.helpers.memory()

        import boto3 s3 = norfs.helpers.s3(s3_client=boto3.client('s3'))

        cp_for_all = norfs.helpers.get_copy_client(local, s3, memory)

        cp_for_all.copy(s3.file('myBucket/source_file.txt'), local.file('target_file.txt'))

    :func:`norfs.helpers.get_copy_client` returns a :class:`norfs.client.CopyClient` instance configured with copy
    strategies for each of the file system clients passed.

    A :class:`norfs.copy.base.Copier` can have copy policies set for a pair of source and destination file systems to
    implement a better strategy of copying between them than read source and write destination.
    :func:`norfs.helpers.get_copy_client` helps you by setting these for you.

    A :class:`norfs.client.CopyClient` exposes the following interface:
    """
    _copier: Copier

    def __init__(self, copier: Copier) -> None:
        """ Constructor for CopyClients. """
        self._copier = copier

    @property
    def copier(self) -> Copier:
        """ The :class:`norfs.copy.base.Copier` instance managed by the client. """
        return self._copier

    def copy(self, src: BaseFileSystemObject, dst: BaseFileSystemObject) -> None:
        """ Copies ``src`` to ``dst``, no mater the file systems they are on. ``src`` and ``dst`` can by both
        :class:`norfs.filesystem.File` or :class:`norfs.filesystem.Directory`.  The only operation not supported is
        copying from a :class:`norfs.filesystem.Directory` into a :class:`norfs.filesystem.File` as it does not make
        sense.

        If source is a :class:`norfs.filesystem.Directory` and destination is a :class:`norfs.filesystem.File` it raises
        a :class:`TypeError`.

        On copy failure it raises a :class:`norfs.fs.base.FileSystemOperationError`.
        """
        self._copier.copy(src.copy_object(), dst.copy_object())
