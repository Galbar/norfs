from typing import (
    Any,
    Dict,
    Optional,
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


_config: Optional[Dict[str, Any]] = None
_copy_handler: Optional[CopyHandler] = None
_local_fs: Optional[LocalFileSystem] = None
_s3_fs: Optional[S3FileSystem] = None
_memory_fs: Optional[MemoryFileSystem] = None


class Version:
    MAJOR: str = "1"
    MINOR: str = "3"
    PATCH: str = "0"

    VERSION: str = ".".join((MAJOR, MINOR))
    RELEASE: str = ".".join((MAJOR, MINOR, PATCH))


def get_copy_handler() -> CopyHandler:
    """ Returns the global instance of CopyHandler. """
    global _copy_handler

    if _copy_handler is None:
        _copy_handler = CopyHandler(GenericCopier())

    return _copy_handler


def _get_config() -> Dict[str, Any]:
    global _config

    if _config is None:
        _config = {
            "s3_client": None,
            "s3_protocol": "s3",
            "s3_separator": "/",
            "memory_separator": "/",
        }

    return _config


def configure(**kwargs: Any) -> None:
    """ Set the configuration for the library.
    Accepted keyword values:

    *  `s3_client`: boto3 S3 client instance for S3FileSystem.
    *  `s3_protocol`: protocol to use for S3FileSystem uri. Defaults to "s3".
    *  `s3_separator`: directory separator to use for S3FileSystem. Defaults to "/".
    *  `memory_separator`: directory separator to use for MemoryFileSystem. Defaults to "/".
    """
    _get_config().update(kwargs)


def _init_local_fs() -> LocalFileSystem:
    global _local_fs

    _local_fs = LocalFileSystem()

    get_copy_handler().set_copy_policy(_local_fs, _local_fs, LocalToLocalCopier())

    return _local_fs


def get_local_fs() -> LocalFileSystem:
    """ Returns the global instance of LocalFileSystem. """
    global _local_fs

    return _local_fs or _init_local_fs()


def localdir(path: str) -> Directory:
    """ Return a Directory instance with the given `path` for the LocalFileSystem. """
    return Directory(get_local_fs(), path, get_copy_handler())


def localfile(path: str) -> File:
    """ Return a File instance with the given `path` for the LocalFileSystem. """
    return File(get_local_fs(), path, get_copy_handler())


def _init_s3_fs() -> S3FileSystem:
    global _s3_fs

    config: Dict[str, Any] = _get_config()

    if config["s3_client"] is None:
        raise ValueError("Cannot initialize S3FileSystem if s3_client is not set.\n"
                         "You can set it using `norfs.configure(s3_client=boto3.client(\"s3\"))`")

    s3_client: Any = config["s3_client"]

    _s3_fs = S3FileSystem(s3_client, uri_protocol=config["s3_protocol"], separator=config["s3_separator"])

    copy_handler: CopyHandler = get_copy_handler()
    copy_handler.set_copy_policy(get_local_fs(), _s3_fs, LocalToS3Copier(s3_client))
    copy_handler.set_copy_policy(_s3_fs, get_local_fs(), S3ToLocalCopier(s3_client))
    copy_handler.set_copy_policy(_s3_fs, _s3_fs, S3ToS3Copier(s3_client))

    return _s3_fs


def get_s3_fs() -> S3FileSystem:
    """ Returns the global instance of S3FileSystem. """
    global _s3_fs

    return _s3_fs or _init_s3_fs()


def _get_s3_path(path_or_bucket: str, prefix: Optional[str]=None) -> str:
    if prefix is None:
        return path_or_bucket
    return "/".join((path_or_bucket, prefix))


def s3dir(path_or_bucket: str, prefix: Optional[str]=None) -> Directory:
    """ Return a Directory instance with the given bucket and path for the S3FileSystem.

    If only one parameter is given the bucket name will be everything up to the first "/".
    """
    return Directory(get_s3_fs(), _get_s3_path(path_or_bucket, prefix), get_copy_handler())


def s3file(path_or_bucket: str, prefix: Optional[str]=None) -> File:
    """ Return a File instance with the given bucket and path for the S3FileSystem.

    If only one parameter is given the bucket name will be everything up to the first "/".
    """
    return File(get_s3_fs(), _get_s3_path(path_or_bucket, prefix), get_copy_handler())


def _init_memory_fs() -> MemoryFileSystem:
    global _memory_fs

    config: Dict[str, Any] = _get_config()

    _memory_fs = MemoryFileSystem(MemoryDirectory(), separator=config["memory_separator"])

    return _memory_fs


def get_memory_fs() -> MemoryFileSystem:
    """ Returns the global instance of MemoryFileSystem. """
    global _memory_fs

    return _memory_fs or _init_memory_fs()


def memorydir(path: str) -> Directory:
    """ Return a Directory instance with the given `path` for the MemoryFileSystem. """
    return Directory(get_memory_fs(), path, get_copy_handler())


def memoryfile(path: str) -> File:
    """ Return a File instance with the given `path` for the MemoryFileSystem. """
    return File(get_memory_fs(), path, get_copy_handler())
