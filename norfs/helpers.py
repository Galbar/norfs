from typing import (
    Any,
    cast,
)
import norfs.copy.local
import norfs.copy.s3
import norfs.client
import norfs.fs.local
import norfs.fs.memory
import norfs.fs.s3


def get_copy_client(*args: norfs.client.FileSystemClient) -> norfs.client.CopyClient:
    copier = norfs.copy.base.Copier(norfs.copy.base.GenericCopyStrategy())
    copy_strategy: norfs.copy.base.CopyStrategy
    for src in args:
        src_type = type(src.fs)
        for dst in args:
            dst_type = type(dst.fs)
            if src_type is norfs.fs.local.LocalFileSystem:
                if dst_type is norfs.fs.local.LocalFileSystem:
                    copy_strategy = norfs.copy.local.LocalToLocalCopyStrategy()
                elif dst_type is norfs.fs.s3.S3FileSystem:
                    copy_strategy = norfs.copy.local.LocalToS3CopyStrategy(
                        cast(norfs.fs.s3.S3FileSystem, dst.fs)._s3_client)
                else:
                    raise TypeError("Unknown Filesystem type {} of client {}".format(dst_type, dst))
            elif src_type is norfs.fs.s3.S3FileSystem:
                if dst_type is norfs.fs.local.LocalFileSystem:
                    copy_strategy = norfs.copy.s3.S3ToLocalCopyStrategy(
                        cast(norfs.fs.s3.S3FileSystem, src.fs)._s3_client)
                elif dst_type is norfs.fs.s3.S3FileSystem:
                    src_s3_client = cast(norfs.fs.s3.S3FileSystem, src.fs)._s3_client
                    dst_s3_client = cast(norfs.fs.s3.S3FileSystem, dst.fs)._s3_client
                    if src_s3_client is dst_s3_client:
                        copy_strategy = norfs.copy.s3.S3ToS3CopyStrategy(src_s3_client)
                    else:
                        continue
                else:
                    raise TypeError("Unknown Filesystem type {} of client {}".format(dst_type, dst))
            else:
                raise TypeError("Unknown Filesystem type {} of client {}".format(src_type, dst))

            copier.set_copy_policy(src.fs, dst.fs, copy_strategy)

    return norfs.client.CopyClient(copier)


def local() -> norfs.client.FileSystemClient:
    return norfs.client.FileSystemClient(norfs.fs.local.LocalFileSystem())


def memory(**kwargs: Any) -> norfs.client.FileSystemClient:
    return norfs.client.FileSystemClient(norfs.fs.memory.MemoryFileSystem(norfs.fs.memory.MemoryDirectory(), **kwargs))


def s3(*args: Any, **kwargs: Any) -> norfs.client.FileSystemClient:
    return norfs.client.FileSystemClient(norfs.fs.s3.S3FileSystem(*args, **kwargs))
