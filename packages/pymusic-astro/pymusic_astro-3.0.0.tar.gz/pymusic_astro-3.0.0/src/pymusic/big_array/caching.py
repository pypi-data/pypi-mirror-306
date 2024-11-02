"""
:mod:`.caching`: caching operations on :class:`.BigArray` objects
=================================================================
"""

from __future__ import annotations

import typing

from .array import BigArray, SummedArray, T_co, TakeArray

if typing.TYPE_CHECKING:
    from typing import Sequence

    from numpy.typing import NDArray

    from .index import IndexNd


class CachedArray(BigArray[T_co]):
    """A simple decorator caching the results of :meth:`index` and
    :meth:`array` in memory.

    The array index and data are still computed lazily, but are remembered
    between method calls and served directly once precomputed.
    """

    def __init__(self, array: BigArray[T_co]):
        """:param array: array to cache"""
        self._array = array

        self._cached_index: IndexNd | None = None
        self._cached_array: NDArray[T_co] | None = None

    def _index(self) -> IndexNd:
        if self._cached_index is None:
            self._cached_index = self._array.index
        return self._cached_index

    def array(self) -> NDArray[T_co]:
        if self._cached_array is None:
            self._cached_array = self._array.array()
        return self._cached_array

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)
