import pytest

import pydtype


class TestTranslate:
    @pytest.mark.parametrize(
        "input_,from_,to,expected",
        [
            ("?", "struct", "numpy", "?"),
            ("?", "numpy", "struct", "?"),
            ("S1", "numpy", "struct", "1s"),
            ("e", "struct", "numpy", "f2"),
            ("5s", "struct", "numpy", "S5"),
            ("h", "struct", "numpy", "i2"),
            ("f8", "numpy", "struct", "d"),
            ("u8", "numpy", "struct", "Q"),
            ("Q", "struct", "struct", "Q"),
        ],
    )
    def test_translate_single_format(self, input_, from_, to, expected):
        assert pydtype.translate(input_, from_, to) == expected

    @pytest.mark.parametrize(
        "input_,from_,to,expected",
        [
            ("??", "struct", "numpy", "?,?"),
            ("?,i2", "numpy", "struct", "?h"),
            ("S1,a90", "numpy", "struct", "1s90s"),
            ("e9s", "struct", "numpy", "f2,S9"),
            ("5s3s", "struct", "numpy", "S5,S3"),
            ("hqd", "struct", "numpy", "i2,i8,f8"),
            ("f8,S7", "numpy", "struct", "d7s"),
        ],
    )
    def test_translate_multiple_formats(self, input_, from_, to, expected):
        assert pydtype.translate(input_, from_, to) == expected

    @pytest.mark.parametrize(
        "input_,from_,to,expected",
        [
            ("5?", "struct", "numpy", "(5,)?"),
            ("(5,)?", "numpy", "struct", "5?"),
            ("7i", "struct", "numpy", "(7,)i4"),
            ("(7,)i8", "numpy", "struct", "7q"),
            ("(7,)u8", "numpy", "struct", "7Q"),
            ("(3,)f8", "numpy", "struct", "3d"),
            ("(3,)S2", "numpy", "struct", "2s2s2s"),
            ("(3,)S10", "numpy", "numpy", "(3,)S10"),
        ],
    )
    def test_translate_single_array(self, input_, from_, to, expected):
        assert pydtype.translate(input_, from_, to) == expected

    @pytest.mark.parametrize(
        "input_,from_,to,expected",
        [
            ("5?3?", "struct", "numpy", "(5,)?,(3,)?"),
            ("(5,)?(3,)?", "numpy", "struct", "5?3?"),
            ("7i3d", "struct", "numpy", "(7,)i4,(3,)f8"),
            ("(7,)i8,(3,)f8", "numpy", "struct", "7q3d"),
            ("(90,)u8,f8", "numpy", "struct", "90Qd"),
            ("(3,)f8,(3,)S2", "numpy", "struct", "3d2s2s2s"),
            ("5s7q", "struct", "numpy", "S5,(7,)i8"),
            ("(3,)S10,(3,)S10", "numpy", "numpy", "(3,)S10,(3,)S10"),
        ],
    )
    def test_translate_multiple_array(self, input_, from_, to, expected):
        assert pydtype.translate(input_, from_, to) == expected
