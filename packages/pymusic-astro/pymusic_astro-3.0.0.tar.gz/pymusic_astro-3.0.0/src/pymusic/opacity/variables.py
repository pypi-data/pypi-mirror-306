from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

import numpy as np

ArrayOrFloat = TypeVar("ArrayOrFloat", np.ndarray, float)


@dataclass(frozen=True)
class DTState(Generic[ArrayOrFloat]):
    rho: ArrayOrFloat
    t: ArrayOrFloat

    @property
    def r(self) -> ArrayOrFloat:
        return self.rho - 3.0 * self.t + 18.0
