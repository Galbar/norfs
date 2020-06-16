import traceback
from io import BytesIO
from urllib.parse import urlencode
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Tuple,
    Optional,
    Union,
    cast
)

from norfs.fs.base import (
    BaseFileSystem,
    FSObjectPath,
    FSObjectType,
    FileSystemOperationError,
    Path,
)

from norfs.permissions import Policy, Perm, Scope


_ALL_PERMS = (Perm.READ, Perm.WRITE, Perm.READ_PERMS, Perm.WRITE_PERMS)


s3_scopes = {
    Scope.GROUP: {
        'Type': 'Group',
        'URI': 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'
    },
    Scope.OTHERS: {
        'Type': 'Group',
        'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'
    },
}
""" Permission scope mapping for S3 """

s3_perms = {
    Perm.READ: 'READ',
    Perm.WRITE: 'WRITE',
    Perm.READ_PERMS: 'READ_ACP',
    Perm.WRITE_PERMS: 'WRITE_ACP',
}
""" Permission mapping for S3 """


class CannedPerms:
    PRIVATE = [Policy(Scope.OWNER, [Perm.WRITE, Perm.READ, Perm.WRITE_PERMS, Perm.READ_PERMS])]
    PUBLIC_READ = PRIVATE + [Policy(Scope.GROUP, [Perm.READ]), Policy(Scope.OTHERS, [Perm.READ])]


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
        self._remove(path, False)

    def file_set_perms(self, path: Path, policies: List[Policy]) -> None:
        """ Set ACL policies for the object.

        Check `norfs.fs.s3.s3_scopes` and `norfs.fs.s3.s3_perms` to understand how :class:`norfs.permissions.Scope` and
        :class:`norfs.permissions.Perm` map to S3 Grantees and Permissions.
        """
        try:
            key = self._separator.join(path.tail)
            acl = self._s3_client.get_object_acl(Bucket=path.drive, Key=key)

            grants = []
            for policy in policies:
                if policy.scope == Scope.OWNER:
                    grantee = acl['Owner'].copy()
                    grantee['Type'] = 'CanonicalUser'
                else:
                    grantee = s3_scopes.get(policy.scope)

                if all((p in policy.perms for p in _ALL_PERMS)):
                    grants.append({
                        'Grantee': grantee,
                        'Permission': 'FULL_CONTROL',
                    })
                else:
                    for perm in policy.perms:
                        permission = s3_perms.get(perm)
                        if permission:
                            grants.append({
                                'Grantee': grantee,
                                'Permission': permission,
                            })

            self._s3_client.put_object_acl(
                AccessControlPolicy={
                    'Grants': grants,
                    'Owner': acl['Owner'],
                },
                Bucket=path.drive,
                Key=key,
            )
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    def file_set_properties(self, path: Path,
                            content_type: Optional[str] = None,
                            tags: Optional[Dict[str, str]] = None,
                            metadata: Optional[Dict[str, str]] = None) -> None:
        """ Set properties for the object.
        """
        kwargs: Dict[str, Any] = {}

        if content_type:
            kwargs['ContentType'] = content_type
            kwargs['MetadataDirective'] = 'REPLACE'

        if tags:
            kwargs['Tagging'] = urlencode(tags)
            kwargs['TaggingDirective'] = 'REPLACE'

        if metadata:
            kwargs['Metadata'] = metadata
            kwargs['MetadataDirective'] = 'REPLACE'

        key: str = self._separator.join(path.tail)
        try:
            acl = self._s3_client.get_object_acl(Bucket=path.drive, Key=key)
            self._s3_client.copy_object(Key=key,
                                        Bucket=path.drive,
                                        CopySource={"Bucket": path.drive, "Key": key},
                                        **kwargs)
            self._s3_client.put_object_acl(
                AccessControlPolicy={
                    'Grants': acl['Grants'],
                    'Owner': acl['Owner'],
                },
                Bucket=path.drive,
                Key=key,
            )
        except Exception:
            raise FileSystemOperationError(traceback.format_exc())

    # Directory operations
    def dir_list(self, path: Path) -> Iterable[FSObjectPath]:
        tail_str: str = self._separator.join(path.tail)
        if tail_str:
            tail_str += self._separator

        response: Dict[str, Union[bool, List[Dict[str, str]]]] = {"IsTruncated": True}
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

            for item in cast(List[Dict[str, str]], response.get("Contents", [])):
                file_name: str = item["Key"]
                if file_name != tail_str:
                    if file_name.endswith(self._separator):
                        yield FSObjectPath(FSObjectType.DIR,
                                           Path(path.drive, *(file_name.split(self._separator)[:-1])))
                    else:
                        yield FSObjectPath(FSObjectType.FILE,
                                           Path(path.drive, *file_name.split(self._separator)))

            for item in cast(List[Dict[str, str]], response.get("CommonPrefixes", [])):
                dir_name: str = item["Prefix"]
                yield FSObjectPath(FSObjectType.DIR,
                                   Path(path.drive, *(dir_name.split(self._separator)[:-1])))

    def dir_remove(self, path: Path) -> None:
        self._remove(path, True)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(s3_client={self._s3_client}, uri_protocol={self._protocol}, "
                f"separator={self._separator})")

    def _remove(self, path: Path, is_dir: bool) -> None:
        tail_str: str = self._separator.join(path.tail)
        if is_dir and tail_str:
            tail_str += self._separator
        response: Dict[str, Union[bool, List[Dict[str, str]]]] = {"IsTruncated": True}
        while response.get("IsTruncated", False):
            try:
                response = self._s3_client.list_objects_v2(
                    Bucket=path.drive,
                    Prefix=tail_str,
                    ContinuationToken=response.get("NextContinuationToken", "")
                )
                contents: List[Dict[str, str]] = cast(List[Dict[str, str]], response.get('Contents', []))
                if contents:
                    self._s3_client.delete_objects(
                        Bucket=path.drive,
                        Delete={
                            'Objects': [{'Key': f['Key']} for f in contents if is_dir or f['Key'] == tail_str]
                        }
                    )
            except Exception:
                raise FileSystemOperationError(traceback.format_exc())
