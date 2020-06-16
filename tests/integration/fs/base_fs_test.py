from typing import (
    Dict,
    List,
    Union,
)

from norfs.fs.base import (
    BaseFileSystem,
    FSObjectType,
    FileSystemOperationError,
    Path,
)

from tests.tools import randstr


# TODO: change `dict` by `'Scenario'` when https://github.com/python/mypy/issues/731 is closed
Scenario = Dict[str, Union[bytes, dict]]


class BaseTestFileSystem:
    fs: BaseFileSystem

    def make_path(self, *tail: str) -> Path:
        raise NotImplementedError()

    def setup_scenario(self, scenario: Scenario) -> None:
        raise NotImplementedError()

    def assert_scenario(self, scenario: Scenario) -> None:
        raise NotImplementedError()

    def test_path_exists(self) -> None:
        scenario: Scenario = {
            'dir': {
                'file': b'content'
            }
        }
        self.setup_scenario(scenario)

        assert self.fs.path_exists(self.make_path("dir", "file")) is True
        assert self.fs.path_exists(self.make_path("dir")) is True
        assert self.fs.path_exists(self.make_path("direct")) is False
        assert self.fs.path_exists(self.make_path("dir", "asf")) is False
        assert self.fs.path_exists(self.make_path("dir", "subdir", "asf")) is False

    def test_file_read(self) -> None:
        file_contents: bytes = randstr().encode()
        scenario: Scenario = {
            'dira': {
                'fileaa': file_contents,
            },
        }
        self.setup_scenario(scenario)

        assert self.fs.file_read(self.make_path("dira", "fileaa")) == file_contents

    def test_file_read_on_a_dir_fails(self) -> None:
        file_contents: bytes = randstr().encode()
        scenario: Scenario = {
            'dira': {
                'fileaa': file_contents,
            },
        }
        self.setup_scenario(scenario)

        error_happened: bool
        try:
            self.fs.file_read(self.make_path("dira"))
        except FileSystemOperationError:
            error_happened = True
        else:
            error_happened = False

        assert error_happened

    def test_file_write(self) -> None:
        scenario: Scenario = {
            'dira': {}
        }
        file_contents: bytes = randstr().encode()
        expected_scenario: Scenario = {
            'dira': {
                'dirb': {
                    'fileaba': file_contents
                }
            }
        }
        self.setup_scenario(scenario)

        self.fs.file_write(self.make_path("dira", "dirb", "fileaba"), file_contents)

        self.assert_scenario(expected_scenario)

    def test_file_remove(self) -> None:
        scenario: Scenario = {
            'dira': {
                'fileaa': b'contentaa'
            }
        }
        expected_scenario: Scenario = {
            'dira': {}
        }

        self.setup_scenario(scenario)

        self.fs.file_remove(self.make_path("dira", "fileaa"))

        self.assert_scenario(expected_scenario)

    def test_dir_list(self) -> None:
        scenario: Scenario = {
            'dira': {
                'fileaa': b'contentaa',
                'fileab': b'contentab',
                'dirc': {
                    'fileaca': b'contentaca'
                },
            },
            'dirb': {},
            'filec': b'contentc',
        }
        self.setup_scenario(scenario)

        self._assert_dir_list(self.make_path(),
                              [self.make_path(path) for path in ["filec"]],
                              [self.make_path(path) for path in ["dira", "dirb"]],
                              [])
        self._assert_dir_list(self.make_path(),
                              [self.make_path(path) for path in ["filec"]],
                              [self.make_path(path) for path in ["dira", "dirb"]],
                              [])
        self._assert_dir_list(self.make_path("dira"),
                              [self.make_path(*path) for path in [["dira", "fileaa"], ["dira", "fileab"]]],
                              [self.make_path(*path) for path in [["dira", "dirc"]]],
                              [])
        self._assert_dir_list(self.make_path("dira", "dirc"),
                              [self.make_path(*path) for path in [["dira", "dirc", "fileaca"]]],
                              [],
                              [])
        self._assert_dir_list(self.make_path("dirb"), [], [], [])
        self._assert_dir_list(self.make_path("dira", "non", "existent", "dir"), [], [], [])

    def test_dir_remove(self) -> None:
        scenario: Scenario = {
            'dira': {
                'fileaa': b'contentaa',
                'fileab': b'contentab',
                'dirc': {
                    'fileaca': b'contentaca'
                },
            },
            'dirb': {},
            'filec': b'contentc',
        }
        expected_scenario: Scenario = {
            'dirb': {},
            'filec': b'contentc',
        }
        self.setup_scenario(scenario)
        self.fs.dir_remove(self.make_path("dira"))
        self.assert_scenario(expected_scenario)

    def _assert_dir_list(self, path: Path, files: List[Path], dirs: List[Path], others: List[Path]) -> None:
        result_files = []
        result_dirs = []
        result_others = []
        for obj in self.fs.dir_list(path):
            if obj.type == FSObjectType.DIR:
                result_dirs.append(obj.path)
            elif obj.type == FSObjectType.FILE:
                result_files.append(obj.path)
            else:
                result_others.append(obj.path)

        assert set(result_files) == set(files)
        assert set(result_dirs) == set(dirs)
        assert set(result_others) == set(others)
