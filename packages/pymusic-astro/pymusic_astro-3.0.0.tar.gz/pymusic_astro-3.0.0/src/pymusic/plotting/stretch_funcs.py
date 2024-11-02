from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

import matplotlib.colors as colors
import numpy as np

if typing.TYPE_CHECKING:
    from typing import Sequence, TypeVar

    F = TypeVar("F", float, np.ndarray)


class StretchFunc(ABC):
    @abstractmethod
    def forward(self, x: F) -> F:
        """Apply stretch function to value"""

    @abstractmethod
    def inverse(self, x: F) -> F:
        """Apply inverse stretch function to value"""

    @abstractmethod
    def scaled(self, factor: float) -> StretchFunc:
        """Return the StretchFunc obtained by rescaling this StretchFunc"""

    def __call__(self, x: F) -> F:
        return self.forward(x)

    def as_mpl_norm(self) -> colors.FuncNorm:
        vmin, vmax = self.bounds()
        return colors.FuncNorm((self.forward, self.inverse), vmin=vmin, vmax=vmax)

    def ticks(self, count: int, digits: int = 1) -> Sequence[float]:
        def round(x: float) -> float:
            if x == 0.0:
                return 0.0
            xmag = 10.0 ** np.floor(np.log10(np.abs(x)))
            return np.round(x / xmag, digits - 1) * xmag

        return [
            round(x) for x in self.inverse(np.linspace(-1.0, 1.0, count, endpoint=True))
        ]

    def bounds(self) -> tuple[float, float]:
        return self.inverse(-1.0), self.inverse(1.0)


@dataclass(frozen=True)
class LinearStretch(StretchFunc):
    scale: float

    def forward(self, x: F) -> F:
        return x / self.scale

    def inverse(self, y: F) -> F:
        return y * self.scale

    def scaled(self, factor: float) -> StretchFunc:
        return LinearStretch(scale=self.scale * factor)


@dataclass(frozen=True)
class ArcsinhStretch(StretchFunc):
    lin_scale: float
    sat_scale: float

    @property
    def _s(self) -> float:
        return np.arcsinh(self.sat_scale / self.lin_scale)

    def forward(self, x: F) -> F:
        return np.arcsinh(x / self.lin_scale) / self._s

    def inverse(self, y: F) -> F:
        return np.sinh(y * self._s) * self.lin_scale

    def scaled(self, factor: float) -> StretchFunc:
        return ArcsinhStretch(
            lin_scale=self.lin_scale * factor, sat_scale=self.sat_scale * factor
        )
