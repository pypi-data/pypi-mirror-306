from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property

import numpy as np

from pymusic.big_array.array import BigArray, SummedArray, TakeArray
from pymusic.big_array.index import ItemsIndex1d
from pymusic.utils.ndarray import iter_lines, iter_planes, midpoints

from .wedge_harmonics import WedgeHarmonics2DPowerSpectrum

if typing.TYPE_CHECKING:
    from typing import Callable, Sequence

    from numpy.typing import NDArray

    from pymusic.big_array import FloatOrCplx
    from pymusic.big_array.index import IndexNd

    from .wedge_harmonics import WedgeHarmonicsTransform1D, WedgeHarmonicsTransform2D


class WedgeHarm1DArray(BigArray[np.complex128]):
    def __init__(
        self,
        array: BigArray[FloatOrCplx],
        wedge_harm_xform: WedgeHarmonicsTransform1D,
        theta_axis: str,
        ell_eff_axis: str,
    ):
        """:param array: array to transform
        :param wedge_harm_xform: 1D wedge harmonics transform to apply
        :param theta_axis: axis to transform along
        :param ell_eff_axis: name to use for new ell_eff axis
        """
        self._array = array
        self._wht1d = wedge_harm_xform
        self._theta_axis = theta_axis
        self._ell_eff_axis = ell_eff_axis

    def _with_array(self, arr: BigArray[FloatOrCplx]) -> BigArray[np.complex128]:
        return WedgeHarm1DArray(
            arr,
            self._wht1d,
            self._theta_axis,
            self._ell_eff_axis,
        )

    def _index(self) -> IndexNd:
        return self._array.index.replace(
            self._theta_axis,
            ItemsIndex1d(
                self._ell_eff_axis,
                self._wht1d.equivalent_ells,
            ),
        )

    def array(self) -> np.ndarray:
        assert np.allclose(
            np.asarray(self._array.labels_along_axis(self._theta_axis)),
            self._wht1d.theta_grid.cell_centers(),
        ), "WedgeHarm1DArray: thetas of source array differ from those of the wedge transform"

        return np.apply_along_axis(
            self._wht1d.transform,
            self._array.iaxis(self._theta_axis),
            self._array.array(),
        )

    def take(self, labels: Sequence[object], axis: str) -> BigArray[np.complex128]:
        if axis == self._ell_eff_axis:
            return TakeArray(self, labels, axis)
        else:
            assert axis != self._theta_axis
            return self._with_array(self._array.take(labels, axis))

    def sum(self, axis: str) -> BigArray[np.complex128]:
        if axis == self._ell_eff_axis:
            return SummedArray(self, self._ell_eff_axis)
        else:
            return self._with_array(self._array.sum(axis))


@dataclass(frozen=True)
class WedgeHarm1DPowerSpectrumArray(BigArray[np.float64]):
    source: BigArray[FloatOrCplx]
    wedge_harm_xform: WedgeHarmonicsTransform1D
    theta_axis: str
    ell_eff_axis: str

    @cached_property
    def _pspec_arr(self) -> BigArray[np.float64]:
        return WedgeHarm1DArray(
            self.source,
            self.wedge_harm_xform,
            self.theta_axis,
            self.ell_eff_axis,
        ).abs2()

    def _index(self) -> IndexNd:
        return self._pspec_arr.index

    def array(self) -> np.ndarray:
        return self._pspec_arr.array()

    def take(self, labels: Sequence[object], axis: str) -> BigArray[np.float64]:
        return self._pspec_arr.take(labels, axis)

    def sum(self, axis: str) -> BigArray[np.float64]:
        return self._pspec_arr.sum(axis)


@dataclass(frozen=True)
class WedgeHarm2DPowerSpectrumArray(BigArray[np.float64]):
    """Take the wedge harmonics power spectrum of the input `source` data.

    :param source: the source `BigArray` data to take the spectrum of
    :param wedge_harm_xform: the 2D wedge transform (`WedgeHarmonicsTransform2D`) to use
    :param theta_axis: the label of the theta axis
    :param phi_axis: the label of the phi axis
    :param ell_eff_axis: name to use for new ell_eff axis
    :param ell_eff_bins: bins to use for ell_eff spectrum binning;
        the midpoints of the bins will be used as ell_eff axis labels
        for the power spectrum array
    :param power_quantity: a function that takes a WedgeHarmonics2DPowerSpectrum
        and returns the desired power spectrum quantity for each bin.
        Defaults to returning the total energy in each bin.
    """

    source: BigArray[FloatOrCplx]
    wedge_harm_xform: WedgeHarmonicsTransform2D
    theta_axis: str
    phi_axis: str
    ell_eff_axis: str
    ell_eff_bins: np.ndarray
    power_quantity: Callable[[WedgeHarmonics2DPowerSpectrum], NDArray[np.float64]] = (
        lambda pspec: pspec.total_energy()
    )

    def _with_source(self, source: BigArray[FloatOrCplx]) -> BigArray[np.float64]:
        return WedgeHarm2DPowerSpectrumArray(
            source,
            self.wedge_harm_xform,
            self.theta_axis,
            self.phi_axis,
            self.ell_eff_axis,
            self.ell_eff_bins,
        )

    @property
    def _ell_points(self) -> np.ndarray:
        return midpoints(self.ell_eff_bins)

    def _index(self) -> IndexNd:
        # Replace theta axis with ell_eff (bin centers) labels; drop phi_axis
        return self.source.index.replace(
            self.theta_axis,
            ItemsIndex1d(
                self.ell_eff_axis,
                tuple(self._ell_points),
            ),
        ).drop(self.phi_axis)

    def array(self) -> NDArray[np.float64]:
        assert np.allclose(
            np.asarray(self.source.labels_along_axis(self.theta_axis)),
            self.wedge_harm_xform.theta_grid.cell_centers(),
        ), "WedgeHarm2DPowerSpectrumArray: thetas of source array differ from those of the wedge transform"
        assert np.allclose(
            np.asarray(self.source.labels_along_axis(self.phi_axis)),
            self.wedge_harm_xform.phi_grid.cell_centers(),
        ), "WedgeHarm2DPowerSpectrumArray: phis of source array differ from those of the wedge transform"

        # Input array, obtained from self.source
        arr_in = self.source.array()
        iax_theta_in = self.source.iaxis(self.theta_axis)
        iax_phi_in = self.source.iaxis(self.phi_axis)
        assert arr_in.shape == self.source.shape

        # Output array, obtained from self
        out = np.empty(shape=self.shape, dtype=np.float64)
        iax_ell_out = self.iaxis(self.ell_eff_axis)
        assert out.shape == self.shape

        # Iterate over all matching (theta, phi) input planes and (ell_eff,) output lines
        for input_plane, output_line in zip(
            iter_planes(arr_in.shape, iax_theta_in, iax_phi_in),
            iter_lines(out.shape, iax_ell_out),
        ):
            pspec = WedgeHarmonics2DPowerSpectrum(
                xform=self.wedge_harm_xform,
                field=input_plane.read(source=arr_in),
                ell_eff_bins=self.ell_eff_bins,
            )
            output_line.write(line=self.power_quantity(pspec), dest=out)

        return out

    def take(self, labels: Sequence[object], axis: str) -> BigArray[np.float64]:
        assert axis in self.axes
        if axis != self.ell_eff_axis:
            return self._with_source(self.source.take(labels, axis))
        else:
            return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[np.float64]:
        # Spectrum is not linear so sum does not propagate to `source`:
        return SummedArray(self, axis)
