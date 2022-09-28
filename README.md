# pydtype

[![PyPI](https://img.shields.io/pypi/v/pydtype.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/pydtype/)
[![Python](https://img.shields.io/pypi/pyversions/pydtype.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/pydtype/)
[![Test](https://img.shields.io/github/workflow/status/KaoruNishikawa/pydtype/Test?logo=github&label=Test&style=flat-square)](https://github.com/KaoruNishikawa/pydtype/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](https://github.com/KaoruNishikawa/pydtype/blob/main/LICENSE)

Translate data type specifiers between common frameworks.

## Features

This library provides:

- Translator of data type spacifier such as [format character in struct](https://docs.python.org/3/library/struct.html#format-characters) and [dtype in Numpy](https://numpy.org/doc/stable/reference/arrays.dtypes.html#specifying-and-constructing-data-types).

## Installation

```shell
pip install pydtype
```

## Usage

To translate struct format `h` (2-byte integer) to Numpy format, run the following script.

```python
>>> import pydtype
>>> pydtype.translate("h", "struct", "numpy")
'i16'
```

---

This library is using [Semantic Versioning](https://semver.org).
