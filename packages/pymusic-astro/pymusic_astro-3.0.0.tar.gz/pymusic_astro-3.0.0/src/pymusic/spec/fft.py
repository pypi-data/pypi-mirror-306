from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Iterator

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from .windows import WindowFunction


def fourier_amplitudes_from_signal(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """FFT, properly normalized so that the amplitude of a single complex
    exponential signal exp(1j*omega*t) is 1.0 for mode omega.

    This ensures that the average power in mode omega is |s_hat(omega)|^2,
    which is the "right" convention to use, see e.g.:

    Heinzel, G., Rudiger, A., Schilling, R., 2002.
    Spectrum and spectral density estimation by the Discrete Fourier transform
    (DFT), including a comprehensive list of window functions and some new
    flat-top windows.
    https://pure.mpg.de/pubman/faces/ViewItemOverviewPage.jsp?itemId=item_152164
    """
    return np.fft.fft(x, axis=axis, norm="forward")


def signal_from_fourier_amplitudes(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Inverse of fourier_amplitudes_from_signal"""
    return np.fft.ifft(x, axis=axis, norm="forward")


class Sampling(ABC):
    """Base class for all samplings, i.e. ordered sequence of points inside a
    large sampling interval, the `span`, which is assumed to correspond to the
    true period of the sampled signal."""

    @property
    @abstractmethod
    def points(self) -> np.ndarray:
        """The sampling points"""

    @property
    @abstractmethod
    def span(self) -> float:
        """The total time span of the sampling duration; this is also the
        period of the periodic signal"""

    @cached_property
    def num_points(self) -> int:
        """The number of sampling points"""
        return len(self.points)

    @property
    def u_points(self) -> np.ndarray:
        x = self.points
        u = (x - x[0]) / self.span
        return u


@dataclass(frozen=True)
class GivenPointsSampling(Sampling):
    sample_points: NDArray
    span_: float

    @property
    def points(self) -> np.ndarray:
        return self.sample_points

    @property
    def span(self) -> float:
        return self.span_


@dataclass(frozen=True)
class UniformSampling(Sampling):
    x0: float
    delta: float
    num_points: int

    def __post_init__(self) -> None:
        assert self.num_points > 0
        assert self.delta > 0.0

    @cached_property
    def points(self) -> np.ndarray:
        return self.x0 + np.arange(self.num_points) * self.delta

    @property
    def span(self) -> float:
        return self.num_points * self.delta


def make_uniform_sampling_from_points(
    sample_points: NDArray, spacing_tol: float
) -> UniformSampling:
    n = len(sample_points)
    assert n >= 2
    delta = (sample_points[-1] - sample_points[0]) / (n - 1)
    assert delta > 0.0
    us = UniformSampling(x0=sample_points[0], num_points=n, delta=delta)
    max_relative_epsilon = np.abs(sample_points - us.points).max() / delta
    if max_relative_epsilon >= spacing_tol:
        raise RuntimeError(
            f"non-uniform samples deviate by {max_relative_epsilon} "
            f"which exceeds requested spacing_tol={spacing_tol}"
        )
    return us


@dataclass(frozen=True)
class FourierModes:
    """Fourier modes for a given uniform sampling"""

    usampling: UniformSampling

    @cached_property
    def n(self) -> int:
        return self.usampling.num_points

    @cached_property
    def freqs(self) -> np.ndarray:
        """Frequencies, in physical units"""
        return np.fft.fftfreq(self.n, self.usampling.delta)

    @cached_property
    def omegas(self) -> np.ndarray:
        """Angular frequencies"""
        return 2.0 * np.pi * self.freqs

    @cached_property
    def mode_nums(self) -> np.ndarray:
        """Mode numbers, in [-N/2, N/2], as provided by `numpy.fft.fftfreq`"""
        return np.rint(np.fft.fftfreq(self.n, 1.0 / self.n))

    def shift_phase_factor(self, shift: float) -> NDArray[np.complex128]:
        """Phase factor for each mode, corresponding to a real-space shift of `shift`,
        i.e. if t = t0 + t', and A[w] are the amplitudes for modes exp(i*w*t'), then
        A[w] * shift_phase_factor[w] are the amplitudes for modes exp(i*w*t).
        """
        # A[w] exp(i*w*t') = A[w] exp(-i*w*t0) exp(i*w*t), so:
        return np.exp(-1j * self.omegas * shift)


class FourierPair(ABC):
    @property
    @abstractmethod
    def signal(self) -> NDArray:
        """Signal for this pair"""

    @property
    @abstractmethod
    def uniform_sampling(self) -> UniformSampling:
        """Uniform sampling (real-space points)"""

    @property
    @abstractmethod
    def ampl(self) -> NDArray:
        """Fourier amplitudes for this pair"""

    @property
    def modes(self) -> FourierModes:
        return FourierModes(self.uniform_sampling)


@dataclass(frozen=True)
class FourierPairFromSignal(FourierPair):
    signal_: NDArray
    uniform_sampling_: UniformSampling

    @property
    def signal(self) -> NDArray:
        return self.signal_

    @property
    def uniform_sampling(self) -> UniformSampling:
        return self.uniform_sampling_

    @cached_property
    def ampl(self) -> NDArray:
        return fourier_amplitudes_from_signal(self.signal)


@dataclass(frozen=True)
class FourierPairFromAmplitudes(FourierPair):
    ampl_: NDArray
    uniform_sampling_: UniformSampling

    @property
    def ampl(self) -> NDArray:
        return self.ampl_

    @property
    def uniform_sampling(self) -> UniformSampling:
        return self.uniform_sampling_

    @cached_property
    def signal(self) -> NDArray:
        return signal_from_fourier_amplitudes(self.ampl)


@dataclass(frozen=True)
class SmartFourierPair(FourierPair):
    pair: FourierPair

    # Implementation of FourierPair interface

    @property
    def signal(self) -> NDArray:
        return self.pair.signal

    @property
    def uniform_sampling(self) -> UniformSampling:
        return self.pair.uniform_sampling

    @property
    def ampl(self) -> NDArray:
        return self.pair.ampl

    @property
    def modes(self) -> FourierModes:
        return self.pair.modes

    # Some helper constructors

    def _with_ampl(self, ampl: NDArray) -> SmartFourierPair:
        return SmartFourierPair(FourierPairFromAmplitudes(ampl, self.uniform_sampling))

    def _with_signal(self, signal: NDArray) -> SmartFourierPair:
        return SmartFourierPair(FourierPairFromSignal(signal, self.uniform_sampling))

    # Some simple algebraic operations

    def diff(self, order: int = 1) -> SmartFourierPair:
        """Fourier differentiation"""
        assert order >= 0
        return self._with_ampl(((1j * self.modes.omegas) ** order) * self.ampl)

    def prod_realspace(self, arr: NDArray) -> SmartFourierPair:
        """Multiply by `arr` in real space"""
        return self._with_signal(self.signal * arr)

    # Useful quantities for e.g. power spectra

    @cached_property
    def mag2(self) -> np.ndarray:
        """Square magnitudes"""
        return np.real(self.ampl * self.ampl.conj())

    @cached_property
    def mag(self) -> np.ndarray:
        """Magnitudes"""
        return np.sqrt(self.mag2)

    @cached_property
    def magnitude_spectrum(self) -> pd.Series:
        """Magnitude spectrum"""
        df = pd.DataFrame({"freq": np.abs(self.modes.freqs), "mag2": self.mag2})
        return df.groupby("freq")["mag2"].mean().apply(np.sqrt).sort_index()  # type: ignore

    @cached_property
    def power_spectrum(self) -> pd.Series:
        """Power spectrum"""
        df = pd.DataFrame({"freq": np.abs(self.modes.freqs), "mag2": self.mag2})
        return df.groupby("freq")["mag2"].sum().sort_index()  # type: ignore


class FFTPlan(ABC):
    @property
    @abstractmethod
    def modes(self) -> FourierModes:
        """Return the Fourier modes"""

    @abstractmethod
    def fourier_pair(self, signal: NDArray) -> FourierPair:
        """Return the Fourier transform pair for the signal"""


class FFT(ABC):
    """
    Base class for one-dimensional Fourier transforms
    """

    @abstractmethod
    def plan(self, sample_points: NDArray) -> FFTPlan:
        """Return a plan (concrete, cached FFT) for the given sampling points"""


@dataclass(frozen=True)
class FFT1DPlan(FFTPlan):
    usampling: UniformSampling
    window: WindowFunction

    @cached_property
    def modes(self) -> FourierModes:
        return FourierModes(self.usampling)

    @cached_property
    def _window_values(self) -> NDArray:
        return self.window.window_func(self.usampling.u_points)

    def fourier_pair(self, signal: NDArray) -> FourierPair:
        return FourierPairFromSignal(self._window_values * signal, self.usampling)


@dataclass(frozen=True)
class FFT1D(FFT):
    """
    One-dimensional Fourier transform for equispaced data

    :param window: window function to use,
        see https://en.wikipedia.org/wiki/Window_function.
        Use a :class:`.NoWindow` instance for non-windowed transforms.
        :class:`.BlackmanWindow` is a good general-purpose choice.
        Note that in general, you might want to create a normalized window using
        :class:`.NormalizedWindow` in order to e.g. preserve the signal power
        by passing it `normalization=PreservePower()`.
        See also :class:`.PreservePower` and :class:`.PreserveAmplitudes`.
    :param spacing_tol: relative tolerance to enforce
        for uniform spacing between sampling points
    """

    window: WindowFunction
    spacing_tol: float = 1e-10

    def plan(self, sample_points: NDArray) -> FFTPlan:
        us = make_uniform_sampling_from_points(sample_points, self.spacing_tol)
        return FFT1DPlan(usampling=us, window=self.window)


@dataclass(frozen=True)
class Signal:
    """A periodic smooth signal with power-law distributed modes in [k_min, k_max]"""

    period: float
    k_min: int
    k_max: int
    spec_index: float
    real: bool = True
    seed: int = 42

    def _re_if_real(self, x: np.ndarray) -> np.ndarray:
        if self.real:
            return np.real(x)
        else:
            return x

    @cached_property
    def nmodes(self) -> int:
        return self.k_max - self.k_min + 1

    @cached_property
    def modes(self) -> np.ndarray:
        return np.arange(self.k_min, self.k_max + 1)

    @cached_property
    def amplitudes(self) -> np.ndarray:
        ampl = self.modes**self.spec_index
        ampl /= np.sqrt(np.sum(ampl**2))  # Roughly normalize RMS of signal to 1
        return ampl

    @cached_property
    def phases(self) -> np.ndarray:
        state = np.random.RandomState(seed=self.seed)
        return state.uniform(low=0.0, high=2.0 * np.pi, size=self.nmodes)

    def iter_modes(self) -> Iterator[tuple[float, float, float]]:
        "Iterate over (omega, amplitude, phase) for all modes of signal"
        for m, ampl, phi in zip(self.modes, self.amplitudes, self.phases):
            yield 2.0 * np.pi * m / self.period, ampl, phi

    def signal(self, t: np.ndarray) -> np.ndarray:
        "Evaluate signal at times t"
        s = np.zeros_like(t, dtype="complex")
        for omega, ampl, phi in self.iter_modes():
            s += ampl * np.exp(1j * (omega * t + phi))
        return self._re_if_real(s)

    def signal_diff(self, t: np.ndarray, n: int = 1) -> np.ndarray:
        "n-th derivative of signal at times t"
        assert n >= 0
        ds = np.zeros_like(t, dtype="complex")
        for omega, ampl, phi in self.iter_modes():
            ds = ds + self._re_if_real(
                ampl * ((1j * omega) ** n) * np.exp(1j * (omega * t + phi))
            )
        return self._re_if_real(ds)
