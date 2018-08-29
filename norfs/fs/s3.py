import traceback
from io import BytesIO
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

from norfs.fs.base import (
    BaseFileSystem,
    DirListResult,
    FileSystemOperationError,
    Path,
)


class S3FileSystem(BaseFileSystem):
    _s3_client: Any
    _protocol: str
    _separator: str

    def __init__(self, s3_client: Any, *, uri_protocol: str="s3", separator: str="/") -> None:
        self._s3_client = s3_client
        self._protocol = uri_protocol
        self._separator = separator

    # General operations
    def parse_path(self, path: str) -> Path:
        bucket_path_separator_position: int = path.find("/")
        drive: str = path
        tail: List[str] = []
        tail_end: int = len(path)
        if path.endswith(self._separator):
            tail_end -= len(self._separator)
        if bucket_path_separator_position > 0:
            drive = path[:bucket_path_separator_position]
            tail_start: int = bucket_path_separator_position + 1
            if tail_end > tail_start:
                tail = path[tail_start:tail_end].split(self._separator)
        return Path(drive, *tail)

    def path_exists(self, path: Path) -> bool:
        prefix: str = self._separator.join(path.tail)
        response: Dict[str, List[Dict[str, str]]] = self._s3_client.list_objects_v2(
            Bucket=path.drive,
            Prefix=prefix,
            Delimiter=self._separator
        )

        contents: List[Dict[str, str]] = response.get('Contents', [])
        for item in contents:
            file_name: str = item['Key']
            if file_name == prefix:
                return True

        prefixes: List[Dict[str, str]] = response.get('CommonPrefixes', [])
        for item in prefixes:
            dir_name: str = item['Prefix']
            if dir_name == prefix + self._separator:
                return True

        return False

    def path_to_string(self, path: Path) -> str:
        joint: str = ""
        if path.tail:
            joint = "/"
        return f"{path.drive}{joint}{self._separator.join(path.tail)}"

    def path_to_uri(self, path: Path) -> str:
        return f"{self._protocol}://{self.path_to_string(path)}"

    # File operations
    def file_read(self, path: Path) -> bytes:
        prefix: str = self._separator.join(path.tail)
        try:
            data = BytesIO()
            self._s3_client.download_fileobj(path.drive, prefix, data)
            data.seek(0)
            return data.read()
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    def file_write(self, path: Path, content: bytes) -> None:
        try:
            dirs: Tuple[str, ...] = path.parent.tail
            acc_prefix: str = ""
            for dir_ in dirs:
                if acc_prefix:
                    acc_prefix = self._separator.join((acc_prefix, dir_))
                else:
                    acc_prefix = dir_
                self._s3_client.upload_fileobj(BytesIO(b""), path.drive, acc_prefix + self._separator)

            path_str: str = self.path_to_string(path)
            tail: str = path_str[path_str.find("/") + 1:]
            self._s3_client.upload_fileobj(BytesIO(content), path.drive, tail)
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    def file_remove(self, path: Path) -> None:
        prefix: str = self._separator.join(path.tail)
        try:
            response: Dict[str, List[Dict[str, str]]] = self._s3_client.list_objects_v2(
                Bucket=path.drive,
                Prefix=prefix,
            )
            contents: List[Dict[str, str]] = response.get('Contents', [])
            if contents:
                self._s3_client.delete_objects(
                    Bucket=path.drive,
                    Delete={
                        'Objects': [{'Key': f['Key']} for f in contents if f['Key'] == prefix]
                    }
                )
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    # Directory operations
    def dir_list(self, path: Path) -> DirListResult:
        tail_str: str = self._separator.join(path.tail)
        if tail_str:
            tail_str += self._separator

        files: List[Path] = []
        dirs: List[Path] = []

        response: Dict[str, List[Dict[str, str]]]
        try:
            response = self._s3_client.list_objects_v2(
                Bucket=path.drive,
                Prefix=tail_str,
                Delimiter=self._separator
            )
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

        files, dirs = self._extend_files_and_dirs_with_response(tail_str, path, files, dirs, response)

        while response.get("IsTruncated", False):
            try:
                response = self._s3_client.list_objects_v2(
                    Bucket=path.drive,
                    Prefix=tail_str,
                    Delimiter=self._separator,
                    ContinuationToken=response.get("NextContinuationToken", "")
                )
            except Exception:
                raise FileSystemOperationError(traceback.format_exc())

            files, dirs = self._extend_files_and_dirs_with_response(tail_str, path, files, dirs, response)

        return DirListResult(files, dirs, [])

    def dir_remove(self, path: Path) -> None:
        try:
            response: Dict[str, List[Dict[str, str]]] = self._s3_client.list_objects_v2(
                Bucket=path.drive,
                Prefix=self._separator.join(path.tail) + self._separator
            )
            contents: List[Dict[str, str]] = response.get('Contents', [])
            if contents:
                self._s3_client.delete_objects(
                    Bucket=path.drive,
                    Delete={
                        'Objects': [{'Key': f['Key']} for f in contents]
                    }
                )
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(s3_client={self._s3_client}, uri_protocol={self._protocol}, "
                f"separator={self._separator})")

    def _extend_files_and_dirs_with_response(self, tail_str: str, path: Path, files: List[Path], dirs: List[Path],
                                             response: Dict[str, List[Dict[str, str]]]
                                             ) -> Tuple[List[Path], List[Path]]:
        file_name: str
        for item in response.get("Contents", []):
            file_name = item["Key"]
            if file_name != tail_str:
                if file_name.endswith(self._separator):
                    dirs.append(Path(path.drive, *(file_name.split(self._separator)[:-1])))
                else:
                    files.append(Path(path.drive, *file_name.split(self._separator)))

        dir_name: str
        for item in response.get("CommonPrefixes", []):
            dir_name = item["Prefix"]
            dirs.append(Path(path.drive, *(dir_name.split(self._separator)[:-1])))

        return files, dirs
