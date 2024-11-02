from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import numpy as np
import pandas as pd

if typing.TYPE_CHECKING:
    from numpy.typing import DTypeLike, NDArray


@dataclass
class _ParticleEventRecord:
    ndim: int
    gid_dtype: DTypeLike = np.int64

    @property
    def _coords(self) -> list[str]:
        return [f"x{i}" for i in range(1, self.ndim + 1)]

    @property
    def fields(self) -> dict[str, DTypeLike]:
        return {
            "gid": self.gid_dtype,
            **{f"penetration_{c}": np.float64 for c in self._coords},
            "penetration_t": np.float64,
            "penetration_v": np.float64,
            **{f"turnaround_{c}": np.float64 for c in self._coords},
            "turnaround_t": np.float64,
            "penetration_max_v": np.float64,
        }

    @property
    def dtype(self) -> np.dtype:
        return np.dtype(list(self.fields.items()))


@dataclass
class ParticleEventsRawFile:
    file_name: str
    ndim: int

    @cached_property
    def _rec(self) -> _ParticleEventRecord:
        return _ParticleEventRecord(self.ndim)

    @cached_property
    def num_events(self) -> int:
        fsize = Path(self.file_name).stat().st_size
        dtype = self._rec.dtype
        if fsize % dtype.itemsize != 0:
            raise ValueError(
                f"Size of file {self.file_name} is not a multiple of the event size"
            )
        return fsize // dtype.itemsize

    def ndarray(self) -> NDArray:
        with open(self.file_name, "rb") as f:
            data = np.fromfile(f, dtype=self._rec.dtype, count=self.num_events)
            return data

    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.ndarray())
