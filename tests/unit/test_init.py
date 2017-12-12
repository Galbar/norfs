import os

from typing import (
    Any,
    Dict,
)
from unittest import (
    TestCase,
    mock,
)

import norfs
from norfs.copy import (
    CopyHandler,
)
from norfs.filesystem import (
    Directory,
    File,
)
from norfs.fs.local import LocalFileSystem
from norfs.fs.s3 import S3FileSystem
from norfs.fs.memory import (
    MemoryFileSystem,
)

from tests.tools import randstr


class TestNorfs(TestCase):
    initial_config: Dict[str, Any]

    def setUp(self) -> None:
        self.initial_config = norfs._config.copy()

    def tearDown(self) -> None:
        norfs._config = self.initial_config
        norfs._copy_handler = None
        norfs._local_fs = None
        norfs._s3_fs = None
        norfs._memory_fs = None

    def test_get_copy_handler(self) -> None:
        copy_handler: CopyHandler = norfs.get_copy_handler()

        assert norfs.get_copy_handler() is copy_handler

    def test_get_local_fs(self) -> None:
        localfs: LocalFileSystem = norfs.get_local_fs()

        assert norfs.get_local_fs() is localfs

    def test_localdir(self) -> None:
        path: str = os.getcwd()
        ldir: Directory = norfs.localdir(path)

        assert str(ldir) == f"Directory(fs=LocalFileSystem(), path={path}, copy_handler={norfs.get_copy_handler()})"

    def test_localfile(self) -> None:
        path: str = os.getcwd()
        lfile: File = norfs.localfile(path)

        assert str(lfile) == f"File(fs=LocalFileSystem(), path={path}, copy_handler={norfs.get_copy_handler()})"

    def test_get_s3_fs_not_configured_raises_exception(self) -> None:
        with self.assertRaises(ValueError):
            norfs.get_s3_fs()

    def test_get_s3_fs_with_s3_client(self) -> None:
        s3_client: Any = mock.Mock()
        norfs.configure(s3_client=s3_client)
        s3fs: S3FileSystem = norfs.get_s3_fs()
        assert norfs.get_s3_fs() is s3fs

    def test_s3dir(self) -> None:
        s3_client: Any = mock.Mock()
        norfs.configure(s3_client=s3_client, s3_separator=randstr(charset="!@#$%^&*()/"))

        bucket: str = randstr()
        path: str = randstr()
        s3dir: Directory = norfs.s3dir(bucket, path)

        expected = f"Directory(fs={norfs.get_s3_fs()}, path={bucket}/{path}, copy_handler={norfs.get_copy_handler()})"
        assert str(s3dir) == expected

        bucket = randstr()
        path = randstr()
        s3dir = norfs.s3dir("/".join((bucket, path)))

        expected = f"Directory(fs={norfs.get_s3_fs()}, path={bucket}/{path}, copy_handler={norfs.get_copy_handler()})"
        assert str(s3dir) == expected

    def test_s3file(self) -> None:
        s3_client: Any = mock.Mock()
        norfs.configure(s3_client=s3_client, s3_separator=randstr(charset="!@#$%^&*()/"))

        bucket: str = randstr()
        path: str = randstr()
        s3file: File = norfs.s3file(bucket, path)

        expected = f"File(fs={norfs.get_s3_fs()}, path={bucket}/{path}, copy_handler={norfs.get_copy_handler()})"
        assert str(s3file) == expected

        bucket = randstr()
        path = randstr()
        s3file = norfs.s3file("/".join((bucket, path)))

        expected = f"File(fs={norfs.get_s3_fs()}, path={bucket}/{path}, copy_handler={norfs.get_copy_handler()})"
        assert str(s3file) == expected

    def test_get_memory_fs(self) -> None:
        memfs: MemoryFileSystem = norfs.get_memory_fs()

        assert memfs is norfs.get_memory_fs()

    def test_memorydir(self) -> None:
        path: str = randstr()
        memdir: Directory = norfs.memorydir(path)

        expected_str = f"Directory(fs={norfs.get_memory_fs()}, path={path}, copy_handler={norfs.get_copy_handler()})"
        assert str(memdir) == expected_str

        path = randstr()
        memdir = norfs.memorydir(path)

        expected_str = f"Directory(fs={norfs.get_memory_fs()}, path={path}, copy_handler={norfs.get_copy_handler()})"
        assert str(memdir) == expected_str

    def test_memoryfile(self) -> None:
        path: str = randstr()
        memfile: File = norfs.memoryfile(path)

        expected_str = f"File(fs={norfs.get_memory_fs()}, path={path}, copy_handler={norfs.get_copy_handler()})"
        assert str(memfile) == expected_str

        path = randstr()
        memfile = norfs.memoryfile(path)

        expected_str = f"File(fs={norfs.get_memory_fs()}, path={path}, copy_handler={norfs.get_copy_handler()})"
        assert str(memfile) == expected_str
