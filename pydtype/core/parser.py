from abc import ABC, abstractmethod
from typing import ClassVar, List, Tuple, Union

from .specifier import Specifier
from ..typing import Shape


class Parser(ABC):

    framework: ClassVar[str]

    @classmethod
    @abstractmethod
    def encode(cls, *spec: Tuple[Specifier, Shape], strategy: str = "exact") -> str:
        ...

    @classmethod
    @abstractmethod
    def decode(cls, spec: str) -> List[Union[str, Tuple[Specifier, Shape]]]:
        ...
