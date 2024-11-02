"""
:mod:`.music`: :class:`.BigArray` support for MUSIC dumps and simulations
=========================================================================
"""

from __future__ import annotations

import typing

import numpy as np

from .array import BigArray, IndexNd, ItemsIndex1d, SummedArray, TakeArray

if typing.TYPE_CHECKING:
    from typing import Sequence

    from numpy.typing import NDArray

    from ..io.music import MusicDump


class MusicDumpArray(BigArray[np.floating]):
    """An array using a MUSIC dump as the data source.
    All fields are interpolated to cell centers.
    """

    def __init__(self, dump: MusicDump, verbose: bool):
        """
        :param dump: music dump to use as array source
        :param verbose: whether to print out a message for every dump read operation
        """
        self.dump = dump
        self.verbose = verbose

    def _index(self) -> IndexNd:
        indexes = [
            ItemsIndex1d("var", self.dump.field_names),
            *[
                ItemsIndex1d(f"x{ax+1}", self.dump.point_grid(ax).cell_points())
                for ax in range(self.dump.num_space_dims)
            ],
        ]
        return IndexNd(indexes)

    def array(self) -> NDArray[np.floating]:
        # Read dump file
        if self.verbose:
            print(f"Will read '{self.dump.file_name}'")
        dump_data = self.dump.data_arrays()
        return np.stack(
            [dump_data[var].cell_centered_cube() for var in self.dump.field_names],
            axis=0,
        )

    def take(self, labels: Sequence[object], axis: str) -> BigArray:
        if axis == "var":
            # TYPE SAFETY: implicit requirement that the labels are str if the
            # axis is var breaks LSP with BigArray
            return MusicDumpArray(
                self.dump.keeping_only_vars(labels),  # type: ignore
                self.verbose,
            )
        else:
            return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[np.floating]:
        return SummedArray(self, axis)
