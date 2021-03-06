import boto3

from tempfile import TemporaryDirectory
from typing import (
    Any,
    List,
    Tuple,
)

from unittest import TestCase

from moto import mock_s3

from norfs.fs.base import Path
from norfs.fs.local import LocalFileSystem
from norfs.fs.s3 import S3FileSystem
from norfs.copy.base import (
    CopyDirectory,
    CopyFile,
)
from norfs.copy.s3 import (
    S3ToLocalCopyStrategy,
    S3ToS3CopyStrategy,
)

from tests.tools import (
    random_local_path,
    random_path,
    randstr,
)


@mock_s3
class TestS3ToS3CopyStrategy(TestCase):
    client: Any
    sut: S3ToS3CopyStrategy
    fs: S3FileSystem
    src_bucket_name: str
    dst_bucket_name: str

    def setUp(self) -> None:
        self.client = boto3.client("s3")
        self.sut = S3ToS3CopyStrategy(self.client)
        self.fs = S3FileSystem(self.client)
        self.src_bucket_name = randstr()
        self.dst_bucket_name = randstr()
        self.client.create_bucket(Bucket=self.src_bucket_name)
        self.client.create_bucket(Bucket=self.dst_bucket_name)

    def tearDown(self) -> None:
        boto3.resource("s3").Bucket(self.src_bucket_name).objects.all().delete()
        self.client.delete_bucket(Bucket=self.src_bucket_name)
        boto3.resource("s3").Bucket(self.dst_bucket_name).objects.all().delete()
        self.client.delete_bucket(Bucket=self.dst_bucket_name)

    def test_copy_dir_to_dir(self) -> None:
        src_path: Path = random_path(self.src_bucket_name)
        dst_path: Path = random_path(self.dst_bucket_name)
        content: bytes = randstr().encode()

        scenario: List[Tuple[Path, bytes]] = [(random_path(), randstr().encode()) for _ in range(1100)]

        for path, content in scenario:
            self.fs.file_write(Path(src_path.drive, *src_path.tail, *path.tail), content)

        self.sut.copy_dir_to_dir(CopyDirectory(self.fs, src_path), CopyDirectory(self.fs, dst_path))

        for path, content in scenario:
            assert self.fs.file_read(Path(dst_path.drive, *dst_path.tail, *path.tail)) == content

    def test_copy_file_to_file(self) -> None:
        src_path: Path = random_path(self.src_bucket_name)
        dst_path: Path = random_path(self.dst_bucket_name)
        content: bytes = randstr().encode()

        self.fs.file_write(src_path, content)

        self.sut.copy_file_to_file(CopyFile(self.fs, src_path), CopyFile(self.fs, dst_path))

        assert self.fs.file_read(dst_path) == content


@mock_s3
class TestS3ToLocalCopyStrategy(TestCase):
    client: Any
    sut: S3ToLocalCopyStrategy
    src_fs: S3FileSystem
    dst_tmp_dir: TemporaryDirectory
    dst_fs: LocalFileSystem
    bucket_name: str

    def setUp(self) -> None:
        self.client = boto3.client("s3")
        self.sut = S3ToLocalCopyStrategy(self.client)
        self.src_fs = S3FileSystem(self.client)
        self.dst_tmp_dir = TemporaryDirectory()
        self.dst_fs = LocalFileSystem()
        self.bucket_name = randstr()
        self.client.create_bucket(Bucket=self.bucket_name)

    def tearDown(self) -> None:
        self.dst_tmp_dir.cleanup()
        boto3.resource("s3").Bucket(self.bucket_name).objects.all().delete()
        self.client.delete_bucket(Bucket=self.bucket_name)

    def test_copy_file_to_file(self) -> None:
        src_path: Path = random_path(self.bucket_name)
        dst_path: Path = random_local_path(root=self.dst_tmp_dir.name)[0]
        content: bytes = randstr().encode()

        self.src_fs.file_write(src_path, content)

        self.sut.copy_file_to_file(CopyFile(self.src_fs, src_path), CopyFile(self.dst_fs, dst_path))

        assert self.dst_fs.file_read(dst_path) == content

    def test_copy_dir_to_dir(self) -> None:
        src_path: Path = random_path(self.bucket_name)
        dst_path: Path = random_local_path(root=self.dst_tmp_dir.name)[0]
        content: bytes = randstr().encode()

        scenario: List[Tuple[Path, bytes]] = [(random_path(), randstr().encode()) for _ in range(1100)]

        for path, content in scenario:
            self.src_fs.file_write(Path(src_path.drive, *src_path.tail, *path.tail), content)

        self.sut.copy_dir_to_dir(CopyDirectory(self.src_fs, src_path), CopyDirectory(self.dst_fs, dst_path))

        for path, content in scenario:
            assert self.dst_fs.file_read(Path(dst_path.drive, *dst_path.tail, *path.tail)) == content
