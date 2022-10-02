from typing import Any, Callable, ClassVar, Sequence, Tuple

from .specifier import Specifier
from ..typing import Shape


class Types:

    types: ClassVar[Sequence[Specifier]]
    framework: ClassVar[str]

    @classmethod
    def search(cls, kind: str, byte_size: int, strategy: str = "exact") -> Specifier:
        same_kind = [x for x in cls.types if x.kind == kind]
        return match(byte_size, same_kind, lambda x: x.byte_size, strategy)

    @classmethod
    def find(cls, spec: str) -> Tuple[Specifier, Shape]:
        for t in cls.types:
            shape = t.ident(spec)
            if shape is not None:
                return t, shape
        raise ValueError(f"Specifier {spec} is not supported")


def match(
    target: Any,
    candidates: Sequence[Any],
    extractor: Callable[[Any], Any] = lambda x: x,
    strategy: str = "exact",
) -> Any:
    strategy = strategy.lower()

    if strategy == "exact":
        return next(x for x in candidates if extractor(x) == target)
    if strategy == "closest":
        return sorted(candidates, key=lambda x: abs(extractor(x) - target))[0]
    if strategy == "leaky":
        _candidates = filter(lambda x: extractor(x) <= target, candidates)
        return sorted(_candidates, key=lambda x: abs(extractor(x) - target))[0]
    if strategy == "contain":
        _candidates = filter(lambda x: extractor(x) >= target, candidates)
        return sorted(_candidates, key=lambda x: abs(extractor(x) - target))[0]
