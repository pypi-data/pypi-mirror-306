from __future__ import annotations

import time
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Iterator

import numpy as np
from numpy.typing import NDArray
from scipy.special import eval_chebyt, jn

from .fft import (
    FFT,
    FFTPlan,
    FourierModes,
    FourierPair,
    FourierPairFromAmplitudes,
    FourierPairFromSignal,
    GivenPointsSampling,
    Sampling,
    SmartFourierPair,
    UniformSampling,
)
from .windows import WindowFunction


class NuFFTSignalModel(ABC):
    @abstractmethod
    def signal(
        self, sampling: Sampling, usampling: UniformSampling, ampl: NDArray
    ) -> NDArray:
        """Return signal at points from passed Fourier amplitudes"""


@dataclass(frozen=True)
class FixedPointNuFFTSolver:
    """Fixed-point solver for non-uniform FFT.

    :param max_iter: maximum number of fixed point iterations
    :param float max_conv_factor: ratio between successive residuals `resid(it)/resid(it-1)`
        above which to terminate iteration. Should be < 1.
    :param verbosity: verbosity level to use:

        * `<= 0` disables any diagnostic report
        * `>= 1` prints out convergence summary
        * `>= 2` prints out detailed iteration progress
    """

    max_iter: int = 30
    max_conv_factor: float = 0.95
    verbosity: int = 0

    def solve_amplitudes(
        self,
        nufft: NuFFTSignalModel,
        sampling: Sampling,
        usampling: UniformSampling,
        s_tilde: np.ndarray,
    ) -> FourierPair:
        wtime = time.perf_counter()

        s_hat = FourierPairFromSignal(s_tilde, usampling).ampl
        resid, converged, it = np.inf, False, 0

        for it in range(self.max_iter):
            delta_s = s_tilde - nufft.signal(sampling, usampling, s_hat)
            delta_s_hat = FourierPairFromSignal(delta_s, usampling).ampl
            s_hat += delta_s_hat

            last_resid = resid
            resid = np.max(np.abs(delta_s_hat))

            if self.verbosity >= 2:
                print(f"{nufft}: iter={it + 1:02d}, resid={resid:.5e}")

            # Stopping criterion: whenever convergence is starting to stagnate
            converged = resid >= last_resid * self.max_conv_factor
            if converged:
                break

        wtime = time.perf_counter() - wtime

        # Check for good convergence
        if not converged:
            raise RuntimeError(
                f"{nufft}: maximum number of iterations reached without converging"
            )

        if self.verbosity >= 1:
            print(
                f"{nufft}: converged in {it} fixed-point iterations, "
                f"resid={resid:.5e}, wall_time={wtime:.3e} s"
            )

        return FourierPairFromAmplitudes(s_hat, usampling)


@dataclass(frozen=True)
class TaylorNuFFTSignalModel(NuFFTSignalModel):
    r"""
    Signal reconstruction based on a Taylor expansion in
    :math:`\epsilon_i = \tilde t_i - t_i`.

    Formally, convergence is ensured as long as
    :math:`|\epsilon_i|/\Delta t < \ln(2) / (2 \pi) \approx 0.110`.
    """

    num_terms: int

    def gen_taylor_terms(
        self, eps: np.ndarray, s_hat: FourierPair
    ) -> Iterator[FourierPair]:
        """Generates successive Taylor expansion terms for drift `eps` and current guess `s_hat`."""
        # 1/p!, eps^p and F[s^{(p)}] for p=1
        inv_fact_p = 1.0
        eps_p = eps
        s_dp_hat = SmartFourierPair(s_hat).diff()
        yield s_dp_hat.prod_realspace(inv_fact_p * eps_p)

        # successively compute the other terms
        for p in range(2, self.num_terms + 1):
            inv_fact_p = inv_fact_p / p
            eps_p = eps_p * eps
            s_dp_hat = s_dp_hat.diff()
            yield s_dp_hat.prod_realspace(inv_fact_p * eps_p)

    def signal(
        self, sampling: Sampling, usampling: UniformSampling, ampl: NDArray
    ) -> NDArray:
        s_hat = FourierPairFromAmplitudes(ampl, usampling)
        eps = sampling.points - usampling.points
        s_tilde = s_hat.signal  # Order 0
        for term_hat in self.gen_taylor_terms(eps, s_hat):
            ds = (
                term_hat.signal
            )  # FIXME: compute term_hat in real space directly, saves FFTs
            s_tilde = s_tilde + ds
        return s_tilde


def _primed(terms: Iterable[np.ndarray]) -> Iterator[np.ndarray]:
    """Iterate over terms, scaling the first by 0.5 and all other ones by 1.0"""
    iterator = iter(terms)
    # assume at least one term
    yield 0.5 * next(iterator)
    yield from iterator


def _sum_primed(terms: Iterable[np.ndarray]) -> np.ndarray:
    """Sum over all terms, scaling the first by 0.5"""
    # TYPE SAFETY: assume terms is not empty
    return sum(_primed(terms))  # type: ignore


