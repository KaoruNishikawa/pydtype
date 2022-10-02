from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Optional

from ..typing import Shape


@dataclass
class Specifier(ABC):

    framework: ClassVar[str]
    reference: ClassVar[str]
    common_name: str

    character: str
    kind: str
    byte_size: int

    @abstractmethod
    def with_shape(self, *shape: int) -> str:
        """Return a specifier for array.

        Notes
        -----
        For string or byte array types, the size of first dimension represents the
        length of the string, i.e., shape=(10, 3, 4) means a 2D array of shape (3, 4)
        filled with 10-character strings.

        """
        ...

    @abstractmethod
    def ident(self, spec: str) -> Optional[Shape]:
        ...
