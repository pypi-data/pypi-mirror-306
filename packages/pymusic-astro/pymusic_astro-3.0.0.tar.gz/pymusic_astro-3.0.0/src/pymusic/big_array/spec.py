"""
:mod:`spec`: spectral operations on :class:`.BigArray` objects
==============================================================
"""

from __future__ import annotations

import typing
import warnings
from functools import cached_property

import numpy as np

from ..spec.fft import FFTPlan, FourierModes
from .array import BigArray, FC_co, SummedArray, TakeArray
from .exceptions import BigArrayPerformanceWarning
from .index import ItemsIndex1d

if typing.TYPE_CHECKING:
    from typing import Sequence

    from numpy.typing import NDArray

    from ..spec.fft import FFT
    from ..spec.spherical_harmonics import SphericalHarmonicsTransform1D
    from .array import FloatOrCplx
    from .index import IndexNd


class FFTArray(BigArray[np.complex128]):
    """Fast Fourier transform along an array axis"""

    def __init__(
        self, array: BigArray[FloatOrCplx], fft1d: FFT, axis: str, freq_axis: str
    ):
        """:param array: array to transform
        :param fft1d: Fourier transform to apply
        :param axis: axis to transform along
        :param freq_axis: name to use for new frequency axis
        """
        self._array = array
        self._fft1d = fft1d
        self._axis = axis
        self._fq_axis = freq_axis

    @cached_property
    def _plan(self) -> FFTPlan:
        return self._fft1d.plan(
            np.array(self._array.labels_along_axis(self._axis), dtype=np.float64)
        )

    def _index(self) -> IndexNd:
        modes = self._plan.modes
        idx_freq = ItemsIndex1d(self._fq_axis, modes.freqs)
        return self._array.index.replace(self._axis, idx_freq)

    def _compute1d(self, array1d: NDArray[FloatOrCplx]) -> NDArray[np.complex128]:
        return self._plan.fourier_pair(signal=array1d).ampl.astype(np.complex128)

    def array(self) -> NDArray[np.complex128]:
        iax = self._array.iaxis(self._axis)
        return np.apply_along_axis(self._compute1d, iax, self._array.array())

    def take(self, labels: Sequence[object], axis: str) -> BigArray[np.complex128]:
        if axis != self._fq_axis:
            # Taking along non-FFT direction, so take(fft(.)) = fft(take(.))
            return FFTArray(
                self._array.take(labels, axis),
                self._fft1d,
                self._axis,
                self._fq_axis,
            )
        else:
            warnings.warn(
                "taking indices along FFT direction incurs FFT computation along full axis",
                BigArrayPerformanceWarning,
            )
            return TakeArray(self, labels, self._fq_axis)

    def sum(self, axis: str) -> BigArray[np.complex128]:
        # FFT is linear so we can propagate the sum inwards
        if axis != self._fq_axis:
            # Summing along non-FFT direction, so sum(fft(.)) = fft(sum(.))
            return FFTArray(
                self._array.sum(axis),
                self._fft1d,
                self._axis,
                self._fq_axis,
            )
        else:
            warnings.warn(
                "summing along FFT direction incurs full FFT computation along axis",
                BigArrayPerformanceWarning,
            )
            return SummedArray(self, self._fq_axis)


