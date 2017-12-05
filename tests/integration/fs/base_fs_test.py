from typing import (
    Dict,
    Union,
)

from norfs.fs import (
    BaseFileSystem,
    DirListResult,
    Path,
)

from tests.tools import randstr


# TODO: change `dict` by `'Scenario'` when https://github.com/python/mypy/issues/4200 is closed
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

        assert self.fs.dir_list(self.make_path()) == DirListResult(
            [self.make_path(path) for path in ["filec"]],
            [self.make_path(path) for path in ["dira", "dirb"]],
            []
        )
        assert self.fs.dir_list(self.make_path("dira")) == DirListResult(
            [self.make_path(*path) for path in [["dira", "fileaa"], ["dira", "fileab"]]],
            [self.make_path(*path) for path in [["dira", "dirc"]]],
            []
        )
        assert self.fs.dir_list(self.make_path("dira", "dirc")) == DirListResult(
            [self.make_path(*path) for path in [["dira", "dirc", "fileaca"]]],
            [], []
        )
        assert self.fs.dir_list(self.make_path("dirb")) == DirListResult([], [], [])
        assert self.fs.dir_list(self.make_path("dira", "non", "existent", "dir")) == DirListResult([], [], [])

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
