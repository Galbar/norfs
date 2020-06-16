from typing import List, Any
from enum import Enum, auto


class Perm(Enum):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    READ_PERMS = auto()
    WRITE_PERMS = auto()


class Scope(Enum):
    OWNER = auto()
    GROUP = auto()
    OTHERS = auto()


class Policy:

    _scope: Scope
    _perms: List[Perm]

    def __init__(self, scope: Scope, perms: List[Perm]) -> None:
        self._scope = scope
        self._perms = perms

    @property
    def scope(self) -> Scope:
        return self._scope

    @property
    def perms(self) -> List[Perm]:
        return self._perms

    def __eq__(self, o: Any) -> bool:
        if not isinstance(o, Policy):
            return False

        return self._scope == o._scope and set(self._perms) == set(o._perms)
