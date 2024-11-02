from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

import numpy as np

from .array import BigArray, StackedArray, SummedArray, T_co
from .caching import CachedArray

if TYPE_CHECKING:
    from typing import Callable, Sequence

    from numpy.typing import NDArray

    from .index import Index1d, IndexNd


U_contra = TypeVar("U_contra", bound=np.number, contravariant=True)


class MultiApplyArray(BigArray[T_co], Generic[T_co, U_contra]):
    """An array formed by applying multiple functions element-wise to an existing array,
    creating a new axis with a label for each applied function, potentially changing the data type.
    """

    def __init__(
        self,
        array: BigArray[U_contra],
        apply_funcs: Sequence[Callable[[NDArray[U_contra]], NDArray[T_co]]],
        new_index1d: Index1d,
        new_iaxis: int = 0,
    ):
        """
        :param array: source array
        :param apply_funcs: functions to apply element-wise to array
        :param new_index1d: new index to place applied functions along
        :param new_iaxis: location where to insert new axis
        """

        self._array = array
        self._apply_funcs = apply_funcs
        self._new_index1d = new_index1d
        self._new_iaxis = new_iaxis

    def _stack(self, arr: BigArray[U_contra]) -> BigArray[T_co]:
        return StackedArray(
            [arr.apply(f) for f in self._apply_funcs],
            self._new_index1d,
            self._new_iaxis,
        )

    def _index(self) -> IndexNd:
        return self._stack(self._array).index

    def array(self) -> NDArray[T_co]:
        # Make sure to cache the base array, so that we execute its own
        # data pipeline only once
        cached_array = CachedArray(self._array)
        # Stack cached array and get the data
        data = self._stack(cached_array).array()
        # Release the cache and return
        del cached_array
        return data

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        if axis == self._new_index1d.name:
            i_take_funcs = [self._new_index1d.ordinal_index(label) for label in labels]
            return MultiApplyArray(
                self._array,
                [self._apply_funcs[i] for i in i_take_funcs],
                self._new_index1d.take(labels),
                self._new_iaxis,
            )
        else:
            return MultiApplyArray(
                self._array.take(labels, axis),
                self._apply_funcs,
                self._new_index1d,
                self._new_iaxis,
            )

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)


class DerivedFieldArray(BigArray[T_co]):
    """An array formed by combining input variables from another array using a user-provided function"""

    def _index(self) -> IndexNd:
        return self._array.index.drop(self._axis)

    def array(self) -> NDArray[T_co]:
        data = self._array.take(labels=self._inputs, axis=self._axis).array()
        iax = self._array.iaxis(self._axis)
        var_data = [data.take(i, iax) for i, _ in enumerate(self._inputs)]
        return self._formula_func(*var_data)

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return DerivedFieldArray(
            self._array.take(labels, axis),
            self._axis,
            self._inputs,
            self._formula_func,
            self._force_dtype,
        )

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)

    def __init__(
        self,
        array: BigArray,
        axis: str,
        inputs: Sequence[object],
        formula_func: Callable[..., NDArray[T_co]],
        force_dtype: np.dtype | None = None,
    ):
        """
        :param array: input array to derive new quantity from
        :param axis: axis name along which input variables are stored
        :param inputs: list of inputs for user function, specified as a list of
            labels along the desired axis
        :param formula_func: user function from which output is derived, must
            accept :class:`numpy.ndarray` arguments, with exactly as many
            arguments as `inputs` entries, and in the same order
        :param force_dtype: data type of resulting array, obtained from `array` by default
        """
        self._array = array
        self._axis = axis
        self._inputs = inputs
        self._formula_func = formula_func
        self._force_dtype = force_dtype
