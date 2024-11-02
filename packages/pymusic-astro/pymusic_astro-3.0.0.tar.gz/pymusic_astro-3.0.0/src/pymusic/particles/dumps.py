from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

import numpy as np
import pandas as pd
from music_pykg.particles import ParticleData

from .. import big_array as pma

if typing.TYPE_CHECKING:
    from os import PathLike
    from typing import Callable, Iterator, MutableMapping, Sequence


class ParticleDump(ABC):
    """Base class for ParticleDump objects"""

    @property
    @abstractmethod
    def time(self) -> float:
        pass

    @property
    @abstractmethod
    def npart(self) -> int:
        pass

    @property
    @abstractmethod
    def ndim(self) -> int:
        pass

    @abstractmethod
    def dataframe(self) -> pd.DataFrame:
        pass


@dataclass(frozen=True)
class ParticleDumpFromFile(ParticleDump):
    fname: str | PathLike
    group: str = "tracers"
    position_vector: int = 0

    @cached_property
    def _data(self) -> ParticleData:
        return ParticleData(
            fname=self.fname,
            group=self.group,
            position_vector=self.position_vector,
        )

    @property
    def time(self) -> float:
        return self._data.time

    @property
    def npart(self) -> int:
        return self._data.npart

    @property
    def ndim(self) -> int:
        return self._data.ndim

    def dataframe(self) -> pd.DataFrame:
        return self._data.dataframe()


@dataclass(frozen=True)
class CachedDump(ParticleDump):
    source: ParticleDump

    @cached_property
    def time(self) -> float:
        return self.source.time

    @cached_property
    def npart(self) -> int:
        return self.source.npart

    @cached_property
    def ndim(self) -> int:
        return self.source.ndim

    @cached_property
    def _df(self) -> pd.DataFrame:
        return self.source.dataframe()

    def dataframe(self) -> pd.DataFrame:
        return self._df


@dataclass(frozen=True)
class ManagedCachedDump(ParticleDump):
    source: ParticleDump
    cache: MutableMapping

    @cached_property
    def time(self) -> float:
        return self.source.time

    @cached_property
    def npart(self) -> int:
        return self.source.npart

    @cached_property
    def ndim(self) -> int:
        return self.source.ndim

    def dataframe(self) -> pd.DataFrame:
        key = id(self)
        try:
            return self.cache[key]
        except KeyError:
            value = self.source.dataframe()
            self.cache[key] = value
            return value


@dataclass(frozen=True)
class DumpFilteredByGids(ParticleDump):
    source: ParticleDump
    gids: Sequence[int]

    @property
    def time(self) -> float:
        return self.source.time

    @cached_property
    def npart(self) -> int:
        return len(self.dataframe())

    @property
    def ndim(self) -> int:
        return self.source.ndim

    def dataframe(self) -> pd.DataFrame:
        df = self.source.dataframe()
        return df.loc[np.array(self.gids), :].copy()


@dataclass(frozen=True)
class DumpFilteredByFunc(ParticleDump):
    source: ParticleDump
    func: Callable[[pd.DataFrame], pd.Series]

    @property
    def time(self) -> float:
        return self.source.time

    @cached_property
    def npart(self) -> int:
        return len(self.dataframe())

    @property
    def ndim(self) -> int:
        return self.source.ndim

    def dataframe(self) -> pd.DataFrame:
        df = self.source.dataframe()
        return df.loc[self.func(df), :].copy()


@dataclass(frozen=True)
class Cart2DFromSpherical2DDump(ParticleDump):
    """2D spherical to 2D Cartesian coordinates.
    The Cartesian coordinates correspond to (X, Z) in global XYZ coordinates"""

    source: ParticleDump

    @property
    def time(self) -> float:
        return self.source.time

    @property
    def npart(self) -> int:
        return self.source.npart

    @property
    def ndim(self) -> int:
        return self.source.ndim

    def dataframe(self) -> pd.DataFrame:
        assert self.source.ndim == 2
        df = self.source.dataframe()
        r, theta = df.x1.copy(), df.x2.copy()
        df["x1"] = r * np.sin(theta)
        df["x2"] = r * np.cos(theta)
        return df


@dataclass(frozen=True)
class CartFromSpherical3DDump(ParticleDump):
    """3D spherical to 3D Cartesian coordinates, i.e. global XYZ coordinates"""

    source: ParticleDump

    @property
    def time(self) -> float:
        return self.source.time

    @property
    def npart(self) -> int:
        return self.source.npart

    @property
    def ndim(self) -> int:
        return self.source.ndim

    def dataframe(self) -> pd.DataFrame:
        assert self.source.ndim == 3
        df = self.source.dataframe()
        r, theta, phi = df.x1.copy(), df.x2.copy(), df.x3.copy()
        df["x1"] = r * np.sin(theta) * np.cos(phi)
        df["x2"] = r * np.cos(theta) * np.cos(phi)
        df["x3"] = r * np.sin(phi)
        return df


@dataclass(frozen=True)
class SynchedHydroAndParticleData:
    hydro_data: pma.BigArray
    particle_seq: Sequence[ParticleDump]

    def __getitem__(self, index: int) -> tuple[float, pma.BigArray, ParticleDump]:
        particles = self.particle_seq[index]
        time = particles.time
        hydro = self.hydro_data.xs(time, "time")
        return time, hydro, particles

    @cached_property
    def times(self) -> np.ndarray:
        t_part = [dump.time for dump in self.particle_seq]
        t_hydro = self.hydro_data.labels_along_axis("time")
        return np.array(sorted(set(t_part) & set(t_hydro)))

    def __len__(self) -> int:
        return len(self.times)

    def __iter__(self) -> Iterator[tuple[float, pma.BigArray, ParticleDump]]:
        for i in range(len(self)):
            yield self[i]
