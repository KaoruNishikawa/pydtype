import pytest

from pydtype.frameworks import StructParser


class TestStructParser:
    @pytest.mark.parametrize(
        "specifier, shape, kind, byte_size",
        [
            ("c", tuple(), "char", 1),
            ("b", tuple(), "int", 1),
            ("B", tuple(), "uint", 1),
            ("?", tuple(), "bool", 1),
            ("h", tuple(), "int", 2),
            ("H", tuple(), "uint", 2),
            ("i", tuple(), "int", 4),
            ("I", tuple(), "uint", 4),
            ("l", tuple(), "int", 4),
            ("L", tuple(), "uint", 4),
            ("q", tuple(), "int", 8),
            ("Q", tuple(), "uint", 8),
            ("e", tuple(), "float", 2),
            ("f", tuple(), "float", 4),
            ("d", tuple(), "float", 8),
            ("s", tuple(), "bytes", 1),
        ],
    )
    def test_decode_single_format(self, specifier, shape, kind, byte_size):
        spec, _shape = StructParser.decode(specifier)[0]
        assert spec.kind == kind
        assert spec.byte_size == byte_size
        assert _shape == shape

    @pytest.mark.parametrize(
        "specifier, shape, kind, byte_size",
        [
            ("cc", [tuple(), tuple()], ["char", "char"], [1, 1]),
            ("bB", [tuple(), tuple()], ["int", "uint"], [1, 1]),
            ("?hH", [tuple(), tuple(), tuple()], ["bool", "int", "uint"], [1, 2, 2]),
            ("iIl", [tuple(), tuple(), tuple()], ["int", "uint", "int"], [4, 4, 4]),
            ("qQe", [tuple(), tuple(), tuple()], ["int", "uint", "float"], [8, 8, 2]),
            ("fd", [tuple(), tuple()], ["float", "float"], [4, 8]),
            ("ss", [tuple(), tuple()], ["bytes", "bytes"], [1, 1]),
        ],
    )
    def test_decode_multiple_formats(self, specifier, shape, kind, byte_size):
        for (spec, ashape), _shape, _kind, _byte_size in zip(
            StructParser.decode(specifier), shape, kind, byte_size
        ):
            assert spec.kind == _kind
            assert spec.byte_size == _byte_size
            assert ashape == _shape

    @pytest.mark.parametrize(
        "specifier, shape, kind, byte_size",
        [
            ("11c", (11,), "char", 1),
            ("5b", (5,), "int", 1),
            ("55B", (55,), "uint", 1),
            ("3?", (3,), "bool", 1),
            ("2h", (2,), "int", 2),
            ("5H", (5,), "uint", 2),
            ("13i", (13,), "int", 4),
            ("5I", (5,), "uint", 4),
            ("100l", (100,), "int", 4),
            ("15L", (15,), "uint", 4),
            ("55q", (55,), "int", 8),
            ("5Q", (5,), "uint", 8),
            ("25e", (25,), "float", 2),
            ("51f", (51,), "float", 4),
            ("55d", (55,), "float", 8),
            ("5s", (5,), "bytes", 1),
        ],
    )
    def test_decode_single_array(self, specifier, shape, kind, byte_size):
        spec, _shape = StructParser.decode(specifier)[0]
        assert spec.kind == kind
        assert spec.byte_size == byte_size
        assert _shape == shape

    @pytest.mark.parametrize(
        "specifier, shape, kind, byte_size",
        [
            ("5c2c", [(5,), (2,)], ["char", "char"], [1, 1]),
            ("100b3B", [(100,), (3,)], ["int", "uint"], [1, 1]),
            ("?2h5H", [tuple(), (2,), (5,)], ["bool", "int", "uint"], [1, 2, 2]),
            ("1iI1l", [(1,), tuple(), (1,)], ["int", "uint", "int"], [4, 4, 4]),
            ("q10Qe", [tuple(), (10,), tuple()], ["int", "uint", "float"], [8, 8, 2]),
            ("15f15d", [(15,), (15,)], ["float", "float"], [4, 8]),
            ("1s150s", [(1,), (150,)], ["bytes", "bytes"], [1, 1]),
        ],
    )
    def test_decode_multiple_array(self, specifier, shape, kind, byte_size):
        for (spec, ashape), _shape, _kind, _byte_size in zip(
            StructParser.decode(specifier), shape, kind, byte_size
        ):
            assert spec.kind == _kind
            assert spec.byte_size == _byte_size
            assert ashape == _shape
