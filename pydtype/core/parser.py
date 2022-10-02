from abc import ABC, abstractmethod
from typing import List, Tuple, Union

from .specifier import Specifier
from ..typing import Shape


class Parser(ABC):
    @classmethod
    @abstractmethod
    def encode(cls, *spec, strategy: str = "exact") -> str:
        ...

    @classmethod
    @abstractmethod
    def decode(cls, spec: str) -> List[Union[str, Tuple[Specifier, Shape]]]:
        ...
