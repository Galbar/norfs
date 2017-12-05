from collections import deque
from typing import (
    Deque,
    Tuple,
    Set,
)
from unittest import TestCase

from norfs.fs import Path
from norfs.fs.memory import (
    MemoryFileSystem,
    MemoryDirectory,
    MemoryFile,
)

from .base_fs_test import (
    BaseTestFileSystem,
    Scenario,
)


class TestMemoryFileSystem(BaseTestFileSystem, TestCase):

    def setUp(self) -> None:
        self.root: MemoryDirectory = MemoryDirectory()
        self.fs = MemoryFileSystem(self.root)

    def setup_scenario(self, scenario: Scenario) -> None:
        for dir_name in self.root.list_dirs():
            self.root.remove_dir(dir_name)
        for file_name in self.root.list_files():
            self.root.remove_file(file_name)

        queue: Deque[Tuple[MemoryDirectory, Scenario]] = deque([(self.root, scenario)])
        while queue:
            dir_: MemoryDirectory
            scene: Scenario
            dir_, scene = queue.pop()
            for name, value in scene.items():
                if isinstance(value, dict):
                    subdir: MemoryDirectory = MemoryDirectory()
                    dir_.put_dir(name, subdir)
                    queue.append((subdir, value))
                else:
                    file_: MemoryFile = MemoryFile(value)
                    dir_.put_file(name, file_)

    def make_path(self, *tail: str) -> Path:
        return Path("", *tail)

    def assert_scenario(self, scenario: Scenario) -> None:
        queue: Deque[Tuple[MemoryDirectory, Scenario]] = deque([(self.root, scenario)])
        while queue:
            dir_: MemoryDirectory
            scene: Scenario
            dir_, scene = queue.pop()
            subdirs: Set[str] = set()
            files: Set[str] = set()
            for name, value in scene.items():
                if isinstance(value, dict):
                    queue.append((dir_.get_dir(name), value))
                    subdirs.add(name)
                else:
                    assert dir_.get_file(name).contents == value
                    files.add(name)

            assert subdirs == set(dir_.list_dirs())
            assert files == set(dir_.list_files())
