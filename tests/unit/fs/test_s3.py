import random

from typing import List
from unittest import (
    TestCase,
    mock,
)

from norfs.fs.base import (
    FSObjectType,
    Path,
)
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
        self.client = mock.Mock()
        self.fs = S3FileSystem(self.client, uri_protocol=self.protocol, separator=self.separator)

    def test_parse_path(self) -> None:
        expected_path: Path = random_path()
        abs_input_path_str: str = f"{expected_path.drive}/{self.separator.join(expected_path.tail)}"
        assert self.fs.parse_path(abs_input_path_str) == expected_path
        assert self.fs.parse_path(abs_input_path_str + self.separator) == expected_path

        expected_path = Path(randstr())
        abs_input_path_str = f"{expected_path.drive}"
        assert self.fs.parse_path(abs_input_path_str) == expected_path
        assert self.fs.parse_path(abs_input_path_str + "/") == expected_path
        assert self.fs.parse_path(abs_input_path_str + "/" + self.separator) == expected_path

    def test_path_to_string(self) -> None:
        path: Path = random_path()
        result: str = self.fs.path_to_string(path)
        assert result == f"{path.drive}/{self.separator.join(path.tail)}"

        path = Path(randstr())
        result = self.fs.path_to_string(path)
        assert result == f"{path.drive}"

    def test_path_to_uri(self) -> None:
        path: Path = random_path()
        path_str: str = f"{path.drive}/{self.separator.join(path.tail)}"
        assert self.fs.path_to_uri(path) == "{}://{}".format(self.protocol, path_str)

    def test_dir_list_continuation_token(self) -> None:
        times: int = random.randint(2, 5)
        input_path: Path = random_path()
        tail_str: str = self.separator.join(input_path.tail)
        files: List[List[str]] = [[randstr() for _ in range(random.randint(1, 3))] for _ in range(times)]
        dirs: List[List[str]] = [[randstr() for _ in range(random.randint(1, 3))] for _ in range(times)]
        cont_tokens: List[str] = [randstr() for _ in range(times - 1)]
        self.client.list_objects_v2.side_effect = [
            {
                "Contents": [{"Key": tail_str + self.separator + file} for file in iter_files],
                "CommonPrefixes": [{"Prefix": tail_str + self.separator + dir + self.separator} for dir in iter_dirs],
                "IsTruncated": True,
                "NextContinuationToken": cont_token
            }
            for iter_files, iter_dirs, cont_token in zip(files[:-1], dirs[:-1], cont_tokens)
        ] + [
            {
                "Contents": [{"Key": tail_str + self.separator + file} for file in files[-1]],
                "CommonPrefixes": [{"Prefix": tail_str + self.separator + dir + self.separator} for dir in dirs[-1]],
                "IsTruncated": False,
            }
        ]
        result_files = []
        result_dirs = []
        result_others = []

        for obj in self.fs.dir_list(input_path):
            if obj.type == FSObjectType.DIR:
                result_dirs.append(obj.path)
            elif obj.type == FSObjectType.FILE:
                result_files.append(obj.path)
            else:
                result_others.append(obj.path)

        expected_call_list: List[mock.call] = [
            mock.call(
                Bucket=input_path.drive,
                Prefix=tail_str + self.separator,
                Delimiter=self.separator,
                ContinuationToken=""
            )
        ] + [
            mock.call(
                Bucket=input_path.drive,
                Prefix=tail_str + self.separator,
                Delimiter=self.separator,
                ContinuationToken=cont_token
            )
            for cont_token in cont_tokens
        ]
        assert self.client.list_objects_v2.call_args_list == expected_call_list
        assert result_files == [input_path.child(file) for files_it in files for file in files_it]
        assert result_dirs == [input_path.child(dir) for dirs_it in dirs for dir in dirs_it]
        assert result_others == []
