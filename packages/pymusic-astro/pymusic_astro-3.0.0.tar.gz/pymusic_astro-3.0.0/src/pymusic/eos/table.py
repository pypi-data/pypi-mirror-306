from __future__ import annotations

import pickle
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import numpy as np

if typing.TYPE_CHECKING:
    from typing import Mapping, Sequence


@dataclass(frozen=True)
class Abundances:
    x: float
    z: float

    @property
    def y(self) -> float:
        return 1.0 - (self.x + self.z)


class Table(ABC):
    @abstractmethod
    def arrays(self) -> Mapping[str, np.ndarray]:
        """Return the table as an dict of Numpy arrays"""

    @abstractmethod
    def coords(self) -> Mapping[str, np.ndarray]:
        """Return the grid coordinate arrays, indexed by name"""

    def meshgrid(self) -> Sequence[np.ndarray]:
        x, y = self.coords().values()
        return np.meshgrid(x, y, indexing="ij")


class TableFile(ABC):
    """Represent a file whose content can be seen as a table."""

    @abstractmethod
    def read(self) -> Table:
        """Build a Table from the file content."""


class NumpyArrayTable(Table):
    """A table based on actual Numpy arrays"""

    def __init__(
        self,
        arrays: Mapping[str, np.ndarray],
        coords: Mapping[str, np.ndarray],
    ):
        self._arrays = dict(arrays)
        self._coords = dict(coords)
        # Try to catch annoying shape problems early on
        assert all(a.ndim == 1 for a in self._coords.values())
        shape = tuple(a.size for a in self._coords.values())
        assert len(shape) == 2
        assert all(a.shape == shape for a in self._arrays.values())

    def arrays(self) -> Mapping[str, np.ndarray]:
        return self._arrays

    def coords(self) -> Mapping[str, np.ndarray]:
        return self._coords


class MemCachedTable(Table):
    def __init__(self, table: Table):
        self._table = table
        self._cache_arrays: Mapping[str, np.ndarray] | None = None
        self._cache_coords: Mapping[str, np.ndarray] | None = None

    def arrays(self) -> Mapping[str, np.ndarray]:
        if self._cache_arrays is None:
            self._cache_arrays = self._table.arrays()
        return self._cache_arrays

    def coords(self) -> Mapping[str, np.ndarray]:
        if self._cache_coords is None:
            self._cache_coords = self._table.coords()
        return self._cache_coords


class DiskCachedTable(Table):
    def __init__(self, table: Table, file_name: str):
        self._table = table
        self._fname = file_name

    def _read(self) -> tuple[Mapping[str, np.ndarray], Mapping[str, np.ndarray]]:
        with open(self._fname, "rb") as f:
            print(f"About to read cached table from '{self._fname}'")
            return pickle.load(f)

    def _write(
        self, coords: Mapping[str, np.ndarray], arrays: Mapping[str, np.ndarray]
    ) -> None:
        with open(self._fname, "wb") as f:
            pickle.dump((coords, arrays), f)
            print(f"Wrote cached table to '{self._fname}'")

    def _get(self) -> tuple[Mapping[str, np.ndarray], Mapping[str, np.ndarray]]:
        if Path(self._fname).exists():
            coords, arrays = self._read()
        else:
            coords, arrays = self._table.coords(), self._table.arrays()
            self._write(coords, arrays)
        return coords, arrays

    def arrays(self) -> Mapping[str, np.ndarray]:
        _, arrays = self._get()
        return arrays

    def coords(self) -> Mapping[str, np.ndarray]:
        coords, _ = self._get()
        return coords


@dataclass(frozen=True)
class TableFromFile(Table):
    file: TableFile

    def _table(self) -> Table:
        return self.file.read()

    def coords(self) -> Mapping[str, np.ndarray]:
        return self._table().coords()

    def arrays(self) -> Mapping[str, np.ndarray]:
        return self._table().arrays()


@dataclass(frozen=True)
class JoinedTable(Table):
    tables: Sequence[Table]

    def coords(self) -> Mapping[str, np.ndarray]:
        cs = [tab.coords() for tab in self.tables]
        assert all(tuple(c) == tuple(cs[0]) for c in cs)

        for ax in cs[0]:
            xs = [c[ax] for c in cs]
            assert all(x.size == xs[0].size for x in xs)

        return cs[0]

    def arrays(self) -> Mapping[str, np.ndarray]:
        arrays: dict[str, np.ndarray] = {}
        for tab in self.tables:
            arrays.update(tab.arrays())
        return arrays


@dataclass(frozen=True)
class LinInterpTable(Table):
    table1: Table
    table2: Table
    x1: float
    x2: float
    x: float

    def arrays(self) -> Mapping[str, np.ndarray]:
        arr1 = self.table1.arrays()
        arr2 = self.table2.arrays()
        if set(arr1) != set(arr2):
            raise ValueError("Cannot interpolate tables with non-matching fields")

        u = (self.x - self.x1) / (self.x2 - self.x1)
        return {field: (1.0 - u) * arr1[field] + u * arr2[field] for field in arr1}

    def coords(self) -> Mapping[str, np.ndarray]:
        return self.table1.coords()


@dataclass(frozen=True)
class FilledNans(Table):
    table: Table
    fill_value: float = 0.0

    def coords(self) -> Mapping[str, np.ndarray]:
        return self.table.coords()

    def arrays(self) -> Mapping[str, np.ndarray]:
        arrays = self.table.arrays()
        return {
            field: np.nan_to_num(arr, nan=self.fill_value)
            for field, arr in arrays.items()
        }
