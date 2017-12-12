from typing import (
    Any,
    Dict,
)

from .copy import (
    CopyHandler,
    GenericCopier,
)
from .copy.local import (
    LocalToLocalCopier,
    LocalToS3Copier,
)
from .copy.s3 import (
    S3ToS3Copier,
    S3ToLocalCopier,
)
from .filesystem import (
    Directory,
    File,
)
from .fs.local import LocalFileSystem
from .fs.s3 import S3FileSystem
from .fs.memory import (
    MemoryFileSystem,
    MemoryDirectory,
)


_copy_handler: CopyHandler = None
_local_fs: LocalFileSystem = None
_s3_fs: S3FileSystem = None
_memory_fs: MemoryFileSystem = None

_config: Dict[str, Any] = {
    "s3_client": None,
    "s3_protocol": "s3",
    "s3_separator": "/",
    "memory_separator": "/",
}


def get_copy_handler() -> CopyHandler:
    global _copy_handler

    if _copy_handler is None:
        _copy_handler = CopyHandler(GenericCopier())

    return _copy_handler


def configure(**kwargs: Any) -> None:
    global _config
    _config.update(kwargs)


def _init_local_fs() -> None:
    global _local_fs

    _local_fs = LocalFileSystem()

    get_copy_handler().set_copy_policy(_local_fs, _local_fs, LocalToLocalCopier())


def get_local_fs() -> LocalFileSystem:
    global _local_fs

    if _local_fs is None:
        _init_local_fs()

    return _local_fs


def localdir(path: str) -> Directory:
    return Directory(get_local_fs(), path, get_copy_handler())


def localfile(path: str) -> File:
    return File(get_local_fs(), path, get_copy_handler())


def _init_s3_fs() -> None:
    global _config
    global _s3_fs

    if _config["s3_client"] is None:
        raise ValueError("Cannot initialize S3FileSystem if s3_client is not set.\n"
                         "You can set it using `norfs.configure(s3_client=boto3.client(\"s3\"))`")

    s3_client: Any = _config["s3_client"]

    _s3_fs = S3FileSystem(s3_client, uri_protocol=_config["s3_protocol"], separator=_config["s3_separator"])

    copy_handler: CopyHandler = get_copy_handler()
    copy_handler.set_copy_policy(get_local_fs(), _s3_fs, LocalToS3Copier(s3_client))
    copy_handler.set_copy_policy(_s3_fs, get_local_fs(), S3ToLocalCopier(s3_client))
    copy_handler.set_copy_policy(_s3_fs, _s3_fs, S3ToS3Copier(s3_client))


def get_s3_fs() -> S3FileSystem:
    global _s3_fs

    if _s3_fs is None:
        _init_s3_fs()

    return _s3_fs


def _get_s3_path(path_or_bucket: str, prefix: str=None) -> str:
    if prefix is None:
        return path_or_bucket
    return "/".join((path_or_bucket, prefix))


def s3dir(path_or_bucket: str, prefix: str=None) -> Directory:
    global _config
    return Directory(get_s3_fs(), _get_s3_path(path_or_bucket, prefix), get_copy_handler())


def s3file(path_or_bucket: str, prefix: str=None) -> File:
    global _config
    return File(get_s3_fs(), _get_s3_path(path_or_bucket, prefix), get_copy_handler())


def _init_memory_fs() -> None:
    global _config
    global _memory_fs

    _memory_fs = MemoryFileSystem(MemoryDirectory(), separator=_config["memory_separator"])


def get_memory_fs() -> MemoryFileSystem:
    global _memory_fs

    if _memory_fs is None:
        _init_memory_fs()

    return _memory_fs


def memorydir(path: str) -> Directory:
    return Directory(get_memory_fs(), path, get_copy_handler())


def memoryfile(path: str) -> File:
    return File(get_memory_fs(), path, get_copy_handler())
