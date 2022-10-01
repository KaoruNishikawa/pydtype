"""Format characters in struct, Python standard library."""

import re
from typing import List, NoReturn, Optional, Tuple, Union

from ..core import Parser, Specifier, Types
from ..typing import Shape


class StructFormat(Specifier):

    framework = "struct"
    reference = "https://docs.python.org/3/library/struct.html#format-characters"

    def with_shape(self, *shape) -> str:
        if len(shape) == 0:
            return self.character
        if len(shape) > 1:
            raise ValueError(f"Multi-dimensional array (shape={shape}) isn't supported")
        return self.character * shape[0]

    def get(self) -> NoReturn:
        raise NotImplementedError(
            "Struct doesn't implement Python objects that represent individual types."
        )

    def ident(self, spec: str) -> Optional[Shape]:
        parsed = re.findall(rf"^(\d*){re.escape(self.character)}$", spec)
        if len(parsed) == 0:
            return
        if parsed[0] == "":
            return tuple()
        return tuple(map(int, parsed))


class StructTypes(Types):
    types = (
        StructFormat("pad byte", "x", None, None),
        StructFormat("char", "c", "char", 1),
        StructFormat("signed char", "b", "int", 1),
        StructFormat("unsigned char", "B", "uint", 1),
        StructFormat("_Bool", "?", "bool", 1),
        StructFormat("short", "h", "int", 2),
        StructFormat("unsigned short", "H", "uint", 2),
        StructFormat("int", "i", "int", 4),
        StructFormat("unsigned int", "I", "uint", 4),
        StructFormat("long", "l", "int", 4),
        StructFormat("unsigned long", "L", "uint", 4),
        StructFormat("long long", "q", "int", 8),
        StructFormat("unsigned long long", "Q", "uint", 8),
        StructFormat("ssize_t", "n", "int", None),
        StructFormat("size_t", "N", "uint", None),
        StructFormat("half precision", "e", "float", 2),
        StructFormat("float", "f", "float", 4),
        StructFormat("double", "d", "float", 8),
        StructFormat("string", "s", "bytes", 1),
        StructFormat("char[]", "p", "bytes", None),
        StructFormat("void", "P", "int", None),
    )


class StructParser(Parser):
    @classmethod
    def encode(cls, *spec, strategy: str = "exact") -> str:
        endian = ""
        if isinstance(spec[0], str):
            endian, *spec = spec

        formats = [
            StructTypes.search(s.kind, s.byte_size, strategy).with_shape(*shape)
            for s, *shape in spec
        ]
        return endian + "".join(formats)

    @classmethod
    def decode(cls, spec: str) -> List[Union[str, Tuple[Specifier, Shape]]]:
        split = re.findall(r"([@=<>!]+|\d*[\w\?])", spec)
        endian = None
        if split[0] in "@=<>!":
            endian, *split = split
        specs = [StructTypes.find(s) for s in split]

        if endian is None:
            return specs
        return [endian] + specs
