from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from ..math import SphericalMidpointQuad1D

if typing.TYPE_CHECKING:
    from ..big_array.array import BigArray
    from .grid1d import Grid1D


class Grid(ABC):
    @property
    @abstractmethod
    def grids(self) -> tuple[Grid1D, ...]:
        """Grids along all axes."""

    @property
    def ndim(self) -> int:
        return len(self.grids)

    @property
    def shape_cells(self) -> tuple[int, ...]:
        return tuple(g.num_cells() for g in self.grids)

    @property
    def shape_faces(self) -> tuple[int, ...]:
        return tuple(s + 1 for s in self.shape_cells)

    @abstractmethod
    def cell_volumes(self) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def averaged_array_along_axis(self, array: BigArray, axis: int) -> BigArray:
        raise NotImplementedError


@dataclass(frozen=True)
class SphericalGrid2D(Grid):
    r_grid: Grid1D
    theta_grid: Grid1D

    @property
    def grids(self) -> tuple[Grid1D, Grid1D]:
        return self.r_grid, self.theta_grid

    def cell_volumes(self) -> np.ndarray:
        r3_f = self.r_grid.face_points() ** 3
        r2_dr = np.diff(r3_f) / 3.0
        costh_f = np.cos(self.theta_grid.face_points())
        sinth_dth = -np.diff(costh_f)
        dphi = 2.0 * np.pi  # azimuthal symmetry
        return dphi * r2_dr[:, np.newaxis] * sinth_dth[np.newaxis, :]

    def averaged_array_along_axis(self, array: BigArray, axis: int) -> BigArray:
        if axis == 1:  # theta
            quad = SphericalMidpointQuad1D(self.theta_grid)
            return array.collapse(quad.average, "x2")

        raise NotImplementedError(
            f"SphericalGrid2D: averaged_array_along_axis not implemented along axis={axis}"
        )


@dataclass(frozen=True)
class SphericalGrid3D(Grid):
    r_grid: Grid1D
    theta_grid: Grid1D
    phi_grid: Grid1D

    @property
    def grids(self) -> tuple[Grid1D, Grid1D, Grid1D]:
        return self.r_grid, self.theta_grid, self.phi_grid

    def cell_volumes(self) -> np.ndarray:
        r3_f = self.r_grid.face_points() ** 3
        r2_dr = np.diff(r3_f) / 3.0
        costh_f = np.cos(self.theta_grid.face_points())
        sinth_dth = -np.diff(costh_f)
        dphi = self.phi_grid.cell_widths()
        return (
            r2_dr[:, np.newaxis, np.newaxis]
            * sinth_dth[np.newaxis, :, np.newaxis]
            * dphi[np.newaxis, np.newaxis, :]
        )

    def averaged_array_along_axis(self, array: BigArray, axis: int) -> BigArray:
        raise NotImplementedError(
            "SphericalGrid3D.averaged_array_along_axis not implemented"
        )


@dataclass(frozen=True)
class CartesianGrid2D(Grid):
    x_grid: Grid1D
    y_grid: Grid1D

    @property
    def grids(self) -> tuple[Grid1D, Grid1D]:
        return self.x_grid, self.y_grid

    def cell_volumes(self) -> np.ndarray:
        dx = self.x_grid.cell_widths()[:, np.newaxis]
        dy = self.y_grid.cell_widths()[np.newaxis, :]
        return dx * dy

    def averaged_array_along_axis(self, array: BigArray, axis: int) -> BigArray:
        raise NotImplementedError(
            f"CartesianGrid2D: averaged_array_along_axis not implemented along axis={axis}"
        )


@dataclass(frozen=True)
class CartesianGrid3D(Grid):
    x_grid: Grid1D
    y_grid: Grid1D
    z_grid: Grid1D

    @property
    def grids(self) -> tuple[Grid1D, Grid1D, Grid1D]:
        return self.x_grid, self.y_grid, self.z_grid

    def cell_volumes(self) -> np.ndarray:
        dx = self.x_grid.cell_widths()[:, np.newaxis, np.newaxis]
        dy = self.y_grid.cell_widths()[np.newaxis, :, np.newaxis]
        dz = self.z_grid.cell_widths()[np.newaxis, np.newaxis, :]
        return dx * dy * dz

    def averaged_array_along_axis(self, array: BigArray, axis: int) -> BigArray:
        raise NotImplementedError(
            f"CartesianGrid3D: averaged_array_along_axis not implemented along axis={axis}"
        )
