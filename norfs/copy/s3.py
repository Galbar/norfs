import os

from typing import Any

from . import (
    GenericCopier,
    CopyFile,
)
from ..fs import Path


class S3ToS3Copier(GenericCopier):

    def __init__(self, s3_client: Any) -> None:
        self._s3_client = s3_client

    def copy_file_to_file(self, src: CopyFile, dst: CopyFile) -> None:
        src_path_str: str = src.fs.path_to_string(src.path)
        src_tail: str = src_path_str[src_path_str.find("/") + 1:]
        copy_source = {
            'Bucket': src.path.drive,
            'Key': src_tail
        }
        dst_path_str: str = dst.fs.path_to_string(dst.path)
        dst_tail: str = dst_path_str[dst_path_str.find("/") + 1:]
        self._s3_client.copy(copy_source, dst.path.drive, dst_tail)


class S3ToLocalCopier(GenericCopier):

    def __init__(self, s3_client: Any) -> None:
        self._s3_client = s3_client

    def copy_file_to_file(self, src: CopyFile, dst: CopyFile) -> None:
        parent_dir: Path = dst.path.parent
        if not dst.fs.path_exists(parent_dir):
            os.makedirs(dst.fs.path_to_string(parent_dir))
        src_path_str: str = src.fs.path_to_string(src.path)
        src_tail: str = src_path_str[src_path_str.find("/") + 1:]
        self._s3_client.download_file(src.path.drive, src_tail, dst.fs.path_to_string(dst.path))
