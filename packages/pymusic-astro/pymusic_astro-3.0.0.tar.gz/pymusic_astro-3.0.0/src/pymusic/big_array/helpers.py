from __future__ import annotations

import dataclasses
import time
import typing

import pandas as pd

from ..utils.mapping import InvertibleMapping
from .array import BigArray, T_co
from .index import ItemsIndex1d

if typing.TYPE_CHECKING:
    from typing import Sequence

    from numpy.typing import NDArray

    from .index import IndexNd


@dataclasses.dataclass(frozen=True)
class _Instant:
    wall: float
    process: float

    @staticmethod
    def now() -> _Instant:
        return _Instant(time.perf_counter(), time.process_time())

    def __sub__(self, other: _Instant) -> _Duration:
        return _Duration(self.wall - other.wall, self.process - other.process)


@dataclasses.dataclass(frozen=True)
class _Duration:
    wall: float
    process: float

    def __add__(self, other: _Duration) -> _Duration:
        return _Duration(self.wall + other.wall, self.process + other.process)


class Timer:
    def __init__(self) -> None:
        self._timer = _Duration(0.0, 0.0)
        self._t_start: _Instant | None = None

    def start(self) -> None:
        assert self._t_start is None
        self._t_start = _Instant.now()

    def stop(self) -> None:
        assert self._t_start is not None
        self._timer += _Instant.now() - self._t_start
        self._t_start = None

    @property
    def t_wall(self) -> float:
        """The total wall time accumulated by the timer."""
        return self._timer.wall

    @property
    def t_process(self) -> float:
        """The total CPU time accumulated by the timer."""
        return self._timer.process


class TimedArray(BigArray[T_co]):
    """An array object with timers around its main methods"""

    def __init__(self, array: BigArray[T_co]):
        """:param array: array object to decorate and measure timings for"""
        self._array = array
        self._t_index = Timer()
        self._t_array = Timer()
        self._t_take = Timer()
        self._t_sum = Timer()

    def _index(self) -> IndexNd:
        self._t_index.start()
        result = self._array.index
        self._t_index.stop()
        return result

    def array(self) -> NDArray[T_co]:
        self._t_array.start()
        result = self._array.array()
        self._t_array.stop()
        return result

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        self._t_take.start()
        result = self._array.take(labels, axis)
        self._t_take.stop()
        return result

    def sum(self, axis: str) -> BigArray[T_co]:
        self._t_sum.start()
        result = self._array.sum(axis)
        self._t_sum.stop()
        return result

    def timings(self) -> pd.DataFrame:
        """:return: timings (in seconds) for each of the instrumented methods"""
        timers = (
            ("index", self._t_index),
            ("array", self._t_array),
            ("take", self._t_take),
            ("sum", self._t_sum),
        )
        df = pd.DataFrame(index=pd.Index([nm for (nm, _) in timers], name="operation"))
        df["wall_seconds"] = [t.t_wall for (_, t) in timers]
        df["process_seconds"] = [t.t_process for (_, t) in timers]
        df["wait_seconds"] = df["wall_seconds"] - df["process_seconds"]
        return df


@dataclasses.dataclass
class ArrayWithRemappedLabels(BigArray[T_co]):
    """An array whose labels along a given axis are obtained by remapping those
    of a source array, using an InvertibleMapping.

    This allows e.g. renaming variables, by remapping labels along the "var"
    axis, etc.
    """

    source: BigArray[T_co]
    axis: str
    # TYPE SAFETY: do not specify types over which InvertibleMapping are
    # generic since those are invariants and cannot be known until runtime
    # as labels can be anything.
    mapping: InvertibleMapping

    def _index(self) -> IndexNd:
        source_idx = self.source.index
        source_idx_ax = source_idx.index1d(self.axis)
        new_idx_ax = ItemsIndex1d(
            self.axis,
            [self.mapping.forward(src_lbl) for src_lbl in source_idx_ax.labels],
        )
        return source_idx.replace(self.axis, new_idx_ax)

    def array(self) -> NDArray[T_co]:
        return self.source.array()

    def _with_array(self, array: BigArray[T_co]) -> ArrayWithRemappedLabels[T_co]:
        return ArrayWithRemappedLabels(array, self.axis, self.mapping)

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        if axis == self.axis:
            # Take the preimage of `labels` in the source array, and remap the result
            src_labels = [self.mapping.backward(lbl) for lbl in labels]
            return self._with_array(self.source.take(src_labels, axis))
        else:
            return self._with_array(self.source.take(labels, axis))

    def sum(self, axis: str) -> BigArray[T_co]:
        if axis == self.axis:
            # Remapped axis disappears after the sum, so we have simply
            return self.source.sum(axis)
        else:
            # Sum crosses is along unchanged dimension
            return ArrayWithRemappedLabels(
                self.source.sum(axis), self.axis, self.mapping
            )
