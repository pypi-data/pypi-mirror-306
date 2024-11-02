from __future__ import annotations

import typing
from dataclasses import dataclass

import numpy as np
from scipy.io import FortranFile

from ..eos.table import Table, TableFile
from .table import NumpyNdimArrayTable

if typing.TYPE_CHECKING:
    from typing import Iterator, Sequence


@dataclass(frozen=True)
class MusicOpacityTableFile(TableFile):
    """An opacity table file in binary format for MUSIC's MESA module"""

    file_name: str
    _var_labels: Sequence[str] = ("kappa",)  # opacity

    def read(self) -> Table:
        f = FortranFile(self.file_name, mode="r")
        nz, nx, nrho, ntemp = [x.item() for x in f.read_record("i4", "i4", "i4", "i4")]
        z_grid = f.read_record(("f8", nz))
        x_grid = f.read_record(("f8", nx))
        t_grid = f.read_record(("f8", ntemp))
        r_grid = f.read_record(("f8", nrho))

        def gen_rows() -> Iterator[np.ndarray]:
            for _ in z_grid:
                for _ in x_grid:
                    for _ in t_grid:
                        yield f.read_record(("f8", nrho))

        data = np.array(list(gen_rows())).reshape((nz, nx, ntemp, nrho))
        f.close()
        return NumpyNdimArrayTable(
            arrays={"logkappa": data[:, :, :, :]},
            coords={"z": z_grid, "x": x_grid, "logT": t_grid, "r": r_grid},
        )
