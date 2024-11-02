r"""
:mod:`pymusic.spec.wedge_harmonics`: spectral analysis on spherical wedges
==========================================================================

Motivation and background
~~~~~~~~~~~~~~~~~~~~~~~~~

**Spherical wedges** are regions of the surface of a unit sphere delimited by

.. math::
        \theta & \in [\alpha, \pi-\alpha], \alpha \in [0, \pi/2[

        \phi   & \in [-\beta, \beta], \beta \in ]0, \pi]

where :math:`\theta` is the colatitude and :math:`\phi` is the longitude.
Here is an example of a 2D wedge (used for 3D simulations) in usual
spherical coordinates and :math:`\alpha=\beta=\pi/6`:

.. image:: /images/wedge.png
        :align: center

**Wedge hamonics** are the eigenfunctions :math:`W_{q,m}` of the
Laplace-Beltrami operator on spherical wedges satisfying
**periodic boundary conditions in both coordinates** :math:`\theta, \phi`:

.. math::
        \nabla^2 W_{q,m} = - \lambda_{q,m} W_{q,m}

Wedge harmonics are suited for the spectral analysis of waves in simulations
of spherical wedges that use periodic boundary conditions,
along :math:`\theta` in 2D :math:`(r, \theta)` simulations (1D wedges)
or :math:`(\theta, \phi)` in 3D :math:`(r, \theta, \phi)` simulations (2D wedges).


Relationship to spherical harmonics
-----------------------------------

Wedge harmonics are indexed by two integers, :math:`q \geq 0, m \geq 0`.
`m` plays a role similar (but not identical) to the azimuthal degree `m`
of spherical harmonics.
`q` plays a role roughly similar to :math:`\ell-|m|` in spherical harmonics.

Like spherical harmonics on a sphere, wedge harmonics form an orthogonal basis
of the periodic functions on the wedge.
Unlike in the case of spherical harmonics, the eigenvalues :math:`\lambda_{q,m}`
depend non-trivially on both `q` and `m` in general.


Wedge harmonics transform
-------------------------

The continuous wedge harmonics transform of a field :math:`f(\theta,\phi)`
is a sequence of complex numbers :math:`\hat f_{q,m}` such that:

.. math::
        f(\theta, \phi) = \sum_{q,m} \hat f_{q,m} W_{q,m}(\theta, \phi)

The discrete 2D transform, implemented in this module, takes a 2D array
of (possibly complex) values :math:`f(\theta_i, \phi_j)` on a grid of points
equispaced in colatitude and longitude, and produces an array
:math:`\hat f_{q,m}` of complex numbers of the same shape.


Angular scales and power spectra
--------------------------------

In the same way that the spherical harmonics coefficients inform about the amount
of signal at different angular scales probed by :math:`\ell`, the wedge harmonics
coefficient :math:`\hat f_{q,m}` contains the amount of signal at scales probed
by mode :math:`q,m`.
Generally speaking, the angular scale probed by a mode (whether spherical,
wedge, Fourier, ...) is directly related to its eigenvalue under the
Laplace-Beltrami operator.

For spherical harmonics, the eigenvalue of mode :math:`\ell,m` is
:math:`\ell (\ell + 1)` and depends only on :math:`\ell`.
We can therefore relate the angular scale of a wedge mode :math:`q,m`
to an approximate spherical harmonics equivalent :math:`\tilde \ell_{q,m}`
by defining :math:`\tilde \ell_{q,m}` using:

.. math::
        \tilde \ell_{q,m} (\tilde \ell_{q,m} + 1) \equiv \lambda_{q,m}

Note that :math:`\tilde \ell` will in general not be an integer,
and will depend on both `q` and `m`.

The way to compute power spectra with wedge harmonics is therefore to bin the
amount of power :math:`|\hat f_{q,m}|^2` in the signal at mode `q,m` into bins
of :math:`\tilde \ell`.

"""

from __future__ import annotations

import enum
import typing
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

import numpy as np
import pandas as pd

from pymusic.grid import UniformGrid1D
from pymusic.utils.ndarray import midpoints

from .fft import fourier_amplitudes_from_signal, signal_from_fourier_amplitudes

if typing.TYPE_CHECKING:
    from numpy.typing import NDArray

    from pymusic.big_array import FloatOrCplx

    EigVals = np.ndarray
    EigVecs = np.ndarray
    EigSys = tuple[EigVals, EigVecs]


TWO_PI = 2.0 * np.pi


