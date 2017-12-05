import os

from collections import deque
from tempfile import TemporaryDirectory
from typing import (
    Deque,
    List,
    Tuple,
)
from unittest import TestCase

from norfs.fs import Path
from norfs.fs.local import LocalFileSystem

from .base_fs_test import (
    BaseTestFileSystem,
    Scenario,
)


class TestLocalFileSystem(BaseTestFileSystem, TestCase):

    def setUp(self) -> None:
        self.fs = LocalFileSystem()
        self.tmp_dir: TemporaryDirectory = TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def setup_scenario(self, scenario: Scenario) -> None:
        self.tmp_dir.cleanup()
        self.tmp_dir = TemporaryDirectory()

        queue: Deque[Tuple[str, Scenario]] = deque([(self.tmp_dir.name, scenario)])
        while queue:
            dir_: str
            scene: Scenario
            dir_, scene = queue.pop()
            for name, value in scene.items():
                if isinstance(value, dict):
                    subdir: str = os.path.join(dir_, name)
                    os.makedirs(subdir)
                    queue.append((subdir, value))
                else:
                    with open(os.path.join(dir_, name), "wb") as f:
                        f.write(value)

    def make_path(self, *tail: str) -> Path:
        abs_path_str: str = os.path.join(self.tmp_dir.name, *tail)
        drive: str
        tail_str: str
        drive, tail_str = os.path.splitdrive(abs_path_str)
        tail_list: List[str] = os.path.normpath(tail_str).split(os.sep)
        return Path(drive, *tail_list)

    def assert_scenario(self, scenario: Scenario) -> None:
        queue: Deque[Tuple[str, Scenario]] = deque([(self.tmp_dir.name, scenario)])
        while queue:
            dir_: str
            scene: Scenario
            dir_, scene = queue.pop()
            for name, value in scene.items():
                if isinstance(value, dict):
                    queue.append((os.path.join(dir_, name), value))
                else:
                    with open(os.path.join(dir_, name), "rb") as f:
                        assert f.read() == value

            assert set(scene.keys()) == set(os.listdir(dir_))
