from __future__ import annotations

import glob
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

import numpy as np
from music_pykg.format2 import Header, MusicNewFormatDumpFile
from music_pykg.known_variables import KnownMusicVariables

from ..big_array import BigArray, ItemsIndex1d, MusicDumpArray, StackedArray
from ..grid import (
    ArbitraryGrid1D,
    CartesianGrid2D,
    CartesianGrid3D,
    NonUniformGridError,
    SphericalGrid2D,
    SphericalGrid3D,
    UniformGrid1D,
)

if typing.TYPE_CHECKING:
    from os import PathLike
    from typing import Iterable, Sequence, TypeAlias

    from ..grid import Grid, Grid1D

    NSlice: TypeAlias = tuple[int | slice, ...]


def _take_slice(ndim: int, index: int, ax: int) -> NSlice:
    return ax * (slice(None),) + (index,) + (ndim - ax - 1) * (slice(None),)


def _l_face_slice(arr: np.ndarray, axis: int) -> NSlice:
    ndim = arr.ndim
    return _take_slice(ndim, 0, axis)


def _r_face_slice(arr: np.ndarray, axis: int) -> NSlice:
    ndim = arr.ndim
    i_last = arr.shape[axis] - 1
    return _take_slice(ndim, i_last, axis)


class ArrayBC(ABC):
    @abstractmethod
    def fill_right_domain_faces(
        self, faces_l: np.ndarray, faces_r: np.ndarray, axis: int
    ) -> None:
        pass


class ReflectiveArrayBC(ArrayBC):
    def fill_right_domain_faces(
        self, faces_l: np.ndarray, faces_r: np.ndarray, axis: int
    ) -> None:
        if np.any(faces_l[_l_face_slice(faces_l, axis)] != 0.0):
            raise ValueError(
                f"ReflectiveArrayBC: expected leftmost values to be zero along axis={axis}, "
                "do your PyMUSIC BCs match the actually used MUSIC BCs?"
            )
        faces_r[_r_face_slice(faces_r, axis)] = 0.0


class PeriodicArrayBC(ArrayBC):
    def fill_right_domain_faces(
        self, faces_l: np.ndarray, faces_r: np.ndarray, axis: int
    ) -> None:
        # Copy leftmost faces to rightmost faces
        faces_r[_r_face_slice(faces_r, axis)] = faces_l[_l_face_slice(faces_l, axis)]


class CubeWithCentering(ABC):
    @abstractmethod
    def raw_cube(self) -> np.ndarray:
        """:return: raw data cube with raw (unmodified) centering"""
        pass

    @abstractmethod
    def cell_centered_cube(self) -> np.ndarray:
        """:return: cell-centered data array"""
        pass


class CellCenteredArray(CubeWithCentering):
    def __init__(self, cube: np.ndarray):
        """:param cube: data cube of values at cell centers"""
        self._cube = cube

    def raw_cube(self) -> np.ndarray:
        return self._cube

    def cell_centered_cube(self) -> np.ndarray:
        return self._cube


class LeftStaggeredArray(CubeWithCentering):
    def __init__(self, cube_at_left_faces: np.ndarray, axis: int, bc: ArrayBC):
        """
        :param cube_at_left_faces: data cube of values at left faces along axis
        :param axis: direction (axis) of staggering
        :param bc: boundary condition to use for centering values near the right domain border
        """
        self._cube_l_faces = cube_at_left_faces
        self.axis = axis
        self.bc = bc

    def raw_cube(self) -> np.ndarray:
        return self._cube_l_faces

    def cell_centered_cube(self) -> np.ndarray:
        cube_l_faces = self._cube_l_faces
        cube_r_faces = np.roll(cube_l_faces, -1, axis=self.axis)
        # Have BCs fill missing rightmost face values
        self.bc.fill_right_domain_faces(cube_l_faces, cube_r_faces, self.axis)
        # Interpolate to cell centers
        return 0.5 * (cube_l_faces + cube_r_faces)