def dag(M: np.ndarray) -> np.ndarray:
    return M.conj().T


@dataclass(frozen=True)
class MatrixComparison:
    atol: float = 1e-10
    rtol: float = 1e-10

    def is_equal(self, A: np.ndarray, B: np.ndarray) -> bool:
        return (A.shape == B.shape) and np.allclose(
            A, B, rtol=self.rtol, atol=self.atol
        )

    def is_hermitian(self, mat: np.ndarray) -> bool:
        return self.is_equal(dag(mat), mat)

    def is_anti_hermitian(self, mat: np.ndarray) -> bool:
        return self.is_equal(dag(mat), -mat)

    def has_only_positive_entries(self, mat: np.ndarray) -> bool:
        return bool(np.all(mat > -self.atol))


class DerivOperator(ABC):
    @property
    @abstractmethod
    def matrix(self) -> np.ndarray:
        """The matrix for this derivative operator"""


@dataclass(frozen=True)
class FourierDerivOperator(DerivOperator):
    """The derivative operator in Fourier space for perioric functions sampled
    on the given grid."""

    grid: UniformGrid1D
    matrix_compare: MatrixComparison = MatrixComparison(atol=1e-12, rtol=1e-12)

    @cached_property
    def matrix(self) -> np.ndarray:
        # Matrices of FFT and inverse FFT, i.e.,
        # image of canonical column vectors by FFT and inverse FFT operations
        eye = np.eye(self.grid.num_cells())
        ft = fourier_amplitudes_from_signal(eye, axis=1)
        ift = signal_from_fourier_amplitudes(eye, axis=1)

        # Build the matrix of the derivative operator from its Fourier space
        # representation. The operator should be carefully based on an FD
        # discretization; see e.g.:
        #
        # Sunaina, Butola, M., Khare, K., 2018. Calculating numerical
        # derivatives using Fourier transform: some pitfalls and how to avoid
        # them. Eur. J. Phys. 39, 065806.
        # https://doi.org/10.1088/1361-6404/aadda6
        #
        # Just like for the real-space FD operator, it is important to use the
        # square root of the Laplacian operator, instead of using a naive
        # first-order stencil (u(n+1) - u(n-1)) / (2h) directly, since the
        # square of this last stencil does not reduce to the usual compact
        # second-order derivative FD operator, and is ill-behaved.

        # This derivative operator matrix is in essence identical to the
        # FiniteDifferenceDerivOperator in the periodic case (in the sense that
        # both matrices yield the same Laplacian as their square), but this
        # Fourier implementation does not require invoking sqrtm().

        N = self.grid.num_cells()
        m = np.fft.fftfreq(N, d=1.0) * N  # Fourier mode number
        k = TWO_PI / self.grid.span() * m
        h = self.grid.spacing()

        # The usual second derivative operator expressed in Fourier is:
        #     diff2_hat = diag(2 * (cos(k*h) - 1) / h**2)
        # which, using a double-angle formula for cos(2x), gives its sqrtm:
        half_h = 0.5 * h
        diff_hat = np.diag(1j * np.abs(np.sin(k * half_h)) / half_h)
        # Note that the abs() is not strictly necessary but seems to produce
        # better-conditioned wedge eigensystems, and the square root seems to
        # correspond to what sqrtm() would return.

        diff = (ift).dot(diff_hat).dot(ft)
        assert self.matrix_compare.is_anti_hermitian(diff)
        return diff


class WedgeBCs(str, enum.Enum):
    PERIODIC = "periodic"
    ZERO_VALUE = "zero_value"
    ZERO_DERIVATIVE = "zero_derivative"


def sqrtm_positive_semidefinite(mat: np.ndarray, comp: MatrixComparison) -> np.ndarray:
    """Return a matrix square root of a Hermitian positive semidefinite matrix `mat`,
    based on its spectral decomposition.

    The result is guaranteed to be Hermitian.
    """
    assert comp.is_hermitian(mat)

    eigvals, W = np.linalg.eigh(mat)
    # Eigenvalues should be real and >= 0
    assert comp.is_equal(eigvals, eigvals.real)
    assert comp.has_only_positive_entries(eigvals)

    D = np.diag(eigvals)
    assert comp.is_equal(W @ D @ dag(W), mat)  # Check spectral decomposition

    # New eigenvalues of sqrtm(mat): sqrt(eigenvalues clipped at 0)
    Dsqrt = np.sqrt(np.maximum(D.real, 0.0))
    # Reassemble sqrt(m) in original basis using spectral decomposition
    return W @ Dsqrt @ dag(W)


