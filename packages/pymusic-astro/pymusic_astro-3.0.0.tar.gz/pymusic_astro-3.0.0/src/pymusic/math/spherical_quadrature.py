"""
:mod:`pymusic.math.spherical_quadrature`: numerical integration on the sphere
=============================================================================

"""

from __future__ import annotations

import typing
import warnings

import numpy as np

if typing.TYPE_CHECKING:
    from typing import Callable, TypeVar

    from numpy.typing import NDArray

    from ..big_array import FC, FloatOrCplx
    from ..grid.grid1d import Grid1D


class SphericalMidpointQuad1D:
    """
    Midpoint method for 1D spherical integration
    """

    def __init__(self, theta_grid: Grid1D, grid_check_tol: float = 1e-10):
        r"""
        :param theta_grid: discretization grid in the :math:`\theta` (colatitude) direction.
            Must be contained within :math:`[0, \pi]`, and should be cell-centered
            for second-order accuracy.
        :param grid_check_tol: absolute tolerance to use
            when checking the colatitude grid bounds
        """
        self.theta_grid = theta_grid
        self.grid_check_tol = grid_check_tol
        if not self.theta_grid.is_cell_centered():
            warnings.warn(
                "theta_grid is not cell-centered, "
                "spherical quadrature will degrade to first-order accuracy"
            )

        theta_min, theta_max = self.theta_grid.bounds()
        if not (
            -self.grid_check_tol <= theta_min < theta_max <= np.pi + self.grid_check_tol
        ):
            raise ValueError("theta (colatitude) grid must be contained in [0, pi]")

        # Precompute differential element
        d_cos_theta = np.abs(np.diff(np.cos(self.theta_grid.face_points())))
        d_phi = 2.0 * np.pi  # 1D case
        self._d_omega = d_cos_theta * d_phi
        self._sum_d_omega = np.sum(self._d_omega)

    @property
    def volume(self) -> np.float64:
        """Volume of total integration domain"""
        # This would be 4*pi for exact integration; we use instead the sum of the weights
        # (dOmega) to ensure that averages preserve constants exactly
        return self._sum_d_omega

    def integrate(self, f_values: NDArray[FC]) -> FC:
        r"""Integrate function on the sphere from 1D array of sampled values along `theta_grid`

        :param f_values: sampled function values at grid cell centers
        :returns: integral of sampled function on the sphere
        """
        return np.sum(f_values * self._d_omega)

    def average(self, f_values: NDArray[FC]) -> FC:
        r"""Average function on the sphere from 1D array of sampled values along `theta_grid`

        :param f_values: sampled function values at grid cell centers
        :returns: average of sampled function on the sphere
        """
        # TYPE SAFETY: mypy doesn't see how to propagate union through /
        return self.integrate(f_values) / self.volume  # type: ignore

    def integrate_func(self, func: Callable[[NDArray[FC]], NDArray[FC]]) -> FC:
        r"""Integrate function of :math:`\theta` on the sphere using quadrature grid

        :param func: scalar function to integrate
        :returns: integral of function on the sphere
        """
        theta_values = self.theta_grid.cell_points()
        return self.integrate(func(theta_values))

    def average_func(self, func: Callable[[NDArray[FC]], NDArray[FC]]) -> FC:
        r"""Average function of :math:`\theta` on the sphere using quadrature grid

        :param func: scalar function to average
        :returns: average of function on the sphere
        """
        theta_values = self.theta_grid.cell_points()
        return self.average(func(theta_values))
