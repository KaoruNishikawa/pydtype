import pytest

from pydtype.frameworks import NumPyParser

from ..conftest import get_spec


class TestStructParser:
    @pytest.mark.parametrize(
        "specifier, shape, kind, byte_size",
        [
            ("?", (), "bool", 1),
            ("b", (), "int", 1),
            ("B", (), "uint", 1),
            ("i1", (), "int", 1),
            ("i2", (), "int", 2),
            ("i4", (), "int", 4),
            ("i8", (), "int", 8),
            ("u1", (), "uint", 1),
            ("u2", (), "uint", 2),
            ("u4", (), "uint", 4),
            ("u8", (), "uint", 8),
            ("f2", (), "float", 2),
            ("f4", (), "float", 4),
            ("f8", (), "float", 8),
            ("f16", (), "float", 16),
            ("c8", (), "complex", 8),
            ("c16", (), "complex", 16),
            ("c32", (), "complex", 32),
            ("m", (), "timedelta", 8),
            ("m8", (), "timedelta", 8),
            ("M", (), "datetime", 8),
            ("M8", (), "datetime", 8),
            ("S", (1,), "bytes", 1),
            ("a", (1,), "bytes", 1),
            ("U", (1,), "str", 1),
            # Unknown
            ("c", (), "char", 1),
        ],
    )
    def test_decode_single_format(self, specifier, shape, kind, byte_size):
        spec, _shape = NumPyParser.decode(specifier)[0]
        assert spec.kind == kind
        assert spec.byte_size == byte_size
        assert _shape == shape

    @pytest.mark.parametrize(
        "specifier, shape, kind, byte_size",
        [
            ("?,?", ((), ()), ["bool", "bool"], [1, 1]),
            ("b,B, i1", ((), (), ()), ["int", "uint", "int"], [1, 1, 1]),
            ("i2,i4,i8", ((), (), ()), ["int", "int", "int"], [2, 4, 8]),
            ("u1, u2", ((), ()), ["uint", "uint"], [1, 2]),
            ("u4,u8", ((), ()), ["uint", "uint"], [4, 8]),
            ("f2, f4", ((), ()), ["float", "float"], [2, 4]),
            ("f8,f16", ((), ()), ["float", "float"], [8, 16]),
            ("c8, c16", ((), ()), ["complex", "complex"], [8, 16]),
            ("c32,m", ((), ()), ["complex", "timedelta"], [32, 8]),
            ("m8, M", ((), ()), ["timedelta", "datetime"], [8, 8]),
            ("M8,S", ((), (1,)), ["datetime", "bytes"], [8, 1]),
            ("a10, U5", ((10,), (5,)), ["bytes", "str"], [1, 1]),
        ],
    )
    def test_decode_multiple_formats(self, specifier, shape, kind, byte_size):
        for (spec, ashape), _shape, _kind, _byte_size in zip(
            NumPyParser.decode(specifier), shape, kind, byte_size
        ):
            assert spec.kind == _kind
            assert spec.byte_size == _byte_size
            assert ashape == _shape

    @pytest.mark.parametrize(
        "specifier, shape, kind, byte_size",
        [
            ("15?", (15,), "bool", 1),
            ("5b", (5,), "int", 1),
            ("55B", (55,), "uint", 1),
            ("2i1", (2,), "int", 1),
            ("(2,5)i2", (2, 5), "int", 2),
            ("(2,5,3)i4", (2, 5, 3), "int", 4),
            ("(2,5,3,4)i8", (2, 5, 3, 4), "int", 8),
            ("(2,5,3,4,5)u1", (2, 5, 3, 4, 5), "uint", 1),
            ("(2, 6)u2", (2, 6), "uint", 2),
            ("(2, 6, 7)u4", (2, 6, 7), "uint", 4),
            ("3u8", (3,), "uint", 8),
            ("7f2", (7,), "float", 2),
            ("(2,5)f4", (2, 5), "float", 4),
            ("(2,5,3) f8", (2, 5, 3), "float", 8),
            ("(2, 5, 3, 4)f16", (2, 5, 3, 4), "float", 16),
            ("(3,) c8", (3,), "complex", 8),
            ("(3, 4) c16", (3, 4), "complex", 16),
            ("(3, 4, 5)c32", (3, 4, 5), "complex", 32),
            ("(3,     )m", (3,), "timedelta", 8),
            ("(3,    4)    m8", (3, 4), "timedelta", 8),
            ("(3, 4, 5)M", (3, 4, 5), "datetime", 8),
            ("(3, 4, 5, 6)M8", (3, 4, 5, 6), "datetime", 8),
            ("(3, 7)S", (1, 3, 7), "bytes", 1),
            ("(3, 7)a11", (11, 3, 7), "bytes", 1),
            ("(3,)U", (1, 3), "str", 1),
        ],
    )
    def test_decode_single_array(self, specifier, shape, kind, byte_size):
        spec, _shape = NumPyParser.decode(specifier)[0]
        assert spec.kind == kind
        assert spec.byte_size == byte_size
        assert _shape == shape

    @pytest.mark.parametrize(
        "specifier, shape, kind, byte_size",
        [
            ("12?,?", ((12,), ()), ["bool", "bool"], [1, 1]),
            ("b,B, 2i1", ((), (), (2,)), ["int", "uint", "int"], [1, 1, 1]),
            ("2i2,3i4,4i8", ((2,), (3,), (4,)), ["int", "int", "int"], [2, 4, 8]),
            ("(1,)u1, 9u2", ((1,), (9,)), ["uint", "uint"], [1, 2]),
            ("(2,4)u4,u8", ((2, 4), ()), ["uint", "uint"], [4, 8]),
            ("(5, 9)f2, (7, 9)f4", ((5, 9), (7, 9)), ["float", "float"], [2, 4]),
            ("(5,   )f8, (3,5)    f16", ((5,), (3, 5)), ["float", "float"], [8, 16]),
            ("c8,    (3,)    c16", ((), (3,)), ["complex", "complex"], [8, 16]),
            ("3c32,  4   m", ((3,), (4,)), ["complex", "timedelta"], [32, 8]),
            ("(2,2,2)m8, 5M", ((2, 2, 2), (5,)), ["timedelta", "datetime"], [8, 8]),
            ("5M8,(7,9)S", ((5,), (1, 7, 9)), ["datetime", "bytes"], [8, 1]),
            ("90a10, (7,5)U5", ((10, 90), (5, 7, 5)), ["bytes", "str"], [1, 1]),
        ],
    )
    def test_decode_multiple_array(self, specifier, shape, kind, byte_size):
        for (spec, ashape), _shape, _kind, _byte_size in zip(
            NumPyParser.decode(specifier), shape, kind, byte_size
        ):
            assert spec.kind == _kind
            assert spec.byte_size == _byte_size
            assert ashape == _shape

    @pytest.mark.parametrize(
        "spec, expected",
        [
            ([get_spec("char", 1), ()], "c"),
            ([get_spec("int", 2), ()], "i2"),
            ([get_spec("int", 4), ()], "i4"),
            ([get_spec("int", 8), ()], "i8"),
            ([get_spec("uint", 2), ()], "u2"),
            ([get_spec("uint", 4), ()], "u4"),
            ([get_spec("uint", 8), ()], "u8"),
            ([get_spec("float", 2), ()], "f2"),
            ([get_spec("float", 4), ()], "f4"),
            ([get_spec("float", 8), ()], "f8"),
            ([get_spec("float", 16), ()], "f16"),
            ([get_spec("complex", 8), ()], "c8"),
            ([get_spec("complex", 16), ()], "c16"),
            ([get_spec("complex", 32), ()], "c32"),
            ([get_spec("timedelta", 8), ()], "m"),
            ([get_spec("datetime", 8), ()], "M"),
            ([get_spec("bytes", 1), (1,)], "S1"),
            ([get_spec("str", 1), (2,)], "U2"),
        ],
    )
    def test_encode_single_format(self, spec, expected):
        assert NumPyParser.encode(spec) == expected

    @pytest.mark.parametrize(
        "spec, expected",
        [
            ([(get_spec("char", 1), ()), (get_spec("char", 1), ())], "c,c"),
            ([(get_spec("int", 2), ()), (get_spec("int", 4), ())], "i2,i4"),
            ([(get_spec("int", 8), ()), (get_spec("uint", 2), ())], "i8,u2"),
            ([(get_spec("uint", 4), ()), (get_spec("uint", 8), ())], "u4,u8"),
            (
                [(get_spec("float", 2), ()), (get_spec("float", 4), ())],
                "f2,f4",
            ),
            (
                [(get_spec("float", 8), ()), (get_spec("float", 16), ())],
                "f8,f16",
            ),
            (
                [(get_spec("complex", 8), ()), (get_spec("complex", 16), ())],
                "c8,c16",
            ),
            (
                [(get_spec("complex", 32), ()), (get_spec("timedelta", 8), ())],
                "c32,m",
            ),
            (
                [(get_spec("datetime", 8), ()), (get_spec("bytes", 1), (1,))],
                "M,S1",
            ),
            ([(get_spec("str", 1), (2,)), (get_spec("str", 1), (3,))], "U2,U3"),
        ],
    )
    def test_encode_multiple_format(self, spec, expected):
        assert NumPyParser.encode(*spec) == expected

    @pytest.mark.parametrize(
        "spec, expected",
        [
            ([get_spec("char", 1), (3,)], "(3,)c"),
            ([get_spec("int", 2), (3, 5)], "(3,5)i2"),
            ([get_spec("int", 4), (3, 5, 7)], "(3,5,7)i4"),
            ([get_spec("int", 8), (2,)], "(2,)i8"),
            ([get_spec("uint", 2), (2, 4)], "(2,4)u2"),
            ([get_spec("uint", 4), (2, 4, 6)], "(2,4,6)u4"),
            ([get_spec("uint", 8), (3,)], "(3,)u8"),
            ([get_spec("float", 2), (3, 5)], "(3,5)f2"),
            ([get_spec("float", 4), (3, 5, 7)], "(3,5,7)f4"),
            ([get_spec("float", 8), (2,)], "(2,)f8"),
            ([get_spec("float", 16), (2, 4)], "(2,4)f16"),
            ([get_spec("complex", 8), (2, 4, 6)], "(2,4,6)c8"),
            ([get_spec("complex", 16), (1234,)], "(1234,)c16"),
            ([get_spec("complex", 32), (53, 31)], "(53,31)c32"),
            ([get_spec("timedelta", 8), (3,)], "(3,)m"),
            ([get_spec("datetime", 8), (31,)], "(31,)M"),
            ([get_spec("bytes", 1), (3, 4)], "(4,)S3"),
            ([get_spec("str", 1), (90, 3, 4)], "(3,4)U90"),
        ],
    )
    def test_encode_single_array(self, spec, expected):
        assert NumPyParser.encode(spec) == expected

    @pytest.mark.parametrize(
        "spec, expected",
        [
            ([(get_spec("char", 1), (3,)), (get_spec("char", 1), (7,))], "(3,)c,(7,)c"),
            (
                [(get_spec("int", 2), (3, 5)), (get_spec("int", 4), (7,))],
                "(3,5)i2,(7,)i4",
            ),
            (
                [(get_spec("int", 8), (3,)), (get_spec("uint", 2), (7, 9))],
                "(3,)i8,(7,9)u2",
            ),
            (
                [(get_spec("uint", 4), (3, 5)), (get_spec("uint", 8), (7, 9))],
                "(3,5)u4,(7,9)u8",
            ),
            (
                [(get_spec("float", 2), (3, 5)), (get_spec("float", 4), ())],
                "(3,5)f2,f4",
            ),
            (
                [(get_spec("float", 8), (3, 5)), (get_spec("float", 16), (7, 9, 9))],
                "(3,5)f8,(7,9,9)f16",
            ),
            (
                [(get_spec("complex", 8), (5,)), (get_spec("complex", 16), (7, 9))],
                "(5,)c8,(7,9)c16",
            ),
            (
                [(get_spec("complex", 32), (5,)), (get_spec("timedelta", 8), (7, 9))],
                "(5,)c32,(7,9)m",
            ),
            (
                [(get_spec("datetime", 8), (3, 7)), (get_spec("bytes", 1), (7, 9))],
                "(3,7)M,(9,)S7",
            ),
            (
                [(get_spec("str", 1), (3, 7, 9)), (get_spec("str", 1), (7, 9))],
                "(7,9)U3,(9,)U7",
            ),
        ],
    )
    def test_encode_multiple_array(self, spec, expected):
        assert NumPyParser.encode(*spec) == expected
