from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import numpy as np

from .interp import SplineOnTable
from .music_formats import MusicDETableFile
from .table import FilledNans, LinInterpTable, MemCachedTable, Table, TableFromFile
from .variables import DEState, F

if typing.TYPE_CHECKING:
    from os import PathLike
    from typing import Mapping, NoReturn, Sequence


@dataclass(frozen=True)
class _MissingTable(Table):
    x: float
    z: float

    def _err(self) -> NoReturn:
        raise ValueError("Missing table for x={self.x}, z={self.z}")

    def arrays(self) -> NoReturn:
        self._err()

    def coords(self) -> NoReturn:
        self._err()


@dataclass
class _FixedXZMesaTable(Table):
    mesa_tables_dir: Path
    x: float
    z: float

    @cached_property
    def _files(self) -> Sequence[MusicDETableFile]:
        return [
            MusicDETableFile(str(f))
            for f in self.mesa_tables_dir.glob("output_DE_*.bindata")
        ]

    @cached_property
    def _xz_tables(
        self,
    ) -> tuple[Sequence[float], Sequence[float], Mapping[tuple[float, float], Table]]:
        xz_tables = {f.xz: TableFromFile(f) for f in self._files}
        xs, zs = (sorted(set(item)) for item in zip(*xz_tables))
        return (
            xs,
            zs,
            {
                (x, z): xz_tables.get((x, z), _MissingTable(x, z))
                for x in xs
                for z in zs
            },
        )

    def coords(self) -> Mapping[str, np.ndarray]:
        # Assume all arrays have compatible coordinates
        return TableFromFile(self._files[0]).coords()

    def arrays(self) -> Mapping[str, np.ndarray]:
        xs, zs, xz_tables = self._xz_tables
        ix = int(np.searchsorted(xs, self.x)) - 1
        iz = int(np.searchsorted(zs, self.z)) - 1

        try:
            x0, x1 = xs[ix], xs[ix + 1]
            z0, z1 = zs[iz], zs[iz + 1]
        except IndexError:
            raise ValueError(
                f"X={self.x}, Z={self.z} cannot be interpolated from available tables"
            )

        assert x0 <= self.x <= x1
        assert z0 <= self.z <= z1

        tab_x_z0 = LinInterpTable(
            xz_tables[(x0, z0)], xz_tables[(x1, z0)], x0, x1, self.x
        )
        tab_x_z1 = LinInterpTable(
            xz_tables[(x0, z1)], xz_tables[(x1, z1)], x0, x1, self.x
        )
        tab_x_z = LinInterpTable(tab_x_z0, tab_x_z1, z0, z1, self.z)
        return tab_x_z.arrays()


@dataclass
class _FixedXZMesaGasState:
    table: Table
    rho: np.ndarray
    e_int: np.ndarray

    @cached_property
    def _ve(self) -> tuple[np.ndarray, np.ndarray]:
        s = DEState(rho=np.log10(self.rho), e=np.log10(self.e_int))
        return s.v, s.e

    def _spline_eval(self, field: str) -> np.ndarray:
        spline = SplineOnTable(FilledNans(self.table), field, order=3, sigma=0.0)
        v, e = self._ve
        return spline(v, e)

    @cached_property
    def temperature(self) -> np.ndarray:
        return 10.0 ** self._spline_eval("logT")

    @cached_property
    def pressure(self) -> np.ndarray:
        return 10.0 ** self._spline_eval("logP")

    @cached_property
    def specific_entropy(self) -> np.ndarray:
        return 10.0 ** self._spline_eval("logS")

    @property
    def specific_energy(self) -> np.ndarray:
        return self.e_int

    @property
    def energy_density(self) -> np.ndarray:
        return self.rho * self.specific_energy

    @cached_property
    def enthalpy_density(self) -> np.ndarray:
        return self.energy_density + self.pressure

    @cached_property
    def specific_enthalpy(self) -> np.ndarray:
        return self.enthalpy_density / self.rho


@dataclass
class FixedXZMesaEoS:
    mesa_tables_dir: str | PathLike
    x: float
    z: float

    @cached_property
    def _table(self) -> Table:
        return MemCachedTable(
            _FixedXZMesaTable(Path(self.mesa_tables_dir), self.x, self.z)
        )

    def state(
        self, rho: float | np.ndarray, e_int: float | np.ndarray
    ) -> _FixedXZMesaGasState:
        return _FixedXZMesaGasState(self._table, np.asarray(rho), np.asarray(e_int))
