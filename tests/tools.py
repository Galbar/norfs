import os
import random
import string

from typing import (
    List,
    Optional,
    Tuple,
)

from norfs.fs.base import Path


def randstr(length: int=10, charset: str=string.ascii_letters) -> str:
    return "".join(random.choice(charset) for _ in range(length))


def random_path(drive: Optional[str]=None, prefix: List[str]=[]) -> Path:
    if drive is None:
        drive = randstr()
    tail: List[str] = prefix + [randstr() for _ in range(random.randint(1, 5))]
    return Path(drive, *tail)


def random_local_path(*, root: Optional[str]=None) -> Tuple[Path, str]:
    root = root or os.getcwd()
    path_str: str = os.path.join(root, *[randstr() for _ in range(random.randint(1, 5))])
    abs_path_str: str = os.path.abspath(path_str)
    drive: str
    tail_str: str
    drive, tail_str = os.path.splitdrive(abs_path_str)
    tail: List[str] = os.path.normpath(tail_str).split(os.sep)
    return Path(drive, *tail), abs_path_str
