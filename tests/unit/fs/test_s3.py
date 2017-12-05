from unittest import TestCase

from norfs.fs import Path
from norfs.fs.s3 import S3FileSystem

from tests.tools import (
    random_path,
    randstr,
)


class TestS3FileSystem(TestCase):
    protocol: str
    separator: str
    fs: S3FileSystem

    def setUp(self) -> None:
        self.protocol = randstr()
        self.separator = randstr()
        self.fs = S3FileSystem(None, uri_protocol=self.protocol, separator=self.separator)

    def test_parse_path(self) -> None:
        expected_path: Path = random_path()
        abs_input_path_str: str = f"{expected_path.drive}/{self.separator.join(expected_path.tail)}"
        assert self.fs.parse_path(abs_input_path_str) == expected_path

    def test_path_to_string(self) -> None:
        path: Path = random_path()
        result: str = self.fs.path_to_string(path)
        assert result == f"{path.drive}/{self.separator.join(path.tail)}"

    def test_path_to_uri(self) -> None:
        path: Path = random_path()
        path_str: str = f"{path.drive}/{self.separator.join(path.tail)}"
        assert self.fs.path_to_uri(path) == "{}://{}".format(self.protocol, path_str)