def sqrtm_negative_semidefinite(mat: np.ndarray, comp: MatrixComparison) -> np.ndarray:
    """Return a matrix square root of a Hermitian negative semidefinite matrix `mat`,
    based on its spectral decomposition.

    The result is guaranteed to be anti-Hermitian.
    """
    return 1j * sqrtm_positive_semidefinite(-mat, comp)


@dataclass(frozen=True)
class FiniteDifferenceDerivOperator(DerivOperator):
    """I am the derivative operator formed by assembling a (Hermitian) finite
    difference matrix for the Laplacian and taking its matrix square root,
    resulting in an anti-Hermitian operator.

    This method ensures that the first derivative operator is anti-Hermitian,
    unlike forming it directly from finite differences, which generally yields
    a non anti-Hermitian operator and results in a Laplacian that is not
    symmetric negative-definite.

    See:

     - Rinehart, R.F., 1960. Skew Matrices as Square Roots.
       The American Mathematical Monthly 67, 157--161.
    """

    grid: UniformGrid1D
    bc: WedgeBCs
    matrix_compare: MatrixComparison = MatrixComparison(atol=1e-12, rtol=1e-12)

    @cached_property
    def matrix(self) -> np.ndarray:
        bc_terms: dict[WedgeBCs, tuple[float, float]] = {
            WedgeBCs.PERIODIC: (-2.0, 1.0),
            WedgeBCs.ZERO_VALUE: (-3.0, 0.0),
            WedgeBCs.ZERO_DERIVATIVE: (-1.0, 0.0),
        }
        diag_term, antidiag_term = bc_terms[self.bc]

        # First construct the standard (1, -2, 1) FD matrix for the Laplacian
        n = self.grid.num_cells()
        lapl = np.diag(-2.0 * np.ones(n))
        lapl += np.diag(np.ones(n - 1), k=1)
        lapl += np.diag(np.ones(n - 1), k=-1)

        # Set the four corner (anti)diagonal terms according to BCs
        lapl[0, 0] = lapl[n - 1, n - 1] = diag_term
        lapl[0, n - 1] = lapl[n - 1, 0] = antidiag_term

        mat = (
            sqrtm_negative_semidefinite(lapl, comp=self.matrix_compare)
            / self.grid.spacing()
        )
        assert self.matrix_compare.is_anti_hermitian(mat)
        return mat


@dataclass(frozen=True)
class SphericalInnerProdOperator:
    r"""The bilinear form B approximating the average-of-product of functions f and g:

    1/|\Omega| \int f(theta) g(theta) d\Omega = F^T.B.G

    on the sphere using the midpoint rule.
    Then note that F^T.B.F is the average power of f on the sphere.
    """

    theta_grid: UniformGrid1D

    @cached_property
    def _diag(self) -> np.ndarray:
        cos_theta = np.cos(self.theta_grid.face_points())
        dcos_theta = np.abs(np.diff(cos_theta))
        # Normalize such that: 1^T.B.1 = 1
        # Note that factors of 2\pi in \phi direction cancel out at numerator
        # and denominator, so we don't need to include them
        return dcos_theta / np.sum(dcos_theta)

    @property
    def matrix(self) -> np.ndarray:
        return np.diag(self._diag)

    @property
    def inv_sqrt_matrix(self) -> np.ndarray:
        return np.diag(1.0 / np.sqrt(self._diag))

    def inner_mat_vec(self, M: np.ndarray, v: np.ndarray) -> np.ndarray:
        r"""Column-wise inner product of matrix M with vector v, i.e. (M^\dagger).B.v;
        result is the vector of inner products of the columns of M with the vector v.
        """
        # Uses the fact that B is diagonal: B_ij = B_i \delta_ij
        return dag(M).dot(self._diag * v)

    def inner_mat_mat(self, P: np.ndarray, Q: np.ndarray) -> np.ndarray:
        # Uses the fact that B is diagonal: (B.Q)_{ij} = B_i Q_{ij}
        BQ = self._diag[:, None] * Q
        return dag(P).dot(BQ)


class EigenSystem(ABC):
    @abstractmethod
    def eig(self) -> EigSys:
        pass


