from __future__ import annotations

import typing
from dataclasses import dataclass
from io import StringIO

import pandas as pd
import xarray

from .table import NumpyArrayTable, TableFile

if typing.TYPE_CHECKING:
    from typing import Iterator, TextIO

    from .table import Table


def _iter_until_blank(f: TextIO) -> Iterator[str]:
    for ln in f:
        if not ln.strip():
            return
        yield ln


@dataclass(frozen=True)
class MesaAsciiTableFile(TableFile):
    """A file in MESA ASCII format"""

    file_name: str
    var1: str  # label of block independent variable (e.g. "logQ")
    var2: str  # label of row independent variable within block (e.g. "logT")

    def _read_header_from(self, f: TextIO) -> dict:
        # Column names can have a single space (@#!) so separate on 2+ spaces
        df = pd.read_csv(
            StringIO("".join([next(f), next(f)])), delimiter=r"\s\s+", engine="python"
        )
        next(f)
        return dict(df.iloc[0, :])

    def _iter_blocks_from(self, f: TextIO) -> Iterator[xarray.Dataset]:
        while True:
            if not next(f).strip().startswith(f"{self.var1} ="):
                return
            v1 = float(next(f).strip())
            next(f)

            df = (
                pd.read_csv(
                    StringIO("".join(_iter_until_blank(f))),
                    delim_whitespace=True,
                )
                .set_index(self.var2)
                .sort_index()
            )
            next(f)
            yield xarray.Dataset(df).expand_dims(dim={self.var1: [v1]})  # type: ignore

    def read(self) -> Table:
        with open(self.file_name, "r") as f:
            _ = self._read_header_from(f)
            dset = xarray.concat(list(self._iter_blocks_from(f)), self.var1)
            assert tuple(dset.dims) == (self.var1, self.var2)
            return NumpyArrayTable(
                arrays={
                    # TYPE SAFETY: xarray.Dataset doesn't offer generic annotations
                    typing.cast(str, name): a.values
                    for (name, a) in dset.items()
                },
                coords={str(ax): dset.coords[ax].values for ax in dset.dims},
            )

    def header(self) -> dict:
        with open(self.file_name, "r") as f:
            return self._read_header_from(f)


@dataclass(frozen=True)
class MesaAsciiDTTableFile(TableFile):
    """A file in MESA ASCII format for DT tabulated data in (logQ,logT) coordinates"""

    file_name: str

    @property
    def _file(self) -> MesaAsciiTableFile:
        return MesaAsciiTableFile(self.file_name, var1="logQ", var2="logT")

    def read(self) -> Table:
        return self._file.read()

    def header(self) -> dict:
        return self._file.header()
