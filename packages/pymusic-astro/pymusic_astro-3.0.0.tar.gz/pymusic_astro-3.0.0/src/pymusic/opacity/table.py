from __future__ import annotations

import typing

import numpy as np

from ..eos.table import Table

if typing.TYPE_CHECKING:
    from typing import Mapping


class NumpyNdimArrayTable(Table):
    """An n-dimensional table based on actual Numpy arrays
    (an n-dim version of eos::table::NumpyArrayTable)
    """

    def __init__(
        self,
        arrays: Mapping[str, np.ndarray],
        coords: Mapping[str, np.ndarray],
    ):
        self._arrays = arrays
        self._coords = coords
        # Try to catch annoying shape problems early on
        assert all(a.ndim == 1 for a in self._coords.values())
        shape = tuple(a.size for a in self._coords.values())
        assert all(a.shape == shape for a in self._arrays.values())

    def arrays(self) -> Mapping[str, np.ndarray]:
        return self._arrays

    def coords(self) -> Mapping[str, np.ndarray]:
        return self._coords
