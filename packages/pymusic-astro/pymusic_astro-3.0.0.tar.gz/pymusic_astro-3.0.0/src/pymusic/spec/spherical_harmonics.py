from __future__ import annotations

import typing

import numpy as np
from scipy.special import sph_harm

FOURPI = 4.0 * np.pi
SQRT_FOURPI = np.sqrt(FOURPI)

if typing.TYPE_CHECKING:
    from numpy.typing import NDArray

    from ..big_array import FC
    from ..math.spherical_quadrature import SphericalMidpointQuad1D


class SphericalHarmonicsTransform1D:
    def __init__(self, quad: SphericalMidpointQuad1D, ell_max: int, tol: float = 0.001):
        r"""
        1D spherical harmonics transform for real or complex input data.

        :param quad: spherical quadrature to use
        :param ell_max: maximum :math:`\ell` to compute spectrum for
        :param tol: tolerance for check on norm of discretized basis functions
        """
        self._quad = quad
        self._theta_grid = quad.theta_grid
        self._theta = self._theta_grid.cell_points()
        self._ell_max = ell_max
        self._tol = float(tol)
        assert self._tol > 0.0

        # Initialize cache
        self._basis_func_cache: dict[int, NDArray[np.float64]] = {}

    def _inner_product(self, bfunc: NDArray[np.float64], g: NDArray[FC]) -> FC:
        conj_b = bfunc  # since basis functions are all real in 1D with m=0
        # Average of b*g over the sphere
        return self._quad.integrate(conj_b * g) / FOURPI  # type: ignore

    def basis_func(self, ell: int) -> NDArray[np.float64]:
        if ell not in self._basis_func_cache:
            b_func_unnorm = sph_harm(
                0, ell, 0, self._theta
            ).real  # FIXME: imag part only involved for m>0?
            b_norm = np.sqrt(self._inner_product(b_func_unnorm, b_func_unnorm))
            # According to normalization conventions of sph_harm, and our choice of inner_product,
            # FOURPI * b_norm**2 should be close enough to 1.0, otherwise we have truncation error
            if abs(SQRT_FOURPI * b_norm - 1.0) > self._tol:
                raise ValueError(
                    f"spherical harmonics integration error exceeds tolerance of {self._tol} for ell={ell}"
                )
            # Scale basis functions so that their norm is 1.0,
            # i.e. they have an average power of 1.0
            self._basis_func_cache[ell] = b_func_unnorm / b_norm

        return self._basis_func_cache[ell]

    def amplitude(self, array: NDArray[FC], ell: int) -> FC:
        return self._inner_product(self.basis_func(ell), array)

    def transform(self, array: NDArray[FC]) -> NDArray[FC]:
        return np.array([self.amplitude(array, ell) for ell in range(self._ell_max)])
