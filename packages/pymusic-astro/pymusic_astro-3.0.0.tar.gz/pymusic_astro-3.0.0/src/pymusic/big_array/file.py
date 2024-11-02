from __future__ import annotations

import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Generic

from .array import (
    BigArray,
    IndexNd,
    ItemsIndex1d,
    NumpyArray,
    SummedArray,
    T_co,
    TakeArray,
)
from .caching import CachedArray

if TYPE_CHECKING:
    from typing import Sequence

    from numpy.typing import NDArray


class ArrayFile(ABC, Generic[T_co]):
    @property
    @abstractmethod
    def path(self) -> Path:
        "Path to the file"

    @abstractmethod
    def read(self) -> NumpyArray[T_co]:
        "Read the file and return its array data as a NumpyArray"

    @abstractmethod
    def write(self, array: BigArray[T_co]) -> None:
        "Write the given `array` to the file"


@dataclass(frozen=True)
class ArrayFromFile(BigArray[T_co]):
    """Array lazily read from an ArrayFile"""

    array_file: ArrayFile[T_co]

    @cached_property
    def _arr(self) -> NumpyArray[T_co]:
        return self.array_file.read()

    # -- BigArray interface

    def _index(self) -> IndexNd:
        return self._arr.index

    def array(self) -> NDArray[T_co]:
        return self._arr.array()

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)


@dataclass
class FileCachedArray(BigArray[T_co]):
    """An array cached to an ArrayFile"""

    array_: BigArray[T_co]
    cache_array_file: ArrayFile[T_co]

    def __post_init__(self) -> None:
        self._cache: CachedArray | None = None

    @property
    def _path(self) -> Path:
        return self.cache_array_file.path

    def _cached(self) -> BigArray[T_co]:
        if self._cache is None:
            if not self._path.exists():
                self._path.parent.mkdir(parents=True, exist_ok=True)
                self.cache_array_file.write(self.array_)
            self._cache = CachedArray(self.cache_array_file.read())
        return self._cache

    # -- BigArray interface

    def _index(self) -> IndexNd:
        return self._cached().index

    def array(self) -> NDArray[T_co]:
        return self._cached().array()

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)


@dataclass(frozen=True)
class PickleArrayFile(ArrayFile[T_co]):
    file_name: str

    @property
    def path(self) -> Path:
        return Path(self.file_name)

    def write(self, array: BigArray[T_co]) -> None:
        # Pickle a dictionary representation of the array
        index_data = {ax: array.labels_along_axis(ax) for ax in array.axes}
        array_data = array.array()
        d = dict(index=index_data, array=array_data)
        with open(self.file_name, "wb") as f:
            pickle.dump(d, f)

    def read(self) -> NumpyArray[T_co]:
        with open(self.file_name, "rb") as f:
            d = pickle.load(f)

        index = IndexNd([ItemsIndex1d(ax, labels) for ax, labels in d["index"].items()])
        data = d["array"]
        return NumpyArray(index, data)
