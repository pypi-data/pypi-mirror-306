from __future__ import annotations

import re
import typing
from dataclasses import dataclass
from functools import cached_property

import numpy as np
import pandas as pd
from scipy.io import FortranFile

from .table import NumpyArrayTable, TableFile
from .variables import DEState, DTState

if typing.TYPE_CHECKING:
    from typing import Iterator, Sequence

    from matplotlib.axes import Axes

    from .table import Table


@dataclass(frozen=True)
class MusicDETableFile(TableFile):
    """An EoS table file in binary format for MUSIC's MESA module"""

    file_name: str
    _var_labels: Sequence[str] = (
        "logD",  # Log density
        "logP",  # Log total pressure, log(Pgas + Prad)
        "logPgas",
        "logT",
        "dlogP/dlogD|E",
        "dlogP/dlogE|D",
        "dlogT/dlogD|E",
        "dlogT/dlogE|D",
        "logS",
        "dlogT/dlogP|S",
        "Gamma1",
        "gamma",
    )

    @property
    def xz(self) -> tuple[float, float]:
        r = re.compile(r"^.*_z([\d.]+)x([\d.]+)\.bindata$")
        m = r.match(str(self.file_name))
        if m is None:
            raise ValueError(f"Cannot parse MUSIC EoS filename: '{self.file_name}'")
        return float(m.group(2)), float(m.group(1))

    def read(self) -> Table:
        f = FortranFile(self.file_name, mode="r")
        ne, nv, nvar = [x.item() for x in f.read_record("i4", "i4", "i4")]
        assert nvar == len(self._var_labels)
        v_grid = f.read_record(("f8", nv))
        e_grid = f.read_record(("f8", ne))

        def gen_rows() -> Iterator[np.ndarray]:
            for _ in v_grid:
                for _ in e_grid:
                    yield f.read_record(("f8", nvar))

        data = np.array(list(gen_rows())).reshape((nv, ne, nvar))
        f.close()
        return NumpyArrayTable(
            arrays={name: data[:, :, i] for (i, name) in enumerate(self._var_labels)},
            coords={"logV": v_grid, "logE": e_grid},
        )

    def write(self, table: Table) -> None:
        arrays = table.arrays()
        coords = table.coords()

        if tuple(coords.keys()) != ("logV", "logE"):
            raise ValueError(
                f"Expected table in (logV, logE) variables, found {tuple(coords.keys())}"
            )

        nv = len(coords["logV"])
        ne = len(coords["logE"])
        nvar = len(self._var_labels)

        missing_fields = set(self._var_labels).difference(set(arrays.keys()))
        if missing_fields:
            raise ValueError(f"Table is missing the following fields: {missing_fields}")

        f = FortranFile(self.file_name, mode="w")

        # Write header
        f.write_record([np.asarray([ne, nv, nvar], dtype="i4")])
        f.write_record(np.asarray(coords["logV"], dtype="f8"))
        f.write_record(np.asarray(coords["logE"], dtype="f8"))

        for iv in range(nv):
            for ie in range(ne):
                f.write_record(
                    np.array(
                        [arrays[var][iv, ie] for var in self._var_labels], dtype="f8"
                    )
                )
        f.close()


@dataclass
class Stellar1DProfile:
    file_name: str

    def dataframe(self, without_last_cell: bool = False) -> pd.DataFrame:
        df = pd.read_csv(self.file_name, skiprows=2, delim_whitespace=True)
        df = df.set_index("i")
        if without_last_cell:
            # Last cell is usually messed up or unreliable
            df = df.iloc[:-1, :]

        # Force coercion to float; sometimes the Fortran format overflows,
        # resulting in entries (and therefore columns) being parsed as strings
        # Typically this happens in the last cell. When reading with
        # without_last_cell=True, this should take care of it, and crash
        # appropriately in case the data cannot be interpreted as float.
        return df.astype("f")

    @cached_property
    def _df_plot(self) -> pd.DataFrame:
        return self.dataframe(without_last_cell=True)

    def plot_qt(self, ax: Axes) -> None:
        s = DTState(rho=np.log10(self._df_plot["rho"]), t=np.log10(self._df_plot["T"]))
        ax.plot(s.q, s.t, "w-", lw=3)
        ax.plot(s.q, s.t, "k-", lw=1)

    def plot_ve(self, ax: Axes) -> None:
        s = DEState(rho=np.log10(self._df_plot["rho"]), e=np.log10(self._df_plot["E"]))
        ax.plot(s.v, s.e, "w-", lw=3)
        ax.plot(s.v, s.e, "k-", lw=1)