class FFTPowerSpectrumArray(BigArray[np.float64]):
    """Fourier power spectrum along an array axis"""

    def __init__(
        self, array: BigArray[FloatOrCplx], fft1d: FFT, axis: str, freq_axis: str
    ):
        """:param array: array to transform
        :param fft1d: Fourier transform to apply
        :param axis: axis to transform along
        :param freq_axis: name to use for new frequency axis
        """
        self._array = array
        self._fft1d = fft1d
        self._axis = axis
        self._fq_axis = freq_axis

    @cached_property
    def _a_hat(self) -> BigArray[np.complex128]:
        return FFTArray(self._array, self._fft1d, self._axis, self._fq_axis)

    @cached_property
    def _freqs(self) -> tuple[float, ...]:
        # TYPE SAFETY: this implicitly relies on labels of _a_hat to be floats.
        return self._a_hat.labels_along_axis(self._fq_axis)  # type: ignore

    @cached_property
    def _abs_freqs(self) -> NDArray[np.float64]:
        return np.abs(self._freqs)

    @cached_property
    def _pspec_freqs(self) -> NDArray[np.float64]:
        return np.unique(self._abs_freqs)

    def _index(self) -> IndexNd:
        idx_abs_freq = ItemsIndex1d(self._fq_axis, tuple(self._pspec_freqs))
        return self._array.index.replace(self._axis, idx_abs_freq)

    def array(self) -> NDArray[np.float64]:
        iax = self._array.iaxis(self._axis)
        a_hat2 = (
            np.abs(self._a_hat.array()) ** 2
        )  # Compute all squared Fourier amplitudes
        n = len(self._freqs)

        def slc(k: int) -> tuple[int | slice, ...]:
            "Select slice k along axis iax"
            return iax * (slice(None),) + (k,) + (self.ndim - iax - 1) * (slice(None),)

        power = np.zeros(shape=self.shape, dtype=np.float64)
        for k, psfq in enumerate(self._pspec_freqs):
            # NOTE: this assumes an order of frequencies in the FFT (corresponding to default fftfreq),
            # but the matching nu <-> -nu is checked below, so this should be safe
            assert psfq == self._abs_freqs[k]
            k0, k1 = k, (n - k) % n
            sk, sk0, sk1 = slc(k), slc(k0), slc(k1)
            if k0 == k1:
                power[sk] = a_hat2[sk0]
            else:
                assert self._freqs[k0] == -self._freqs[k1]
                power[sk] = a_hat2[sk0] + a_hat2[sk1]

        return power

    def take(self, labels: Sequence[object], axis: str) -> BigArray[np.float64]:
        if axis != self._fq_axis:
            # Taking along non-FFT direction, so take(fft(.)) = fft(take(.))
            return FFTPowerSpectrumArray(
                self._array.take(labels, axis),
                self._fft1d,
                self._axis,
                self._fq_axis,
            )
        else:
            warnings.warn(
                "taking indices along FFT direction incurs FFT computation along full axis",
                BigArrayPerformanceWarning,
            )
            return TakeArray(self, labels, self._fq_axis)

    def sum(self, axis: str) -> BigArray[np.float64]:
        # Power spectrum is non linear, so we can't let the sum traverse, but have to evaluate it here
        return SummedArray(self, axis)


class SphHarm1DArray(BigArray[FC_co]):
    """
    1D spherical harmonics transform
    """

    def __init__(
        self,
        array: BigArray[FC_co],
        sph_harm_xform: SphericalHarmonicsTransform1D,
        theta_axis: str,
        ell_axis: str,
        ells: Sequence[int],
    ):
        r""":param array: array to transform
        :param sph_harm_xform: spherical harmonic transform to use
        :param theta_axis: colatitude axis name
        :param ell_axis: axis name to use for new :math:`\ell` axis in spectral domain
        :param ells: sequence of :math:`\ell` values to compute spectrum for
        """
        self._array = array
        self._sh_xform = sph_harm_xform
        self._theta_axis = theta_axis
        self._ell_axis = ell_axis
        self._ells = ells

    def _index(self) -> IndexNd:
        ell_index = ItemsIndex1d(name=self._ell_axis, labels=tuple(self._ells))
        return self._array.index.replace(self._theta_axis, ell_index)

    def _amplitudes_for_desired_ells(self, arr1d: NDArray[FC_co]) -> NDArray[FC_co]:
        return np.array([self._sh_xform.amplitude(arr1d, ell) for ell in self._ells])

    def array(self) -> NDArray[FC_co]:
        iax = self._array.iaxis(self._theta_axis)  # the axis number to transform along
        arr = self._array.array()  # Obtain untransformed array
        return np.apply_along_axis(self._amplitudes_for_desired_ells, iax, arr)

    def take(self, labels: Sequence[object], axis: str) -> BigArray[FC_co]:
        if axis == self._ell_axis:
            # make new SphHarm1DArray with requested subset of ELLS
            # TYPE SAFETY: the assertion ensures that only integer values of ells
            # are fed to SphHarm1DArray
            assert set(labels).issubset(set(self._ells))
            return SphHarm1DArray(
                self._array,
                self._sh_xform,
                self._theta_axis,
                self._ell_axis,
                labels,  # type: ignore
            )
        else:
            # forward take() to array and then transform
            assert axis != self._theta_axis
            return SphHarm1DArray(
                self._array.take(labels, axis),
                self._sh_xform,
                self._theta_axis,
                self._ell_axis,
                self._ells,
            )

    def sum(self, axis: str) -> BigArray[FC_co]:
        if axis == self._ell_axis:
            # Brute-force sum along ell axis
            return SummedArray(self, axis)
        else:
            # Forward sum to array and transform
            return SphHarm1DArray(
                self._array.sum(axis),
                self._sh_xform,
                self._theta_axis,
                self._ell_axis,
                self._ells,
            )
