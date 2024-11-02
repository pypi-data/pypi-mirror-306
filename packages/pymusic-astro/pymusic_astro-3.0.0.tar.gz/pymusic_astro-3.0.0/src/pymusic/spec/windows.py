"""
References:

  - [H78] Harris, J., 1978.
    On the Use of Windows for Harmonic Analysis with the Discrete Fourier
    Transform. Proceedings of the IEEE 66.

  - [HRS02] Heinzel, G., Rudiger, A., Schilling, R., 2002.
    Spectrum and spectral density estimation by the Discrete Fourier transform
    (DFT), including a comprehensive list of window functions and some new
    flat-top windows.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

import numpy as np
from scipy.integrate import quad

from ..math.slicing import slice_bcast_1d


class WindowFunction(ABC):
    """Base class for window functions"""

    @abstractmethod
    def window_func(self, u: np.ndarray) -> np.ndarray:
        """
        :param u: values in [0, 1] at which to evaluate window function
        :return: 1d array of window function values for domain [0, 1]
        """
        pass


class NoWindow(WindowFunction):
    """Don't apply any windowing to input signal"""

    def window_func(self, u: np.ndarray) -> np.ndarray:
        return np.ones_like(u)


class BlackmanWindow(WindowFunction):
    """Blackman window, a good general-purpose window, see :func:`numpy.blackman` and
    https://en.wikipedia.org/wiki/Window_function#Blackman_window
    """

    def window_func(self, u: np.ndarray) -> np.ndarray:
        v = 2.0 * np.pi * u
        return 0.42 - 0.5 * np.cos(v) + 0.08 * np.cos(2.0 * v)


class NuttallWindow(WindowFunction):
    """Nuttall window, with very low side-lobes but relatively broad main lobe
    and therefore lower frequency resolution.

    https://en.wikipedia.org/wiki/Window_function#Nuttall_window,_continuous_first_derivative
    """

    a0: float = 0.355768
    a1: float = 0.487396
    a2: float = 0.144232
    a3: float = 0.012604

    def window_func(self, u: np.ndarray) -> np.ndarray:
        v = 2.0 * np.pi * u
        return (
            self.a0
            - self.a1 * np.cos(v)
            + self.a2 * np.cos(2.0 * v)
            - self.a3 * np.cos(3.0 * v)
        )


class HannWindow(WindowFunction):
    """Hann window, with narrow main lobe (high resolution in frequency)
    but slowly tapering off side-lobes (significant spectral leakage).

    https://en.wikipedia.org/wiki/Hann_function
    """

    def window_func(self, u: np.ndarray) -> np.ndarray:
        v = np.pi * u
        return np.sin(v) ** 2


class WindowNormalization(ABC):
    @abstractmethod
    def linear_scale_factor(self, window: WindowFunction) -> float:
        """For the given WindowFunction, return the factor to multiply windowed
        amplitudes by (or equivalently, the window function itself) to obtain
        the desired normalization"""


@dataclass(frozen=True)
class PreserveAmplitudes(WindowNormalization):
    """Window normalization that (approximately) preserves Fourier amplitudes
    of the signal"""

    def linear_scale_factor(self, window: WindowFunction) -> float:
        w_avg = quad(window.window_func, 0.0, 1.0)[0]
        return 1.0 / w_avg


@dataclass(frozen=True)
class PreservePower(WindowNormalization):
    """Window normalization that (approximately) preserves the Fourier power
    spectrum of the signal"""

    def linear_scale_factor(self, window: WindowFunction) -> float:
        w2_avg = quad(lambda u: window.window_func(u) ** 2, 0.0, 1.0)[0]
        return 1.0 / np.sqrt(w2_avg)


@dataclass(frozen=True)
class NormalizedWindow(WindowFunction):
    window: WindowFunction
    normalization: WindowNormalization

    @cached_property
    def scale_factor(self) -> float:
        return self.normalization.linear_scale_factor(self.window)

    def window_func(self, u: np.ndarray) -> np.ndarray:
        return self.scale_factor * self.window.window_func(u)
