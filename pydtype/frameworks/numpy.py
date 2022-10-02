"""dtype in NumPy."""

import ctypes
import re
from typing import List, Optional, Tuple, Union

from ..core import Parser, Specifier, Types
from ..typing import Shape


class NumPyFormat(Specifier):

    framework = "numpy"
    reference = "https://numpy.org/doc/stable/reference/arrays.dtypes.html"

    def with_shape(self, *shape) -> str:
        if len(shape) == 0:
            return self.character
        if self.character in "SaU":
            if len(shape) == 1:
                return f"{self.character}{shape[0]}"
            if len(shape) == 2:
                return f"({shape[1]},){self.character}{shape[0]}"
            return f"({','.join(map(str, shape[1:]))}){self.character}{shape[0]}"
        else:
            if len(shape) == 1:
                return f"({shape[0]},){self.character}"
            return f"({','.join(map(str, shape))}){self.character}"

    def ident(self, spec: str) -> Optional[Shape]:
        if self.character in "SaU":
            match_str = rf"^\(?([\d,\s]*)\)?\s*{re.escape(self.character)}(\d*)$"
            parsed = re.findall(match_str, spec)
            parsed = [(p.strip().rstrip(","), _len) for p, _len in parsed]
            if len(parsed) == 0:
                return
            shape, length = parsed[0]
            length = int(length) if length else 1
            if parsed[0][0] == "":
                return (int(length),)
            return tuple(map(int, [length, *shape.split(",")]))
        else:
            match_str = rf"^\(?([\d,\s]*)\)?\s*{re.escape(self.character)}$"
            parsed = re.findall(match_str, spec)
            parsed = [p.strip().rstrip(",") for p in parsed]
            if len(parsed) == 0:
                return
            if parsed[0] == "":
                return tuple()
            return tuple(map(int, parsed[0].split(",")))


class NumPyTypes(Types):

    framework = "numpy"
    types = (
        NumPyFormat("bool", "?", "bool", 1),
        NumPyFormat("int8", "b", "int", 1),
        NumPyFormat("uint8", "B", "uint", 1),
        NumPyFormat("int8", "i1", "int", 1),
        NumPyFormat("int16", "i2", "int", 2),
        NumPyFormat("int32", "i4", "int", 4),
        NumPyFormat("int64", "i8", "int", 8),
        NumPyFormat("uint8", "u1", "uint", 1),
        NumPyFormat("uint16", "u2", "uint", 2),
        NumPyFormat("uint32", "u4", "uint", 4),
        NumPyFormat("uint64", "u8", "uint", 8),
        NumPyFormat("float16", "f2", "float", 2),
        NumPyFormat("float32", "f4", "float", 4),
        NumPyFormat("float64", "f8", "float", 8),
        NumPyFormat("float128", "f16", "float", 16),
        NumPyFormat("complex64", "c8", "complex", 8),
        NumPyFormat("complex128", "c16", "complex", 16),
        NumPyFormat("complex256", "c32", "complex", 32),
        NumPyFormat("timedelta", "m", "timedelta", 8),
        NumPyFormat("timedelta", "m8", "timedelta", 8),
        NumPyFormat("datetime", "M", "datetime", 8),
        NumPyFormat("datetime", "M8", "datetime", 8),
        NumPyFormat("object", "O", None, None),
        NumPyFormat("string", "S", "bytes", 1),
        NumPyFormat("string", "a", "bytes", 1),
        NumPyFormat("unicode", "U", "str", 1),
        NumPyFormat("void", "V", None, None),
        # ctypes dtypes
        NumPyFormat("c_short", "h", "int", ctypes.sizeof(ctypes.c_short)),
        NumPyFormat("c_ushort", "H", "uint", ctypes.sizeof(ctypes.c_ushort)),
        NumPyFormat("c_long", "l", "int", ctypes.sizeof(ctypes.c_long)),
        NumPyFormat("c_ulong", "L", "uint", ctypes.sizeof(ctypes.c_ulong)),
        NumPyFormat("c_int", "i", "int", ctypes.sizeof(ctypes.c_int)),
        NumPyFormat("c_uint", "I", "uint", ctypes.sizeof(ctypes.c_uint)),
        NumPyFormat("c_float", "f", "float", ctypes.sizeof(ctypes.c_float)),
        NumPyFormat("c_double", "d", "float", ctypes.sizeof(ctypes.c_double)),
        NumPyFormat("c_longdouble", "g", "float", ctypes.sizeof(ctypes.c_longdouble)),
        # Unknown
        NumPyFormat("c", "c", "char", 1),
        NumPyFormat("p", "p", "int", 8),
        NumPyFormat("P", "P", "uint", 8),
        NumPyFormat("bool", "b1", "bool", 1),
    )


class NumPyParser(Parser):

    framework = "numpy"

    @classmethod
    def encode(cls, *spec, strategy: str = "exact") -> str:
        endian = ""
        if isinstance(spec[0], str):
            endian, *spec = spec

        formats = [
            NumPyTypes.search(s.kind, s.byte_size, strategy).with_shape(*shape)
            for s, shape in spec
        ]
        return endian + ",".join(formats)

    @classmethod
    def decode(cls, spec: str) -> List[Union[str, Tuple[Specifier, Shape]]]:
        split = re.findall(r"\([\d,\s]*\)\s*[a-zA-Z\?]\d*|[\d\s]*[a-zA-Z\?]\d*", spec)
        endian = None
        if split[0] in "=<>|":
            endian, *split = split
        specs = [NumPyTypes.find(s) for s in split]

        if endian is None:
            return specs
        return [endian] + specs
