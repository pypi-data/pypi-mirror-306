"""
:mod:`.diff`: derivatives on :class:`.BigArray` objects
=======================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic

import numpy as np

from .array import BigArray, SummedArray, T_co, TakeArray
from .caching import CachedArray
from .index import ItemsIndex1d

if TYPE_CHECKING:
    from typing import Literal, Sequence, TypeAlias

    from numpy.typing import NDArray

    from .array import U
    from .index import IndexNd

    EdgeOrder: TypeAlias = Literal[1 | 2]


class Partials(BigArray[T_co]):
    """Partial first derivatives using second-order finite differences;
    see :func:`numpy.gradient`.
    """

    def __init__(
        self,
        array: BigArray[T_co],
        diff_axes: Sequence[str],
        result_axis: str = "partials",
        edge_order: EdgeOrder = 2,
    ):
        self._array = array
        self._diff_axes = diff_axes
        self._result_axis = result_axis
        self._edge_order = edge_order

    def _index(self) -> IndexNd:
        return self._array.index.insert(
            0, ItemsIndex1d(name=self._result_axis, labels=tuple(self._diff_axes))
        )

    def array(self) -> NDArray[T_co]:
        g = np.gradient(
            self._array.array(),
            *[np.array(self.labels_along_axis(ax)) for ax in self._diff_axes],
            axis=tuple(self._array.index.iaxis(ax) for ax in self._diff_axes),
            edge_order=self._edge_order,
        )
        if self._array.ndim == 1:
            return np.array([g])
        return np.array(g)

    def _applied_to_array(self, arr: BigArray[U]) -> BigArray[U]:
        return Partials(
            arr,
            self._diff_axes,
            self._result_axis,
            self._edge_order,
        )

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        if axis in self._diff_axes or axis == self._result_axis:
            return TakeArray(self, labels, axis)
        return self._applied_to_array(self._array.take(labels, axis))

    def sum(self, axis: str) -> BigArray[T_co]:
        if axis in self._diff_axes or axis == self._result_axis:
            return SummedArray(self, axis)
        return self._applied_to_array(self._array.sum(axis))


class PolarVectorGradient(BigArray[T_co]):
    """Gradient of vector field in 2D polar coordinates."""

    def __init__(
        self,
        vec: BigArray[T_co],
        r_axis: str,
        theta_axis: str,
        comp_axis: str,
        r_comp: str,
        theta_comp: str,
        grad_axis: str,
    ):
        # TODO needs to add more meaning through some more meaningful object, TensorField or so
        self._vec = vec
        self._r_axis = r_axis
        self._theta_axis = theta_axis
        self._comp_axis = comp_axis
        self._r_comp = r_comp
        self._theta_comp = theta_comp
        self._grad_axis = grad_axis

    def _index(self) -> IndexNd:
        index = self._vec.index
        comp_index = index.index1d(self._comp_axis).take(
            [self._r_comp, self._theta_comp]
        )
        grad_index = ItemsIndex1d(
            name=self._grad_axis, labels=(self._r_axis, self._theta_axis)
        )
        # In order, we:
        #  * Remove component axis
        #  * Left insert gradient direction axis
        #  * Left insert component axis
        # So that final shape is (comp, grad_dir, ...)
        return index.drop(self._comp_axis).insert(0, grad_index).insert(0, comp_index)

    def array(self) -> NDArray[T_co]:
        d1, d2 = self._r_axis, self._theta_axis
        c1, c2 = self._r_comp, self._theta_comp

        # Make a cached version of self._vec, since we will be accessing it heavily
        vec = CachedArray(self._vec)

        # Compute partial derivatives
        du_dx = CachedArray(
            Partials(
                vec,
                (self._r_axis, self._theta_axis),
                result_axis=self._grad_axis,
                edge_order=2,
            )
        )
        du1_dx1 = du_dx.xs(c1, self._comp_axis).xs(d1, self._grad_axis)
        du2_dx1 = du_dx.xs(c2, self._comp_axis).xs(d1, self._grad_axis)
        du1_dx2 = du_dx.xs(c1, self._comp_axis).xs(d2, self._grad_axis)
        du2_dx2 = du_dx.xs(c2, self._comp_axis).xs(d2, self._grad_axis)

        def bcast_along_axis(arr: np.ndarray, axis: int, ndim: int) -> np.ndarray:
            # TODO move out
            shape = tuple(1 if i != axis else -1 for i in range(ndim))
            return np.reshape(arr, shape)

        u1 = vec.xs(c1, self._comp_axis)
        u2 = vec.xs(c2, self._comp_axis)

        inv_r = 1.0 / bcast_along_axis(
            np.array(vec.labels_along_axis(self._r_axis)),
            u1.iaxis(self._r_axis),
            u1.ndim,
        )

        assert u1.index == du2_dx1.index
        return np.array(
            # TYPE SAFETY: this is safe as long as labels are numbers
            [
                [du1_dx1.array(), inv_r * (du1_dx2.array() - u2.array())],  # type: ignore
                [du2_dx1.array(), inv_r * (du2_dx2.array() + u1.array())],  # type: ignore
            ]
        )

    def _applied_to_array(self, vec: BigArray[U]) -> BigArray[U]:
        return PolarVectorGradient(
            vec,
            self._r_axis,
            self._theta_axis,
            self._comp_axis,
            self._r_comp,
            self._theta_comp,
            self._grad_axis,
        )

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        # If taking along component axis, gradient axis, or one of the space dimensions,
        # then take() *cannot* be propagated inside the gradient
        if axis in {self._comp_axis, self._grad_axis, self._r_axis, self._theta_axis}:
            return TakeArray(self, labels, axis)

        # Otherwise, we can safely do grad(take(...))
        return self._applied_to_array(self._vec.take(labels, axis))

    def sum(self, axis: str) -> BigArray[T_co]:
        # Same reasoning as take() here, because the gradient is linear
        if axis in {self._comp_axis, self._grad_axis, self._r_axis, self._theta_axis}:
            return SummedArray(self, axis)
        return self._applied_to_array(self._vec.sum(axis))


class TensorToDict(Generic[T_co]):
    def __init__(
        self,
        tensor_arr: BigArray[T_co],
        rows: Sequence[object],
        row_axis: str,
        cols: Sequence[object],
        col_axis: str,
    ):
        self.tensor_arr = tensor_arr
        self.rows = rows
        self.row_axis = row_axis
        self.cols = cols
        self.col_axis = col_axis
        assert len(self.rows) == len(self.cols)

    @property
    def ndim(self) -> int:
        return len(self.rows)

    @property
    def idims(self) -> range:
        return range(self.ndim)

    def dict(self) -> dict[tuple[int, int], NDArray[T_co]]:
        cached_tensor = CachedArray(self.tensor_arr)
        rax = self.row_axis
        cax = self.col_axis
        return {
            (i, j): cached_tensor.xs(row, axis=rax).xs(col, axis=cax).array()
            for i, row in enumerate(self.rows)
            for j, col in enumerate(self.cols)
        }


class SymmetrizedTensor(BigArray[T_co]):
    """Symmetric (Hermitian) part of tensor T, using regular (Euclidean) Hermitian transpose T^*"""

    def __init__(
        self,
        tensor: BigArray[T_co],
        rows: Sequence[object],
        row_axis: str,
        cols: Sequence[object],
        col_axis: str,
    ):
        self._tensor = tensor
        self._rows = rows
        self._row_axis = row_axis
        self._cols = cols
        self._col_axis = col_axis

    def _index(self) -> IndexNd:
        index = self._tensor.index
        row_index = index.index1d(self._row_axis).take(self._rows)
        col_index = index.index1d(self._col_axis).take(self._cols)
        return (
            index.drop(self._row_axis)
            .drop(self._col_axis)
            .insert(0, col_index)
            .insert(0, row_index)
        )

    def array(self) -> NDArray[T_co]:
        td = TensorToDict(
            self._tensor,
            self._rows,
            self._row_axis,
            self._cols,
            self._col_axis,
        )
        a = td.dict()
        return np.array(
            [[0.5 * (a[i, j] + np.conj(a[j, i])) for j in td.idims] for i in td.idims]
        )

    def _applied_to_array(self, tensor: BigArray[U]) -> BigArray[U]:
        return SymmetrizedTensor(
            tensor,
            self._rows,
            self._row_axis,
            self._cols,
            self._col_axis,
        )

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        if axis in {self._row_axis, self._col_axis}:
            return TakeArray(self, labels, axis)
        return self._applied_to_array(self._tensor.take(labels, axis))

    def sum(self, axis: str) -> BigArray[T_co]:
        if axis in {self._row_axis, self._col_axis}:
            return SummedArray(self, axis)
        return self._applied_to_array(self._tensor.sum(axis))


class TraceOfSquaredTensor(BigArray[T_co]):
    """Trace of T^* T, where * is the (Euclidean) Hermitian transpose"""

    def __init__(
        self,
        tensor: BigArray[T_co],
        rows: Sequence[object],
        row_axis: str,
        cols: Sequence[object],
        col_axis: str,
    ):
        self._tensor = tensor
        self._rows = rows
        self._row_axis = row_axis
        self._cols = cols
        self._col_axis = col_axis

    def _index(self) -> IndexNd:
        return self._tensor.index.drop(self._col_axis).drop(self._row_axis)

    def _applied_to_array(self, tensor: BigArray[U]) -> BigArray[U]:
        return TraceOfSquaredTensor(
            tensor,
            self._rows,
            self._row_axis,
            self._cols,
            self._col_axis,
        )

    def array(self) -> NDArray[T_co]:
        td = TensorToDict(
            self._tensor,
            self._rows,
            self._row_axis,
            self._cols,
            self._col_axis,
        )
        a = td.dict()
        # TYPE SAFETY: this isn't safe as sum() returns 0 when fed an empty
        # collection
        return sum(np.abs(a[i, j]) ** 2 for i in td.idims for j in td.idims)  # type: ignore

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        if axis in {self._row_axis, self._col_axis}:
            return TakeArray(self, labels, axis)
        return self._applied_to_array(self._tensor.take(labels, axis))

    def sum(self, axis: str) -> BigArray[T_co]:
        if axis in {self._row_axis, self._col_axis}:
            return SummedArray(self, axis)
        return self._applied_to_array(self._tensor.sum(axis))