@dataclass(frozen=True)
class WedgeThetaEigenSystem(EigenSystem):
    r"""Solutions (v, W) of the "theta wedge eigenproblem" for a fixed azimuthal mode number m:

        H.W = v B.W,   H := D^\dagger.B.D + m^2 eta^2 (S^{-1})^\dagger.B.(S^{-1})

    where:

        D is an anti-Hermitian derivative operator,
        B is the theta inner product operator (which must be real symmetric positive definite),
        S is the matrix that multiplies a function by sin(theta) pointwise,
        phi_span is the span of the wedge in the azimuthal direction, in radians
        abs_m is the (absolute value of) the azimuthal mode number to solve for
    """

    theta_grid: UniformGrid1D
    diff_op: DerivOperator
    innerp_op: SphericalInnerProdOperator
    phi_span: float
    abs_m: int

    @property
    def eta_abs_m(self) -> float:
        eta = TWO_PI / self.phi_span
        return eta * self.abs_m

    def prob_mat(self) -> np.ndarray:
        """Return the matrix H"""
        D = self.diff_op.matrix

        assert 0.0 < self.phi_span <= TWO_PI
        assert (
            np.abs(self.theta_grid.center() - np.pi / 2.0) < 1e-9
        ), "WedgeThetaEigenSystem: theta_grid must be centered around pi/2 to use wedge harmonics"

        sin_theta = np.sin(self.theta_grid.cell_centers())
        invS_eta_m = np.diag(self.eta_abs_m / sin_theta)

        innerB = self.innerp_op.inner_mat_mat
        return innerB(D, D) + innerB(invS_eta_m, invS_eta_m)

    def reduced_prob_mat(self) -> np.ndarray:
        """Return the Hermitian reduced problem matrix H' = isqrt(B).H.isqrt(B) such that:

            (v, W') eigenpair of H'
        <=>             H'                 .W' = v W'
        <=>             H'.sqrt(B).isqrt(B).W' = v W'
        <=>     sqrt(B).H'.sqrt(B).isqrt(B).W' = v sqrt(B).W'
        <=> [sqrt(B).H'.sqrt(B)].[isqrt(B).W'] = v B.[isqrt(B).W']
        <=>                    H.[isqrt(B).W'] = v B.[isqrt(B).W']
        <=> (v, isqrt(B).W') solves the general eigenproblem
        """
        H = self.prob_mat()
        Bisqrt = self.innerp_op.inv_sqrt_matrix
        return dag(Bisqrt).dot(H).dot(Bisqrt)

    def reduced_eig(self) -> EigSys:
        """Solve the reduced eigenproblem:
        H'.W' = v W'
        """
        Hprime = self.reduced_prob_mat()
        v, Wprime = np.linalg.eigh(Hprime)
        return v, Wprime

    def eig(self) -> EigSys:
        """Solve the general eigenproblem from the reduced eigenproblem, by computing:
        W = isqrt(B).W'

        The resulting eigenvectors W are B-normalized.
        """
        v, Wprime = self.reduced_eig()
        Bisqrt = self.innerp_op.inv_sqrt_matrix
        W = Bisqrt.dot(Wprime)
        # No need to B-normalize W, since Wprime is already identity-normalized
        return v, W

    def residual_weak_formulation(self) -> np.ndarray:
        """Residual matrix for the solved eigensystem in the weak, symmetric formulation"""
        H = self.prob_mat()
        B = self.innerp_op.matrix
        v, W = self.eig()
        return (H @ W) - (B @ W) * v[None, :]

    def residual_strong_formulation(self) -> np.ndarray:
        """Residual in strong, non-symmetric formulation.

        Note that in strong form, the matrix `B` is never used, and `S` appears instead.
        Both `B` and `S` represent the metric of the sphere (`sin(theta)` term).
        Because of small differences in how `B` and `S` are formulated, this can result
        in small differences, probably to second order in the cell size.
        """
        D = self.diff_op.matrix
        sin_theta = np.sin(self.theta_grid.cell_centers())
        S = np.diag(sin_theta)
        invS = np.diag(1.0 / sin_theta)
        invS2 = np.diag(1.0 / sin_theta**2)
        v, W = self.eig()
        return (invS @ D @ S @ D - invS2 * self.eta_abs_m**2) @ W + (W * v[None, :])


