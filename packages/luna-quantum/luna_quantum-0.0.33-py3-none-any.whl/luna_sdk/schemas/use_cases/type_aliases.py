from typing import Dict, Tuple, Union

Node = Union[int, str]

NestedDictGraph = Dict[Node, Dict[Node, Dict[str, float]]]

NestedDictIntGraph = Dict[int, Dict[int, Dict[str, float]]]

CalculusLiteral = Tuple[int, bool]

Clause = Tuple[CalculusLiteral, ...]