@dataclass(frozen=True)
class _RawMusicDump:
    """Music dump with fields named as in format 2.

    :param dump_file: input dump file
    :param recenter_bc_along_axes: list of boundary conditions
        to use for re-centering along each space direction
    :param music_vars: a `KnownMusicVariables` object describing variables
        and their centering
    """

    dump_file: MusicNewFormatDumpFile
    recenter_bc_along_axes: Sequence[ArrayBC]
    music_vars: KnownMusicVariables

    @cached_property
    def _header(self) -> Header:
        return self.dump_file.read_header()

    def _array_with_centering(
        self, name: str, data_cube: np.ndarray
    ) -> CubeWithCentering:
        var = self.music_vars.legacy(name)
        ndim = self.num_space_dims

        num_stag_ax = var.nodes.num_staggered_axes(ndim)
        # Only cell- (num_stag_ax==0) and face- (num_stag_ax==1) centered
        # quantities are supported for now
        assert 0 <= num_stag_ax <= 1

        for ax in range(ndim):
            if var.nodes.is_staggered_along(ax, ndim):
                return LeftStaggeredArray(
                    data_cube, axis=ax, bc=self.recenter_bc_along_axes[ax]
                )
        else:
            assert num_stag_ax == 0
            return CellCenteredArray(data_cube)

    def data_arrays(self) -> dict[str, CubeWithCentering]:
        _, cubes_dict = self.dump_file.read()
        return {
            name: self._array_with_centering(name, cube)
            for name, cube in cubes_dict.items()
        }

    @property
    def file_name(self) -> str | PathLike:
        return self.dump_file.file_name

    @property
    def field_names(self) -> Sequence[str]:
        return self.dump_file.field_names

    @property
    def num_space_dims(self) -> int:
        return self.dump_file.num_space_dims

    @property
    def num_velocities(self) -> int:
        return self.dump_file.num_velocities

    @property
    def num_scalars(self) -> int:
        return self.dump_file.num_scalars

    def point_grid(self, axis: int) -> Grid1D:
        assert 0 <= axis < self.num_space_dims
        xf = getattr(self._header, f"face_loc_{axis + 1}")
        try:
            return UniformGrid1D.from_face_points(xf, cell_points_loc=0.5)
        except NonUniformGridError:
            return ArbitraryGrid1D(xf)

    @property
    def time(self) -> float:
        return float(self._header.time)

    @property
    def grid(self) -> Grid:
        ndim = self.num_space_dims
        if ndim not in (2, 3):
            raise ValueError(f"ndim expected to be 2 or 3, got {ndim}")

        if ndim == 2:
            if self._header.spherical:
                return SphericalGrid2D(self.point_grid(0), self.point_grid(1))
            return CartesianGrid2D(self.point_grid(0), self.point_grid(1))

        if self._header.spherical:
            return SphericalGrid3D(
                self.point_grid(0), self.point_grid(1), self.point_grid(2)
            )
        return CartesianGrid3D(
            self.point_grid(0), self.point_grid(1), self.point_grid(2)
        )

    def keeping_only_vars(self, names: Iterable[str]) -> _RawMusicDump:
        to_keep = set(names)
        return _RawMusicDump(
            self.dump_file.keeping_only(lambda s: s in to_keep),
            self.recenter_bc_along_axes,
            self.music_vars,
        )


@dataclass
class MusicDump:
    _raw_dump: _RawMusicDump
    music_vars: KnownMusicVariables

    """Music dump with fields renamed to pymusic conventions."""

    @staticmethod
    def from_file(
        dump_file: MusicNewFormatDumpFile,
        recenter_bc_along_axes: Sequence[ArrayBC],
        music_vars: KnownMusicVariables,
    ) -> MusicDump:
        """Create a new instance.

        :param dump_file: input dump file
        :param recenter_bc_along_axes: list of boundary conditions
            to use for re-centering along each space direction
        :param music_vars: a `KnownMusicVariables` object describing variables
            and their centering
        """
        return MusicDump(
            _RawMusicDump(dump_file, recenter_bc_along_axes, music_vars),
            music_vars,
        )

    def data_arrays(self) -> dict[str, CubeWithCentering]:
        dat_arr = self._raw_dump.data_arrays()
        return {self.music_vars.legacy(name).name: val for name, val in dat_arr.items()}

    @property
    def file_name(self) -> str | PathLike:
        return self._raw_dump.file_name

    @cached_property
    def field_names(self) -> Sequence[str]:
        return tuple(
            self.music_vars.legacy(name).name for name in self._raw_dump.field_names
        )

    @property
    def num_space_dims(self) -> int:
        return self._raw_dump.num_space_dims

    @property
    def num_velocities(self) -> int:
        return self._raw_dump.num_velocities

    @property
    def num_scalars(self) -> int:
        return self._raw_dump.num_scalars

    def point_grid(self, axis: int) -> Grid1D:
        return self._raw_dump.point_grid(axis)

    @property
    def time(self) -> float:
        return self._raw_dump.time

    @property
    def grid(self) -> Grid:
        return self._raw_dump.grid

    def keeping_only_vars(self, names: Iterable[str]) -> MusicDump:
        return MusicDump(
            self._raw_dump.keeping_only_vars(
                self.music_vars[name].legacy_name for name in names
            ),
            self.music_vars,
        )


class MusicSim:
    def __init__(self, dumps: Sequence[MusicDump]):
        """
        :param dumps: list or sequence of dumps
        """
        if len(dumps) == 0:
            raise ValueError(
                "list of dumps is empty, expecting at least one dump per simulation"
            )

        self.dumps = dumps

    def big_array(self, verbose: bool = False) -> BigArray:
        if verbose:
            print(
                f"MusicSim: assembling BigArray for {len(self.dumps)} dumps; will read all headers..."
            )
        dump_arrays = [MusicDumpArray(dump, verbose) for dump in self.dumps]
        # Build time index
        time_index = ItemsIndex1d("time", [dump.time for dump in self.dumps])
        if verbose:
            print("MusicSim: ...done!")
        # Return stacked array
        return StackedArray(dump_arrays, time_index, 0)

    def point_grid(self, axis: int) -> Grid1D:
        return self.dumps[0].point_grid(axis)

    @property
    def grid(self) -> Grid:
        return self.dumps[0].grid

    @classmethod
    def from_dump_file_names(
        cls,
        file_names: Iterable[str | PathLike],
        recenter_bc_list: Sequence[ArrayBC],
    ) -> MusicSim:
        music_vars = KnownMusicVariables()
        return cls(
            [
                MusicDump.from_file(
                    MusicNewFormatDumpFile(f),
                    recenter_bc_list,
                    music_vars=music_vars,
                )
                for f in file_names
            ]
        )

    @classmethod
    def from_dump_dir(
        cls,
        directory: str,
        recenter_bc_list: Sequence[ArrayBC],
    ) -> MusicSim:
        return cls.from_dump_file_names(
            sorted(glob.glob(directory + "/*.music")), recenter_bc_list
        )
