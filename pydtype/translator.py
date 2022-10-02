from typing import Dict

from .core import Parser
from .frameworks import NumPyParser, StructParser

parser_implementations = [NumPyParser, StructParser]
framework: Dict[str, Parser] = {p.framework.lower(): p for p in parser_implementations}


def translate(specifier: str, from_: str, to: str, strategy: str = "exact") -> str:
    from_, to = from_.lower(), to.lower()
    decoded = framework[from_].decode(specifier)
    try:
        return framework[to].encode(*decoded, strategy=strategy)
    except StopIteration:
        raise ValueError(
            f"Cannot translate {specifier} from {from_} to {to} in {strategy} mode."
        )
