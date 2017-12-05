import boto3

from tempfile import TemporaryDirectory
from typing import Any
from unittest import TestCase

from moto import mock_s3

from norfs.fs import Path
from norfs.fs.local import LocalFileSystem
from norfs.fs.s3 import S3FileSystem
from norfs.copy import CopyFile
from norfs.copy.s3 import (
    S3ToLocalCopier,
    S3ToS3Copier,
)

from tests.tools import (
    random_local_path,
    random_path,
    randstr,
)


@mock_s3
class TestS3ToS3Copier(TestCase):
    client: Any
    sut: S3ToS3Copier
    fs: S3FileSystem
    src_bucket_name: str
    dst_bucket_name: str

    def setUp(self) -> None:
        self.client = boto3.client("s3")
        self.sut = S3ToS3Copier(self.client)
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

    def test_copy_file_to_file(self) -> None:
        src_path: Path = random_path(self.src_bucket_name)
        dst_path: Path = random_path(self.dst_bucket_name)
        content: bytes = randstr().encode()

        self.fs.file_write(src_path, content)

        self.sut.copy_file_to_file(CopyFile(self.fs, src_path), CopyFile(self.fs, dst_path))

        assert self.fs.file_read(dst_path) == content


@mock_s3
class TestS3ToLocalCopier(TestCase):
    client: Any
    sut: S3ToLocalCopier
    src_fs: S3FileSystem
    dst_tmp_dir: TemporaryDirectory
    dst_fs: LocalFileSystem
    bucket_name: str

    def setUp(self) -> None:
        self.client = boto3.client("s3")
        self.sut = S3ToLocalCopier(self.client)
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