@dataclass(frozen=True)
class SortedAndNormalizedEigenSystem(EigenSystem):
    source: EigenSystem
    theta_grid: UniformGrid1D

    def eig(self) -> EigSys:
        v, W = self.source.eig()

        # Sort eigenvalues and eigenvectors in eigenvalue order
        assert np.isrealobj(v)
        sort_order = np.argsort(v)
        v = v[sort_order]
        W = W[:, sort_order]

        # Shift all phase angles to have phase=0 for theta at center of theta interval
        thetas = self.theta_grid.cell_centers()
        for i in range(W.shape[1]):
            W0 = np.interp(self.theta_grid.center(), thetas, W[:, i])
            if np.abs(W0) > 1e-10:
                phase = W0 / np.abs(W0)
            else:
                phase = 1.0
            W[:, i] /= phase

        return v, W


@dataclass(frozen=True)
class WedgeHarmonicsThetaTransform:
    grid: UniformGrid1D
    diff_op: DerivOperator
    inner_prod: SphericalInnerProdOperator
    phi_span: float
    abs_m: int

    @cached_property
    def _cached_eig(self) -> EigSys:
        return SortedAndNormalizedEigenSystem(
            WedgeThetaEigenSystem(
                self.grid,
                self.diff_op,
                self.inner_prod,
                phi_span=self.phi_span,
                abs_m=self.abs_m,
            ),
            self.grid,
        ).eig()

    @property
    def eigvals(self) -> np.ndarray:
        w, _ = self._cached_eig
        return w

    @property
    def modes(self) -> np.ndarray:
        _, V = self._cached_eig
        return V

    def q_mode(self, q: int) -> np.ndarray:
        return self.modes[:, q]

    def transform(self, field: np.ndarray) -> np.ndarray:
        return self.inner_prod.inner_mat_vec(self.modes, field)

    def inverse_transform(self, ampl_q: np.ndarray) -> np.ndarray:
        return (self.modes).dot(ampl_q)

    @property
    def equivalent_ells(self) -> np.ndarray:
        return 0.5 * (np.sqrt(1.0 + 4.0 * self.eigvals) - 1.0)


@dataclass(frozen=True)
class WedgeHarmonicsTransform1D:
    """1D wedge harmonics transform

    :param theta_grid: uniform grid of theta cells to use as support for the transform.
    """

    theta_grid: UniformGrid1D
    bc: WedgeBCs

    @cached_property
    def _xform(self) -> WedgeHarmonicsThetaTransform:
        return WedgeHarmonicsThetaTransform(
            self.theta_grid,
            FiniteDifferenceDerivOperator(self.theta_grid, self.bc),
            SphericalInnerProdOperator(self.theta_grid),
            phi_span=TWO_PI,
            abs_m=0,
        )

    def q_mode(self, q: int) -> np.ndarray:
        "Return the mode function for mode `q`"
        return self._xform.q_mode(q)

    def transform(self, field: np.ndarray) -> np.ndarray:
        "Returns the transform the input `field` array of cell-centered values"
        return self._xform.transform(field)

    def inverse_transform(self, ampl_q: np.ndarray) -> np.ndarray:
        "Returns the inverse transform of the given array of amplitudes"
        return self._xform.inverse_transform(ampl_q)

    @property
    def equivalent_ells(self) -> np.ndarray:
        r"Returns the equivalent ell :math:`\tilde \ell` for each mode `q`"
        return self._xform.equivalent_ells


