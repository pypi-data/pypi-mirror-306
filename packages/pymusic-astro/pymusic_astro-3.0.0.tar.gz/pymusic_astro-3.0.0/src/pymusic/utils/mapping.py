from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

X = typing.TypeVar("X")
Y = typing.TypeVar("Y")

if typing.TYPE_CHECKING:
    from typing import Mapping


class InvertibleMapping(ABC, typing.Generic[X, Y]):
    @abstractmethod
    def forward(self, x: X) -> Y:
        "Map `x` forward to `y = f(x)`"

    @abstractmethod
    def backward(self, y: Y) -> X:
        "Map `y` forward to `x` such that `y = f(x)`"


@dataclass(frozen=True)
class DictBasedMapping(InvertibleMapping[X, Y]):
    forward_dict: Mapping[X, Y]

    @cached_property
    def _backward_dict(self) -> dict[Y, X]:
        d = {y: x for x, y in self.forward_dict.items()}
        if len(d) != len(self.forward_dict):
            raise ValueError("Dictionary mapping is not invertible")
        return d

    def forward(self, x: X) -> Y:
        return self.forward_dict[x]

    def backward(self, y: Y) -> X:
        return self._backward_dict[y]
