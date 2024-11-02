from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

import numpy as np
from scipy.interpolate import RectBivariateSpline

from .table import Table

if typing.TYPE_CHECKING:
    from typing import Mapping


class BivariateScalar(ABC):
    """A continuous bivariate scalar"""

    @abstractmethod
    def __call__(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Evaluate the scalar (or derivatives) at given point(s)"""

    @abstractmethod
    def dx(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Evaluate the derivative along axis 1 at given point(s)"""

    @abstractmethod
    def dy(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Evaluate the derivative along axis 2 at given point(s)"""


@dataclass
class SplineOnNDArray(BivariateScalar):
    """2D spline interpolation on Numpy array
    - with bounds checking (returns NaN outside of domain)
    - of configurable order
    - supporting first derivatives
    - callable on sequences of unstructured points, not only 2D grids (see grid=False)
    """

    array: np.ndarray
    x: np.ndarray
    y: np.ndarray
    order: int
    sigma: float = 0.0

    @cached_property
    def _bounds(self) -> tuple[float, float, float, float]:
        return np.min(self.x), np.max(self.x), np.min(self.y), np.max(self.y)

    def _in_bounds_mask(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        x_min, x_max, y_min, y_max = self._bounds
        return (x >= x_min) & (x <= x_max) & (y >= y_min) & (y <= y_max)

    @cached_property
    def _spline(self) -> RectBivariateSpline:
        # Rescale the s parameter so that this object's `s` represents the typical
        # noise or error on the array values, see:
        # https://github.com/scipy/scipy/blob/master/scipy/interpolate/fitpack/regrid.f
        # e.g. comments around line 197:
        s = len(self.x) * len(self.y) * (self.sigma**2)
        return RectBivariateSpline(
            self.x,
            self.y,
            self.array,
            kx=self.order,
            ky=self.order,
            s=s,
        )

    def _eval(self, x: np.ndarray, y: np.ndarray, dx: int, dy: int) -> np.ndarray:
        xa = np.asarray(x)
        ya = np.asarray(y)
        f = self._spline(xa, ya, dx, dy, grid=False)
        f[~self._in_bounds_mask(xa, ya)] = np.nan
        return np.squeeze(f)

    def __call__(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._eval(x, y, 0, 0)

    def dx(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._eval(x, y, 1, 0)

    def dy(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._eval(x, y, 0, 1)


@dataclass
class SplineOnTable(BivariateScalar):
    table: Table
    field: str
    order: int
    sigma: float = 0.0

    @cached_property
    def _s(self) -> SplineOnNDArray:
        x, y = self.table.coords().values()
        array = self.table.arrays()[self.field]
        return SplineOnNDArray(
            array,
            x,
            y,
            self.order,
            self.sigma,
        )

    def __call__(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._s(x, y)

    def dx(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._s.dx(x, y)

    def dy(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._s.dy(x, y)


@dataclass
class SplineWithInterpolatedFDDeriv(BivariateScalar):
    """2D spline on a table on which derivatives are computed
    by interpolation of the finite difference derivatives (computed using np.gradient).
    This can be less noisy than using SplineOnTable derivatives (which use
    exact derivatives of the interpolating spline).
    """

    table: Table
    field: str
    order: int
    sigma: float = 0.0
    deriv_order: int = 1
    deriv_sigma: float = 0.0

    @cached_property
    def _xy(self) -> tuple[np.ndarray, ...]:
        return tuple(self.table.coords().values())

    @cached_property
    def _array(self) -> np.ndarray:
        return self.table.arrays()[self.field]

    @cached_property
    def _s(self) -> SplineOnNDArray:
        x, y = self._xy
        return SplineOnNDArray(self._array, x, y, self.order, self.sigma)

    @cached_property
    def _sdx(self) -> SplineOnNDArray:
        x, y = self._xy
        return SplineOnNDArray(
            np.gradient(self._array, x, axis=0),
            x,
            y,
            self.deriv_order,
            self.deriv_sigma,
        )

    @cached_property
    def _sdy(self) -> SplineOnNDArray:
        x, y = self._xy
        return SplineOnNDArray(
            np.gradient(self._array, y, axis=1),
            x,
            y,
            self.deriv_order,
            self.deriv_sigma,
        )

    def __call__(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._s(x, y)

    def dx(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._sdx(x, y)

    def dy(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return self._sdy(x, y)


@dataclass
class RemappedTable(Table):
    fields: Mapping[str, BivariateScalar]
    old_vars: tuple[str, str]
    old_vars_at_new_vars: Table

    def coords(self) -> Mapping[str, np.ndarray]:
        return self.old_vars_at_new_vars.coords()

    def arrays(self) -> Mapping[str, np.ndarray]:
        old_at_new = self.old_vars_at_new_vars.arrays()

        old_coords = tuple(old_at_new[ax] for ax in self.old_vars)
        return {field: spline(*old_coords) for (field, spline) in self.fields.items()}