@dataclass(frozen=True)
class ChebNuFFTSignalModel(NuFFTSignalModel):
    r"""
    NuFFT signal reconstruction based on an expansion in Chebyshev polynomials.
    """

    num_terms: int

    def __post_init__(self) -> None:
        num_terms_low = 3
        if self.num_terms <= num_terms_low:
            warnings.warn(
                f"{self.__class__.__name__}: "
                f"num_terms={self.num_terms} is below recommended minimum of {num_terms_low}"
            )

    def _a_pr_coef(self, p: int, r: int, gamma: float) -> float:
        if abs(p - r) % 2 == 0:
            x = -gamma * np.pi / 2.0
            return 4.0 * (1j**r) * jn((p + r) / 2, x) * jn((r - p) / 2, x)
        else:
            return 0.0

    def signal(
        self, sampling: Sampling, usampling: UniformSampling, ampl: NDArray
    ) -> NDArray:
        # NOTE: we choose the convention where this transform uses the (+) sign in the FFT.
        # This is the opposite of the convention used by Ruiz-Antoln & Townsend.
        # Flipping the sign convention amounts to:
        #  - Conjugating u[m](x, y) * v[m](x, y) in the approximation of exp(-ixy) to get exp(ixy);
        #    this is performed in the calculation of u_vecs, since the v[] are real
        #  - Replacing fft() by ifft() when applying the DFT
        assert self.num_terms >= 0

        if self.num_terms == 0:
            return np.zeros_like(ampl)

        # Compute drift epsilon
        eps = sampling.points - usampling.points

        # Compute x and gamma
        x = eps / usampling.delta
        gamma = np.max(np.abs(x))

        # Compute matrix of coefficients A[p, r]
        mat = np.array(
            [
                [self._a_pr_coef(p, r, gamma) for r in range(self.num_terms)]
                for p in range(self.num_terms)
            ]
        )

        # Compute u, v coordinates
        u = x / gamma
        assert np.all(np.abs(u) <= 1)

        modes = FourierModes(usampling)
        k, k_mid = modes.mode_nums, 0.0  # k \in [-n/2, n/2] so centered on 0
        f0 = 2.0 * np.pi / modes.n  # conversion from k to y
        y, y_mid = f0 * k, f0 * k_mid
        v = (y - y_mid) / np.pi
        assert np.all(np.abs(v) <= 1)

        # Compute u_r vectors
        u_vecs = [
            _sum_primed(
                # See note above for why we conj()
                np.conj(mat[p, r] * np.exp(-1j * y_mid * x) * eval_chebyt(p, u))
                for p in range(self.num_terms)
            )
            for r in range(self.num_terms)
        ]

        # Compute v_r vectors
        v_vecs = list(_primed(eval_chebyt(r, v) for r in range(self.num_terms)))

        # Forward NuFFT
        signal = sum(
            u_vecs[r] * FourierPairFromAmplitudes(v_vecs[r] * ampl, usampling).signal
            for r in range(self.num_terms)
        )
        # TYPE SAFETY: this is safe as we know num_terms > 0 at this point, so
        # sum won't just return 0
        return signal  # type: ignore


@dataclass(frozen=True)
class NuFFT1DPlan(FFTPlan):
    window: WindowFunction
    sampling: Sampling
    sampling_period: float
    spacing_tol: float = 0.110
    signal_model: NuFFTSignalModel = TaylorNuFFTSignalModel(num_terms=8)
    solver: FixedPointNuFFTSolver = FixedPointNuFFTSolver()

    @cached_property
    def modes(self) -> FourierModes:
        return FourierModes(self._usampling)

    @cached_property
    def _x0(self) -> float:
        # Pick an origin point that minimizes average epsilon**2
        n = self.sampling.num_points
        return np.mean(self.sampling.points - np.arange(n) * self.sampling_period)

    @cached_property
    def _phase0(self) -> NDArray[np.complex128]:
        """Phase factor corresponding to starting at x0"""
        return self.modes.shift_phase_factor(self._x0)

    @cached_property
    def _usampling(self) -> UniformSampling:
        n = self.sampling.num_points
        delta = self.sampling_period
        us = UniformSampling(x0=self._x0, num_points=n, delta=delta)
        max_relative_epsilon = np.max(np.abs(self.sampling.points - us.points)) / delta
        if max_relative_epsilon >= self.spacing_tol:
            raise RuntimeError(
                f"non-uniform samples deviate by {max_relative_epsilon} "
                f"which exceeds requested spacing_tol={self.spacing_tol}"
            )
        return us

    @cached_property
    def _window_values(self) -> NDArray:
        u_tilde = self.sampling.u_points
        assert np.all((u_tilde >= 0) & (u_tilde < 1))
        return self.window.window_func(u_tilde)

    def fourier_pair(self, signal: NDArray) -> FourierPair:
        win_signal = self._window_values * signal
        ampl: FourierPair = self.solver.solve_amplitudes(
            self.signal_model, self.sampling, self._usampling, win_signal
        )
        return FourierPairFromAmplitudes(ampl.ampl * self._phase0, self._usampling)


@dataclass(frozen=True)
class NuFFT1D(FFT):
    r"""
    One-dimensional non-uniform Fourier transform.

    For signals sampled on non-uniform sampling points :math:`\tilde t_i`,
    this transform iteratively recovers the Fourier amplitudes of the signal
    if it were sampled on uniform points :math:`t_i` of spacing :math:`\Delta t`.

    :param window: window function to use
    :param sampling_period: specify uniform time delta to use for uniform sampling
    :param spacing_tol: relative tolerance on maximum drift in sampling points
    :param signal_model: `NuFFTSignalModel` to use for signal reconstruction
    :param solver: solver to use for forward NuFFT
    """

    window: WindowFunction
    sampling_period: float
    spacing_tol: float = 0.110
    signal_model: NuFFTSignalModel = TaylorNuFFTSignalModel(num_terms=8)
    solver: FixedPointNuFFTSolver = FixedPointNuFFTSolver()

    def plan(self, sample_points: NDArray) -> FFTPlan:
        return NuFFT1DPlan(
            window=self.window,
            sampling=GivenPointsSampling(
                sample_points=sample_points,
                span_=len(sample_points) * self.sampling_period,
            ),
            sampling_period=self.sampling_period,
            spacing_tol=self.spacing_tol,
            signal_model=self.signal_model,
            solver=self.solver,
        )
