from abc import ABC, abstractmethod
from typing import List, Tuple, Union

from ..typing import Shape


class Parser(ABC):
    @classmethod
    @abstractmethod
    def encode(cls, *spec) -> str:
        ...

    @classmethod
    @abstractmethod
    def decode(cls, spec: str) -> List[Union[str, Tuple[str, int, Shape]]]:
        ...
