from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import numpy as np

from ..eos.interp import SplineOnTable
from ..eos.table import (
    FilledNans,
    LinInterpTable,
    MemCachedTable,
    NumpyArrayTable,
    Table,
    TableFromFile,
)
from .music_formats import MusicOpacityTableFile
from .variables import DTState

if typing.TYPE_CHECKING:
    from typing import Mapping

    from ..eos.table import TableFile


@dataclass
class _FixedXZMesaOpacityTable(Table):
    mesa_table_file: str | Path
    x: float
    z: float

    @cached_property
    def _file(self) -> TableFile:
        return MusicOpacityTableFile(str(self.mesa_table_file))

    @cached_property
    def _table(self) -> Table:
        return TableFromFile(self._file)

    def coords(self) -> Mapping[str, np.ndarray]:
        coords = TableFromFile(self._file).coords()
        del coords["x"], coords["z"]
        return coords

    def arrays(self) -> Mapping[str, np.ndarray]:
        table = self._table.arrays()["logkappa"]
        full_coords = TableFromFile(self._file).coords()
        zs = full_coords["z"]
        xs = full_coords["x"]
        iz = np.searchsorted(zs, self.z) - 1
        ix = np.searchsorted(xs, self.x) - 1

        try:
            x0, x1 = xs[ix], xs[ix + 1]
            z0, z1 = zs[iz], zs[iz + 1]
        except IndexError:
            raise ValueError(
                f"X={self.x}, Z={self.z} cannot be interpolated from available tables"
            )
        assert x0 <= self.x <= x1
        assert z0 <= self.z <= z1

        tab_x0_z0 = NumpyArrayTable({"logkappa": table[iz, ix]}, coords=self.coords())
        tab_x0_z1 = NumpyArrayTable(
            {"logkappa": table[iz + 1, ix]}, coords=self.coords()
        )
        tab_x1_z0 = NumpyArrayTable(
            {"logkappa": table[iz, ix + 1]}, coords=self.coords()
        )
        tab_x1_z1 = NumpyArrayTable(
            {"logkappa": table[iz + 1, ix + 1]}, coords=self.coords()
        )

        tab_x_z0 = LinInterpTable(tab_x0_z0, tab_x1_z0, x0, x1, self.x)
        tab_x_z1 = LinInterpTable(tab_x0_z1, tab_x1_z1, x0, x1, self.x)
        tab_x_z = LinInterpTable(tab_x_z0, tab_x_z1, z0, z1, self.z)
        return tab_x_z.arrays()


@dataclass
class _FixedXZMesaOpacityState:
    table: Table
    rho: np.ndarray
    temperature: np.ndarray

    @cached_property
    def _rt(self) -> tuple[np.ndarray, np.ndarray]:
        s = DTState(rho=np.log10(self.rho), t=np.log10(self.temperature))
        return s.r, s.t

    def _spline_eval(self, field: str) -> np.ndarray:
        spline = SplineOnTable(FilledNans(self.table), field, order=1, sigma=0.0)
        r, t = self._rt
        return spline(t, r)

    @cached_property
    def kappa(self) -> np.ndarray:
        return 10 ** self._spline_eval("logkappa")


@dataclass
class FixedXZMesaOpacity:
    mesa_table_file: str | Path
    x: float
    z: float

    @cached_property
    def _table(self) -> Table:
        return MemCachedTable(
            _FixedXZMesaOpacityTable(self.mesa_table_file, self.x, self.z)
        )

    def state(
        self, rho: float | np.ndarray, temperature: float | np.ndarray
    ) -> _FixedXZMesaOpacityState:
        return _FixedXZMesaOpacityState(
            self._table, np.asarray(rho), np.asarray(temperature)
        )
