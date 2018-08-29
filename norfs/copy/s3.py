import os
import traceback

from typing import (
    Any,
    Dict,
    List,
)

from norfs.copy.base import (
    CopyDirectory,
    CopyFile,
    GenericCopyStrategy,
)
from norfs.fs.base import (
    FileSystemOperationError,
    Path,
)


class S3ToS3CopyStrategy(GenericCopyStrategy):

    def __init__(self, s3_client: Any) -> None:
        self._s3_client = s3_client

    def _list_dir(self, dir_drive: str, dir_tail: str) -> List[str]:
        response: Dict[str, List[Dict[str, str]]]
        try:
            response = self._s3_client.list_objects_v2(
                Bucket=dir_drive,
                Prefix=dir_tail
            )
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

        items: List[str] = []
        for item in response.get("Contents", []):
            items.append(item["Key"])

        while response.get("IsTruncated", False):
            try:
                response = self._s3_client.list_objects_v2(
                    Bucket=dir_drive,
                    Prefix=dir_tail,
                    ContinuationToken=response.get("NextContinuationToken", "")
                )
            except Exception:
                raise FileSystemOperationError(traceback.format_exc())

            for item in response.get("Contents", []):
                items.append(item["Key"])

        return items

    def copy_dir_to_dir(self, src: CopyDirectory, dst: CopyDirectory) -> None:
        dir_path_str: str = src.fs.path_to_string(src.path)
        src_dir_tail: str = dir_path_str[dir_path_str.find("/") + 1:]
        dir_path_str = src.fs.path_to_string(dst.path)
        dst_dir_tail: str = dir_path_str[dir_path_str.find("/") + 1:]

        for src_obj_path in self._list_dir(src.path.drive, src_dir_tail):
            dst_obj_path: str = src_obj_path.replace(src_dir_tail, dst_dir_tail)
            if src_obj_path.endswith("/"):
                copy_source = {
                    'Bucket': src.path.drive,
                    'Key': src_obj_path
                }
                self._s3_client.copy(copy_source, dst.path.drive, dst_obj_path)
            else:
                src_file: CopyFile = CopyFile(src.fs, src.fs.parse_path(f'{src.path.drive}/{src_obj_path}'))
                dst_file: CopyFile = CopyFile(dst.fs, dst.fs.parse_path(f'{dst.path.drive}/{dst_obj_path}'))
                self.copy_file_to_file(src_file, dst_file)

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


class S3ToLocalCopyStrategy(GenericCopyStrategy):

    def __init__(self, s3_client: Any) -> None:
        self._s3_client = s3_client

    def copy_file_to_file(self, src: CopyFile, dst: CopyFile) -> None:
        parent_dir: Path = dst.path.parent
        if not dst.fs.path_exists(parent_dir):
            os.makedirs(dst.fs.path_to_string(parent_dir))
        src_path_str: str = src.fs.path_to_string(src.path)
        src_tail: str = src_path_str[src_path_str.find("/") + 1:]
        self._s3_client.download_file(src.path.drive, src_tail, dst.fs.path_to_string(dst.path))
