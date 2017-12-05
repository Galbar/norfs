import os

from unittest import TestCase


from norfs.fs import Path
from norfs.fs.local import LocalFileSystem

from tests.tools import random_local_path


class TestLocalFileSystem(TestCase):
    fs: LocalFileSystem

    def setUp(self) -> None:
        self.fs = LocalFileSystem()

    def test_parse_path(self) -> None:
        expected_path: Path
        abs_input_path_str: str
        expected_path, abs_input_path_str = random_local_path()
        assert self.fs.parse_path(abs_input_path_str) == expected_path

        prefix_to_remove: str = os.path.commonpath([os.getcwd(), abs_input_path_str])
        rel_input_path_str: str = abs_input_path_str[len(prefix_to_remove) + len(os.sep):]
        assert self.fs.parse_path(rel_input_path_str) == expected_path

    def test_path_to_string(self) -> None:
        path: Path = random_local_path()[0]
        result: str = self.fs.path_to_string(path)
        assert result == os.path.join(path.drive, os.sep.join(path.tail))
        assert os.path.isabs(result)

    def test_path_to_uri(self) -> None:
        path: Path = random_local_path()[0]
        assert self.fs.path_to_uri(path) == "file:///{}/{}".format(path.drive, os.path.join(*path.tail))
