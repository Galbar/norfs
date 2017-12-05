import os
import shutil

from typing import Any

from . import (
    GenericCopier,
    CopyFile,
)
from ..fs import Path


class LocalToLocalCopier(GenericCopier):

    def copy_file_to_file(self, src: CopyFile, dst: CopyFile) -> None:
        parent_dir: Path = dst.path.parent
        if not dst.fs.path_exists(parent_dir):
            os.makedirs(dst.fs.path_to_string(parent_dir))
        shutil.copyfile(src.fs.path_to_string(src.path), dst.fs.path_to_string(dst.path))


class LocalToS3Copier(GenericCopier):

    def __init__(self, s3_client: Any) -> None:
        self._s3_client = s3_client

    def copy_file_to_file(self, src: CopyFile, dst: CopyFile) -> None:
        dst_path_str: str = dst.fs.path_to_string(dst.path)
        dst_tail: str = dst_path_str[dst_path_str.find("/") + 1:]
        self._s3_client.upload_file(src.fs.path_to_string(src.path), dst.path.drive, dst_tail)
