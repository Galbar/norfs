import boto3

from tempfile import TemporaryDirectory
from typing import Any
from unittest import TestCase

from moto import mock_s3

from norfs.fs.base import Path
from norfs.fs.local import LocalFileSystem
from norfs.fs.s3 import S3FileSystem
from norfs.copy.base import CopyFile
from norfs.copy.local import (
    LocalToLocalCopyStrategy,
    LocalToS3CopyStrategy,
)

from tests.tools import (
    random_local_path,
    random_path,
    randstr,
)


class TestLocalToLocalCopyStrategy(TestCase):

    def setUp(self) -> None:
        self.sut: LocalToLocalCopyStrategy = LocalToLocalCopyStrategy()
        self.src_tmp_dir: TemporaryDirectory = TemporaryDirectory()
        self.dst_tmp_dir: TemporaryDirectory = TemporaryDirectory()
        self.fs: LocalFileSystem = LocalFileSystem()

    def tearDown(self) -> None:
        self.src_tmp_dir.cleanup()
        self.dst_tmp_dir.cleanup()

    def test_copy_file_to_file(self) -> None:
        src_path: Path = random_local_path(root=self.src_tmp_dir.name)[0]
        dst_path: Path = random_local_path(root=self.dst_tmp_dir.name)[0]
        content: bytes = randstr().encode()

        self.fs.file_write(src_path, content)

        self.sut.copy_file_to_file(CopyFile(self.fs, src_path), CopyFile(self.fs, dst_path))

        assert self.fs.file_read(dst_path) == content


@mock_s3
class TestLocalToS3CopyStrategy(TestCase):
    client: Any
    sut: LocalToS3CopyStrategy
    src_tmp_dir: TemporaryDirectory
    src_fs: LocalFileSystem
    dst_fs: S3FileSystem
    bucket_name: str

    def setUp(self) -> None:
        self.client = boto3.client("s3")
        self.sut = LocalToS3CopyStrategy(self.client)
        self.src_tmp_dir = TemporaryDirectory()
        self.src_fs = LocalFileSystem()
        self.dst_fs = S3FileSystem(self.client)
        self.bucket_name = randstr()
        self.client.create_bucket(Bucket=self.bucket_name)

    def tearDown(self) -> None:
        self.src_tmp_dir.cleanup()
        boto3.resource("s3").Bucket(self.bucket_name).objects.all().delete()
        self.client.delete_bucket(Bucket=self.bucket_name)

    def test_copy_file_to_file(self) -> None:
        src_path: Path = random_local_path(root=self.src_tmp_dir.name)[0]
        dst_path: Path = random_path(self.bucket_name)
        content: bytes = randstr().encode()

        self.src_fs.file_write(src_path, content)

        self.sut.copy_file_to_file(CopyFile(self.src_fs, src_path), CopyFile(self.dst_fs, dst_path))

        assert self.dst_fs.file_read(dst_path) == content
