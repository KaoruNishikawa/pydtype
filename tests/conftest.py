from typing import NoReturn

from pydtype.core import Specifier


class SimpleSpecifier(Specifier):
    def with_shape(self, *shape: int) -> NoReturn:
        raise NotImplementedError

    def ident(self, spec: str) -> NoReturn:
        raise NotImplementedError


def get_spec(kind: str, byte_size: int) -> SimpleSpecifier:
    return SimpleSpecifier(None, None, kind, byte_size)
