import boto3

from collections import deque
from io import BytesIO
from typing import (
    Any,
    Deque,
    Tuple,
    Set,
)
from unittest import TestCase

from moto import mock_s3

from norfs.fs import Path
from norfs.fs.s3 import S3FileSystem

from .base_fs_test import (
    BaseTestFileSystem,
    Scenario,
)

from tests.tools import randstr


@mock_s3
class TestS3FileSystem(BaseTestFileSystem, TestCase):

    def setUp(self) -> None:
        self.client: Any = boto3.client("s3")
        self.s3: Any = boto3.resource("s3")
        self.bucket_name: str = "myBucket"
        self.bucket: Any = self.s3.Bucket(self.bucket_name)
        self.separator: str = randstr(3)
        self.fs = S3FileSystem(self.client, separator=self.separator)
        self._create_bucket()

    def tearDown(self) -> None:
        self._delete_bucket()

    def _create_bucket(self) -> None:
        self.client.create_bucket(Bucket=self.bucket_name)

    def _delete_bucket(self) -> None:
        self.bucket.objects.all().delete()
        self.bucket.delete()

    def setup_scenario(self, scenario: Scenario) -> None:
        self._delete_bucket()
        self._create_bucket()

        queue: Deque[Tuple[str, Scenario]] = deque([("", scenario)])
        while queue:
            dir_: str
            scene: Scenario
            dir_, scene = queue.pop()
            for name, value in scene.items():
                sub: str
                if dir_ == "":
                    sub = name
                else:
                    sub = self.separator.join((dir_, name))
                if isinstance(value, dict):
                    self.client.upload_fileobj(BytesIO(b""), self.bucket_name, sub + self.separator)
                    queue.append((sub, value))
                else:
                    self.client.upload_fileobj(BytesIO(value), self.bucket_name, sub)

    def make_path(self, *tail: str) -> Path:
        return Path(self.bucket_name, *tail)

    def assert_scenario(self, scenario: Scenario) -> None:
        all_contents: Set[str] = set()
        queue: Deque[Tuple[str, Scenario]] = deque([("", scenario)])
        while queue:
            path: str
            scene: Scenario
            path, scene = queue.pop()
            for name, value in scene.items():
                key: str = self.separator.join((path, name)) if path else name
                expected_content: bytes
                if isinstance(value, dict):
                    queue.append((key, value))
                    key += self.separator
                    expected_content = b""
                else:
                    expected_content = value

                all_contents.add(key)
                assert self.s3.Object(self.bucket_name, key).get()['Body'].read() == expected_content

        assert all_contents == set(obj.key for obj in self.bucket.objects.all())
