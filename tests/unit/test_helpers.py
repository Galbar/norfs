from unittest import (
    TestCase,
    mock,
)

from norfs import helpers
from norfs.fs.base import Path
from norfs.fs.local import LocalFileSystem
from norfs.fs.memory import MemoryFileSystem
from norfs.fs.s3 import S3FileSystem
from norfs import copy


class TestHelpers(TestCase):

    def test_local_returns_fs_client_with_local_fs(self) -> None:
        actual = helpers.local()
        assert type(actual.fs) is LocalFileSystem
        assert actual != helpers.local()

    def test_memory_returns_fs_client_with_memory_fs(self) -> None:
        actual = helpers.memory()
        assert type(actual.fs) is MemoryFileSystem
        assert actual.fs.path_to_string(Path("", "foo", "bar")) == "foo/bar"
        assert actual != helpers.memory()

    def test_memory_returns_fs_client_with_memory_fs_with_set_separator(self) -> None:
        actual = helpers.memory(separator="@")
        assert type(actual.fs) is MemoryFileSystem
        assert actual.fs.path_to_string(Path("", "foo", "bar")) == "foo@bar"

    def test_s3_returns_fs_client_with_s3_fs(self) -> None:
        actual = helpers.s3(None)
        assert type(actual.fs) is S3FileSystem
        assert actual.fs.path_to_uri(Path("bucket", "foo", "bar")) == "s3://bucket/foo/bar"
        assert actual != helpers.s3(None)

    def test_s3_returns_fs_client_with_s3_fs_with_set_separator_and_protocol(self) -> None:
        actual = helpers.s3(None, uri_protocol="s3a", separator="@")
        assert type(actual.fs) is S3FileSystem
        assert actual.fs.path_to_uri(Path("bucket", "foo", "bar")) == "s3a://bucket/foo@bar"

    def test_get_copier_returns_new_copy_client_instance(self) -> None:
        assert helpers.get_copy_client() is not helpers.get_copy_client()

    def test_get_copier_sets_copy_strategy_for_one_local_filesystem_client(self) -> None:
        local = helpers.local()
        copy_client = helpers.get_copy_client(local)
        assert type(copy_client.copier._copy_strategies[(local.fs, local.fs)]) is copy.local.LocalToLocalCopyStrategy

    def test_get_copier_sets_copy_strategy_for_multiple_local_filesystem_clients(self) -> None:
        local1 = helpers.local()
        local2 = helpers.local()
        copy_client = helpers.get_copy_client(local1, local2)
        assert type(copy_client.copier._copy_strategies[(local1.fs, local1.fs)]) is copy.local.LocalToLocalCopyStrategy
        assert type(copy_client.copier._copy_strategies[(local1.fs, local2.fs)]) is copy.local.LocalToLocalCopyStrategy
        assert type(copy_client.copier._copy_strategies[(local2.fs, local1.fs)]) is copy.local.LocalToLocalCopyStrategy
        assert type(copy_client.copier._copy_strategies[(local2.fs, local2.fs)]) is copy.local.LocalToLocalCopyStrategy

    def test_get_copier_sets_copy_strategy_for_one_s3_filesystem_client(self) -> None:
        s3 = helpers.s3(mock.Mock())
        copy_client = helpers.get_copy_client(s3)
        assert type(copy_client.copier._copy_strategies[(s3.fs, s3.fs)]) is copy.s3.S3ToS3CopyStrategy

    def test_get_copier_sets_copy_strategy_for_multiple_s3_filesystem_client_with_same_boto_s3_client(self) -> None:
        boto_s3_client = mock.Mock()
        s3_1 = helpers.s3(boto_s3_client)
        s3_2 = helpers.s3(boto_s3_client)
        copy_client = helpers.get_copy_client(s3_1, s3_2)
        assert type(copy_client.copier._copy_strategies[(s3_1.fs, s3_1.fs)]) is copy.s3.S3ToS3CopyStrategy
        assert type(copy_client.copier._copy_strategies[(s3_1.fs, s3_2.fs)]) is copy.s3.S3ToS3CopyStrategy
        assert type(copy_client.copier._copy_strategies[(s3_2.fs, s3_1.fs)]) is copy.s3.S3ToS3CopyStrategy
        assert type(copy_client.copier._copy_strategies[(s3_2.fs, s3_2.fs)]) is copy.s3.S3ToS3CopyStrategy

    def test_get_copier_sets_copy_strategy_for_multiple_s3_filesystem_client_with_different_boto_s3_client(
        self
    ) -> None:
        s3_1 = helpers.s3(mock.Mock())
        s3_2 = helpers.s3(mock.Mock())
        copy_client = helpers.get_copy_client(s3_1, s3_2)
        assert type(copy_client.copier._copy_strategies[(s3_1.fs, s3_1.fs)]) is copy.s3.S3ToS3CopyStrategy
        assert (s3_1.fs, s3_2.fs) not in copy_client.copier._copy_strategies
        assert (s3_2.fs, s3_1.fs) not in copy_client.copier._copy_strategies
        assert type(copy_client.copier._copy_strategies[(s3_2.fs, s3_2.fs)]) is copy.s3.S3ToS3CopyStrategy