@dataclass(frozen=True)
class WedgeHarmonicsTransform2D:
    """2D wedge harmonics transform"""

    theta_grid: UniformGrid1D
    phi_grid: UniformGrid1D
    bc: WedgeBCs

    @cached_property
    def theta_diff_op(self) -> DerivOperator:
        return FiniteDifferenceDerivOperator(self.theta_grid, self.bc)

    @cached_property
    def theta_innerp_op(self) -> SphericalInnerProdOperator:
        return SphericalInnerProdOperator(self.theta_grid)

    @cached_property
    def q_xforms(self) -> dict[int, WedgeHarmonicsThetaTransform]:
        # Theta-transforms for each m number; note that all reuse the same operators
        # with a same abs(m), since the theta-transform only depends on abs(m)
        cache = {
            abs_m: WedgeHarmonicsThetaTransform(
                self.theta_grid,
                self.theta_diff_op,
                self.theta_innerp_op,
                phi_span=self.phi_grid.span(),
                abs_m=abs_m,
            )
            for abs_m in set(abs(m) for m in self.m_numbers)
        }
        return {m: cache[abs(m)] for m in self.m_numbers}

    @property
    def q_numbers(self) -> np.ndarray:
        return np.arange(self.theta_grid.num_cells(), dtype="i")

    @property
    def m_numbers(self) -> np.ndarray:
        """Return the m numbers in transform order"""
        n = self.phi_grid.num_cells()
        return np.fft.fftfreq(n, 1.0 / n).astype("i")

    def transform(self, field: np.ndarray) -> np.ndarray:
        assert field.shape == (self.theta_grid.num_cells(), self.phi_grid.num_cells())
        warnings.warn(
            "WedgeHarmonicsTransform2D::transform: using default numpy FFT normalization"
        )

        ampl = fourier_amplitudes_from_signal(field, axis=1)  # ampl[theta,m]
        for im, m in enumerate(self.m_numbers):
            ampl[:, im] = self.q_xforms[m].transform(ampl[:, im])  # ampl[q,m]

        return ampl

    def inverse_transform(self, ampl: np.ndarray) -> np.ndarray:
        assert ampl.shape == (self.theta_grid.num_cells(), self.phi_grid.num_cells())
        warnings.warn(
            "WedgeHarmonicsTransform2D::inverse_transform: using default numpy FFT normalization"
        )

        for im, m in enumerate(self.m_numbers):
            ampl[:, im] = self.q_xforms[m].inverse_transform(
                ampl[:, im]
            )  # ampl[theta,m]
        field = signal_from_fourier_amplitudes(ampl, axis=1)

        return field

    def q_mode(self, q: int, m: int) -> np.ndarray:
        return self.q_xforms[m].q_mode(q)

    def m_mode(self, m: int) -> np.ndarray:
        n = self.phi_grid.num_cells()
        k = np.arange(n)
        assert m in self.m_numbers
        return np.exp(1j * TWO_PI * k * m / n)

    def mode(self, q: int, m: int) -> np.ndarray:
        return (self.q_mode(q, m)[:, None]) * (self.m_mode(m)[None, :])

    @property
    def equivalent_ells(self) -> np.ndarray:
        """2D array of equivalent ell indexed by [q,m] mode"""
        return np.stack(
            [self.q_xforms[m].equivalent_ells for m in self.m_numbers],
            axis=1,
        )


@dataclass(frozen=True)
class WedgeHarmonics2DPowerSpectrum:
    r"""A 2D wedge harmonics power spectrum, calculated on the given `field`

    :param xform: the 2D wedge transform to use for computation
    :param field: the 2D array of field values to compute the spectrum of
    :param ell_eff_bins: bins edges in :math:`\tilde \ell` to use for binning the spectrum
    """

    xform: WedgeHarmonicsTransform2D
    field: NDArray[FloatOrCplx]
    ell_eff_bins: NDArray[np.float64]

    @cached_property
    def _ampl2(self) -> NDArray[np.float64]:
        ampl = self.xform.transform(self.field)
        return np.real(ampl * np.conj(ampl))

    @property
    def _ells(self) -> NDArray[np.float64]:
        return self.xform.equivalent_ells

    @property
    def ell_eff_bin_centers(self) -> NDArray[np.float64]:
        "The array of effective ell bin centers"
        return midpoints(self.ell_eff_bins)

    def total_energy(self) -> NDArray[np.float64]:
        "The total energy of the spectrum in each bin"
        h, _ = np.histogram(self._ells, bins=self.ell_eff_bins, weights=self._ampl2)
        return h

    def mode_counts(self) -> NDArray[np.integer]:
        "The number of wedge modes in each bin"
        h, _ = np.histogram(self._ells, bins=self.ell_eff_bins)
        return h

    def average_energy(self) -> NDArray[np.float64]:
        "The average mode energy in each bin"
        return self.total_energy() / np.maximum(1, self.mode_counts())

    def energy_outside_of_bins(self) -> np.float64:
        "The amount of energy in the signal falling outside of the histogram bins"
        min, max = np.min(self.ell_eff_bins), np.max(self.ell_eff_bins)
        outside = (self._ells < min) | (self._ells > max)
        return np.sum(self._ampl2[outside])

    def dataframe(self) -> pd.DataFrame:
        "Return the spectrum as a `pandas.DataFrame` object"
        return pd.DataFrame(
            {
                "ell_eff": self.ell_eff_bin_centers,
                "ell_eff_bin_left": self.ell_eff_bins[:-1],
                "ell_eff_bin_right": self.ell_eff_bins[1:],
                "total_energy": self.total_energy(),
                "mode_counts": self.mode_counts(),
                "average_energy": self.average_energy(),
            }
        ).set_index("ell_eff")
