"""Format characters in struct, Python standard library."""

import re
from typing import List, Optional, Tuple, Union

from ..core import Parser, Specifier, Types
from ..typing import Shape


class StructFormat(Specifier):

    framework = "struct"
    reference = "https://docs.python.org/3/library/struct.html#format-characters"

    def with_shape(self, *shape: int) -> str:
        if len(shape) == 0:
            return self.character
        if "s" in self.character:
            if len(shape) > 2:
                raise ValueError(
                    f"Multi-dimensional array (shape={shape[1:]}) isn't supported"
                )
            if len(shape) == 1:
                return f"{shape[0]}s"
            return f"{shape[0]}{self.character}" * shape[1]
        else:
            if len(shape) > 1:
                raise ValueError(
                    f"Multi-dimensional array (shape={shape}) isn't supported"
                )
            return f"{shape[0]}{self.character}"

    def ident(self, spec: str) -> Optional[Shape]:
        parsed = re.findall(rf"^(\d*){re.escape(self.character)}$", spec)
        if len(parsed) == 0:
            return
        if parsed[0] == "":
            return (1,) if "s" in spec else tuple()
        return tuple(map(int, parsed))


class StructTypes(Types):

    framework = "struct"
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

    framework = "struct"

    @classmethod
    def encode(cls, *spec: Tuple[Specifier, Shape], strategy: str = "exact") -> str:
        endian = ""
        if isinstance(spec[0], str):
            endian, *spec = spec

        formats = [
            StructTypes.search(s.kind, s.byte_size, strategy).with_shape(*shape)
            for s, shape in spec
        ]
        return endian + "".join(formats)

    @classmethod
    def decode(cls, spec: str) -> List[Union[str, Tuple[Specifier, Shape]]]:
        split = re.findall(r"([@=<>!]+|\d*[a-zA-Z\?])", spec)
        endian = None
        if split[0] in "@=<>!":
            endian, *split = split
        specs = [StructTypes.find(s) for s in split]

        if endian is None:
            return specs
        return [endian] + specs
