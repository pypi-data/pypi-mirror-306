from __future__ import annotations

import typing

import numpy as np

from .array import ConcatenatedArray, ItemsIndex1d, StackedArray
from .derived import DerivedFieldArray

if typing.TYPE_CHECKING:
    from typing import Sequence

    from .array import BigArray


class _VelComponents:
    def __init__(self, all_vars: Sequence[object]):
        self.all_vars = all_vars

    @property
    def vel_comp_vars(self) -> list[object]:
        vel_vars = [v for v in self.all_vars if v in ["vel_1", "vel_2", "vel_3"]]
        assert len(vel_vars) > 0
        return vel_vars

    def mag2(self, v_comp_arrays: Sequence[np.ndarray]) -> np.ndarray:
        assert len(v_comp_arrays) == len(self.vel_comp_vars)
        return np.sum([v**2 for v in v_comp_arrays], axis=0)

    def mag(self, v_comp_arrays: Sequence[np.ndarray]) -> np.ndarray:
        return np.sqrt(self.mag2(v_comp_arrays))


def vel_mag_array(array: BigArray, var_axis: str = "var") -> BigArray:
    v_comps = _VelComponents(array.labels_along_axis(var_axis))
    return DerivedFieldArray(
        array,
        var_axis,
        inputs=v_comps.vel_comp_vars,
        formula_func=lambda *vc_arrs: v_comps.mag(vc_arrs),
    )


def e_kin_density_array(array: BigArray, var_axis: str = "var") -> BigArray:
    v_comps = _VelComponents(array.labels_along_axis(var_axis))
    inputs: list[object] = ["density"]
    inputs.extend(v_comps.vel_comp_vars)
    return DerivedFieldArray(
        array,
        var_axis,
        inputs=inputs,
        formula_func=lambda rho, *vc_arrs: 0.5 * rho * v_comps.mag2(vc_arrs),
    )


def adiabatic_press(rho: np.ndarray, e_int: np.ndarray, gamma: float) -> np.ndarray:
    return e_int * rho * (gamma - 1.0)


def adiabatic_press_array(
    array: BigArray, var_axis: str = "var", gamma: float = 5.0 / 3.0
) -> BigArray:
    return DerivedFieldArray(
        array,
        var_axis,
        inputs=["density", "e_int_spec"],
        formula_func=lambda rho, e_int: adiabatic_press(rho, e_int, gamma),
    )


def adiabat(rho: np.ndarray, e_int: np.ndarray, gamma: float) -> np.ndarray:
    p = adiabatic_press(rho, e_int, gamma)
    return p / (rho**gamma)


def adiabat_array(
    array: BigArray, var_axis: str = "var", gamma: float = 5.0 / 3.0
) -> BigArray:
    return DerivedFieldArray(
        array,
        var_axis,
        inputs=["density", "e_int_spec"],
        formula_func=lambda rho, e_int: adiabat(rho, e_int, gamma),
    )


def add_all_physics(
    array: BigArray, var_axis: str = "var", gamma: float = 5.0 / 3.0
) -> BigArray:
    phys_arrays = {
        "vel_mag": vel_mag_array(array, var_axis),
        "e_kin_density": e_kin_density_array(array, var_axis),
        "adiabatic_pressure": adiabatic_press_array(array, var_axis, gamma),
        "adiabat": adiabat_array(array, var_axis, gamma),
    }
    new_phys_array = StackedArray(
        tuple(phys_arrays.values()),
        ItemsIndex1d(var_axis, tuple(phys_arrays.keys())),
        array.iaxis(var_axis),
    )
    return ConcatenatedArray([array, new_phys_array], var_axis)
