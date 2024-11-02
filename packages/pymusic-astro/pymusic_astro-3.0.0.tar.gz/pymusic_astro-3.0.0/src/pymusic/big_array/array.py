"""
:mod:`.array`: base array classes for :class:`BigArray` objects
===============================================================
"""

from __future__ import annotations

import functools
import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Generic, TypeVar

import numpy as np

from .exceptions import AxisError, BigArrayShapeError, IncompatibleIndexesError
from .index import IndexNd, ItemsIndex1d

if TYPE_CHECKING:
    from typing import Callable, Iterator, Sequence, TypeAlias

    from numpy.typing import NDArray

    from .index import Index1d


T_co = TypeVar("T_co", bound=np.number, covariant=True)
U = TypeVar("U", bound=np.number)
FloatOrCplx: TypeAlias = np.floating | np.complexfloating

FC = TypeVar("FC", bound=FloatOrCplx)
FC_co = TypeVar("FC_co", bound=FloatOrCplx, covariant=True)


class BigArray(ABC, Generic[T_co]):
    """Abstract base class for all big array objects

    The following methods are abstract and must be implemented by all subclasses:

     * :meth:`_index`: return the index for this array
     * :meth:`array`: assemble the whole data in memory as a :class:`numpy.ndarray` object
     * :meth:`take`: slice array by selecting labels along an axis
     * :meth:`sum`: sum array along specified axis

    The following inspection methods are available:

     * :meth:`index`: cached version of :meth:`_index`
     * :meth:`index1d`: get 1d index along an axis
     * :meth:`axes`: report names of axes
     * :meth:`ndim`: report number of dimensions of the array
     * :meth:`iaxis`: report ordinal index of given axis label
     * :meth:`shape`: report shape of the array
     * :meth:`size`: report total number of elements in array
     * :meth:`size_along_axis`: report total number of elements along given axis
     * :meth:`labels_along_axis`: give all labels (axis indices) along given axis

    The following comparison methods are available:

     * :meth:`equals`: tests whether the contents (index and data) of two arrays are identical

    The following convenience methods are provided by this base class
    to construct new array objects relying on the behavior implemented above,
    as well as on other derived collaborator classes:

     * :meth:`apply`: apply a function point-wise on the array, preserving shape
     * :meth:`xs`: perform a cross-section along an axis
     * :meth:`take_filter`: slice array along an axis by applying a filter function on the axis labels
     * :meth:`take_slice`: slice array along an axis by applying a slice to the axis labels
     * :meth:`squeeze`: drop a size-1 axis from the array
     * :meth:`collapse`: collapse the array along given axis by applying a vector → scalar function
     * :meth:`abs2`: return array of squared absolute values
     * :meth:`sum_abs2`: compute the sum of the squared absolute value along an axis
     * :meth:`rms`: compute root mean square (RMS) along an axis
     * :meth:`scaled`: scale the array by a constant factor
     * :meth:`sqrt`: return square root of array

     The following methods allow control over the scheduling of computation:

     * :meth:`slabbed`: return the same array, but slabbed into slabs of specified axis and size
    """

    @abstractmethod
    def _index(self) -> IndexNd:
        """:return: index for this array"""
        pass

    @cached_property
    def index(self) -> IndexNd:
        return self._index()

    def index1d(self, axis: str) -> Index1d:
        """:return: 1d index along desired axis for this array
        :param axis: name of axis
        """
        return self.index.index1d(axis)

    @property
    def axes(self) -> tuple[str, ...]:
        """:return: names of axes"""
        return self.index.axes

    def iaxis(self, axis: str) -> int:
        """:return: ordinal index of specified axis, between 0 and :meth:`ndim`-1
        :param axis: axis name
        """
        return self.index.iaxis(axis)

    @property
    def shape(self) -> tuple[int, ...]:
        """:return: shape of data array"""
        return self.index.shape

    @property
    def size(self) -> int:
        """:return: total number of elements in array"""
        return int(np.prod(self.shape))

    def size_along_axis(self, axis: str) -> int:
        """:return: size along specified axis
        :param axis: axis name
        """
        return self.index.size_along_axis(axis)

    def labels_along_axis(self, axis: str) -> tuple[object, ...]:
        """:return: labels (indices) along specified axis
        :param axis: axis name
        """
        return self.index1d(axis).labels

    @property
    def ndim(self) -> int:
        """:return: number of dimensions of array"""
        return self.index.ndim

    @abstractmethod
    def array(self) -> NDArray[T_co]:
        """Construct the actual NumPy data array for this object

        :return: the full array
        """
        pass

    @abstractmethod
    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        """Construct an array object obtained by taking the selected labels along the desired axis.

        :return: the array object with only the desired labels along the axis
        :param labels: the index labels
        :param axis: the axis name to take along
        """
        pass

    def take_filter(
        self, filter_func: Callable[[object], bool], axis: str
    ) -> BigArray[T_co]:
        """Take along axis, keeping only labels for which `filter_func` evaluates to True.

        :param func filter_func: filter function
        :param axis: axis name to take along
        :return: array with specified labels filtered
        """
        labels = self.index1d(axis).labels
        labels_to_keep = [label for label in labels if filter_func(label)]
        return self.take(labels_to_keep, axis)

    def take_slice(self, slice_: slice, axis: str) -> BigArray[T_co]:
        """Take along axis, applying the given slice to the axis labels"""
        labels = self.labels_along_axis(axis)
        return self.take(labels[slice_], axis)

    def xs(self, label: object, axis: str) -> BigArray[T_co]:
        """Return a cross-section of the array at the given label along the specified axis.
        The default implementation relies on :meth:`take`.

        :return: an array object representing the cross-section
        :param label: the index label to cut at
        :param axis: the axis used for the cross-section
        """
        return self.take([label], axis).squeeze(axis)

    def squeeze(self, axis: str) -> BigArray[T_co]:
        """Remove a size-1 dimension from the array, see :class:`SqueezedArray`."""
        return SqueezedArray(self, axis)

    @abstractmethod
    def sum(self, axis: str) -> BigArray[T_co]:
        """Sum array along given axis

        :return: summed array
        :param axis: axis to reduce along
        """
        pass

    def weighted_sum(
        self, axes: Sequence[str], weights: NDArray[T_co]
    ) -> BigArray[T_co]:
        """Weighted sum of array along given axes. See :class:`WeightedSumArray`.

        :return: array of weighted sums
        :param axes: axis to reduce along
        :param weights: array of weights
        """
        return WeightedSumArray(self, axes, weights)

    def apply(self, func: Callable[[NDArray[T_co]], NDArray[U]]) -> BigArray[U]:
        """Apply a elemental function to every element of the array

        :return: resulting array
        :param func: function to apply
        """
        return ApplyArray(self, func)

    def collapse(self, func: Callable[[NDArray[T_co]], U], axis: str) -> BigArray[U]:
        """Collapse the array along an axis by applying a vector → scalar function along axis.
        See :class:`CollapsedArray`.

        :param func: function to apply
        :param axis: axis to collapse along
        :return: collapsed array
        """
        return CollapsedArray(self, func, axis)

    def abs2(self) -> BigArray[np.float64]:
        """
        :return: squared absolute value of the array
        """
        return self.apply(lambda arr: (arr.real**2 + arr.imag**2).astype(np.float64))

    def sum_abs2(self, axis: str) -> BigArray[np.float64]:
        """Sum square absolute values (moduli) of array elements along given axis

        :return: array of summed squared absolute values
        :param axis: axis to reduce along
        """
        return self.abs2().sum(axis)

    def rms(self, axis: str) -> BigArray[np.float64]:
        """Take RMS of array along axis

        :param axis: axis to sum along
        :return: array of `sqrt(sum(abs2(.)) / size_along(axis))`
        """
        return self.abs2().mean(axis).sqrt()

    def mean(self, axis: str) -> BigArray[T_co]:
        """Take arithmetic mean of array along axis

        :param axis: axis to average along
        :return: array of `sum(.) / size_along(axis)`
        """
        n = self.size_along_axis(axis)
        assert n > 0
        return self.sum(axis).scaled(1.0 / n)

    def scaled(self, factor: float) -> BigArray[T_co]:
        """
        :param factor: factor to multiply the array element-wise with
        :return: scaled array
        """
        # TYPE SAFETY: this is not always a valid operation
        return self.apply(lambda arr: factor * arr)  # type: ignore

    def sqrt(self) -> BigArray[T_co]:
        """
        :return: square root of array, as `np.float64`
        """
        return self.apply(np.sqrt)

    def slabbed(self, along_axis: str, slab_size: int) -> BigArray[T_co]:
        """Returns a new array representing the current array as a concatenation of slabs,
        along a chosen axis and of a given size.
        This is useful to force processing of array in a slab-wise fashion for some operations.
        See :class:`ArrayAsSlabs`.

        :param along_axis: axis to create slabs along
        :param slab_size: size of the slabs, in number of elements
        :return: new array representing the same source array as a concatenation of slabs
        """
        return ArrayAsSlabs(self, along_axis, slab_size).slabbed_and_recombined()

    def __str__(self) -> str:
        return "{}(axes={}, shape={})".format(
            self.__class__.__name__, self.axes, self.shape
        )

    def equals(self, other: BigArray[U]) -> bool:
        """Tests whether the array contents are identical to the contents of another array,
        that is, if both arrays have exactly the same index and the same data.
        Note that this will evaluate :meth:`array` on both arrays `self` and `other`.

        :param other: array to test equality against
        """
        return (self.index == other.index) and bool(
            np.all(self.array() == other.array())
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BigArray):
            return False
        return self.equals(other)


class TakeArray(BigArray[T_co]):
    """Form an array by extracting labels along a given axis.

    This implementation is naive: :meth:`array` first forms the full parent
    array, then uses :func:`numpy.take` to filter the labels along the
    requested axis.
    """

    def __init__(self, array: BigArray[T_co], labels: Sequence[object], axis: str):
        self._array = array
        self._labels = labels
        self._axis = axis

    def _index(self) -> IndexNd:
        idx = self._array.index
        return idx.take(self._labels, self._axis)

    def array(self) -> NDArray[T_co]:
        idx1d = self._array.index1d(self._axis)
        i_labels = [idx1d.ordinal_index(lbl) for lbl in self._labels]
        # Construct full array, and filter with np.take()
        arr = self._array.array()
        return np.take(arr, i_labels, axis=self.iaxis(self._axis))

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)


class NumpyArray(BigArray[T_co]):
    """An array providing data from a :class:`numpy.ndarray`"""

    def __init__(self, index_nd: IndexNd, np_array: NDArray[T_co]):
        self._index_nd = index_nd
        self._np_array = np_array
        if self._index_nd.shape != self._np_array.shape:
            raise BigArrayShapeError("index and ndarray shape mismatch")

    def _index(self) -> IndexNd:
        return self._index_nd

    def array(self) -> NDArray[T_co]:
        return self._np_array

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)


class StackedArray(BigArray[T_co]):
    """An array formed by joining a sequence of arrays along a new axis"""

    def __init__(
        self, arrays: Sequence[BigArray[T_co]], new_index1d: Index1d, iaxis: int
    ):
        """:param arrays: sequence of arrays to join
        :param new_index1d: index to use along new axis, must have same length as `arrays`
        :param iaxis: ordinal position to insert new axis at
        """
        self._arrays = arrays
        self._new_idx = new_index1d
        self._iaxis = iaxis

    def _is_stacked_along(self, axis: str) -> bool:
        return axis == self._new_idx.name

    def _index(self) -> IndexNd:
        index = self._arrays[0].index
        if __debug__ and any(a.index != index for a in self._arrays):
            raise IncompatibleIndexesError(
                "all arrays in StackedArray must have identical indexes"
            )
        # Just prepend the new index to the parent one
        return index.insert(self._iaxis, self._new_idx)

    def array(self) -> NDArray[T_co]:
        return np.stack([arr.array() for arr in self._arrays], axis=self._iaxis)

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        if self._is_stacked_along(axis):
            # The new array is formed from stacking a subset of the original arrays
            i_take_arrs = [self._new_idx.ordinal_index(lbl) for lbl in labels]
            take_arrs = [self._arrays[i] for i in i_take_arrs]
            take_idx = self._new_idx.take(labels)
            return StackedArray(take_arrs, take_idx, self._iaxis)
        else:
            # We are taking along another axis, so just reassemble an array
            # by stacking arrays to which we have forwarded take()
            return StackedArray(
                [arr.take(labels, axis) for arr in self._arrays],
                self._new_idx,
                self._iaxis,
            )

    def sum(self, axis: str) -> BigArray[T_co]:
        if self._is_stacked_along(axis):
            return SummedSeqArray(self._arrays)
        else:
            # Careful because if iaxis(axis) < iaxis(self._axis),
            # then we need to shift the stacking index position by 1 to the left
            new_iaxis = (
                self._iaxis if self.iaxis(axis) > self._iaxis else self._iaxis - 1
            )
            return StackedArray(
                [arr.sum(axis) for arr in self._arrays], self._new_idx, new_iaxis
            )


class ConcatenatedArray(BigArray[T_co]):
    """An array formed from the concatenation of arrays along an existing axis"""

    def __init__(self, arrays: Sequence[BigArray[T_co]], axis: str):
        """:param arrays: sequence of arrays to concatenate
        :param axis: axis label to concatenate along
        """
        self._arrays = arrays
        self._axis = axis

    def _is_concatenated_along(self, axis: str) -> bool:
        return self._axis == axis

    def _index(self) -> IndexNd:
        return IndexNd.concatenate([a.index for a in self._arrays], axis=self._axis)

    def array(self) -> NDArray[T_co]:
        iaxis = self.iaxis(self._axis)
        return np.concatenate([arr.array() for arr in self._arrays], axis=iaxis)

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        if self._is_concatenated_along(axis):
            # Be a bit careful, and take labels only from sub-arrays
            # for which we won't produce an empty array
            def gen_taken_sub_arrays() -> Iterator[BigArray]:
                for arr in self._arrays:
                    avail_labels = arr.labels_along_axis(axis)
                    labels_in_arr = [x for x in labels if x in avail_labels]
                    if len(labels_in_arr) > 0:
                        yield arr.take(labels_in_arr, axis)

            # Concatenate all resulting non-empty arrays
            return ConcatenatedArray(list(gen_taken_sub_arrays()), self._axis)
        else:
            return ConcatenatedArray(
                [a.take(labels, axis) for a in self._arrays], self._axis
            )

    def sum(self, axis: str) -> BigArray[T_co]:
        summed_arrays = [
            a.sum(axis) for a in self._arrays if a.size_along_axis(axis) > 0
        ]
        if self._is_concatenated_along(axis):
            return SummedSeqArray(summed_arrays)
        else:
            return ConcatenatedArray(summed_arrays, self._axis)


class SqueezedArray(BigArray[T_co]):
    """An array with a size one dimension removed"""

    def __init__(self, array: BigArray[T_co], axis: str):
        """:param array: source array
        :param axis: axis name to remove
        """
        self._arr = array
        self._axis = axis

    def _index(self) -> IndexNd:
        return self._arr.index.squeeze(axis=self._axis)

    def array(self) -> NDArray[T_co]:
        return np.squeeze(self._arr.array(), axis=self._arr.iaxis(self._axis))

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        if axis not in self.axes:
            raise AxisError("invalid axis for take()")
        return SqueezedArray(self._arr.take(labels, axis), self._axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        if axis not in self.axes:
            raise AxisError("invalid axis for sum()")
        return SqueezedArray(self._arr.sum(axis), self._axis)


class RandomArray(BigArray[np.float64]):
    """An array of random numbers, sampled from :func:`numpy.random.uniform`"""

    def __init__(self, nd_index: IndexNd, name: str = "random_array", seed: int = 1):
        """
        :param nd_index: n-dimensional index for this array, determines dimension and shape
        :param name: name for this array, for debugging and testing
        :param seed: random seed to use for :class:`numpy.random.RandomState`
        """
        self._nd_index = nd_index
        self._name = name
        self._seed = seed

    def _index(self) -> IndexNd:
        return self._nd_index

    def array(self) -> NDArray[np.float64]:
        r_state = np.random.RandomState(seed=self._seed)
        return r_state.uniform(size=self.shape)

    def take(self, labels: Sequence[object], axis: str) -> BigArray[np.float64]:
        return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[np.float64]:
        return SummedArray(self, axis)


class SummedArray(BigArray[T_co]):
    """Sum array along a direction"""

    def __init__(self, array: BigArray[T_co], axis: str):
        """:param array: input array sum
        :param axis: axis to sum along
        """
        self._array = array
        self._axis = axis

    def _index(self) -> IndexNd:
        return self._array.index.drop(self._axis)

    def array(self) -> NDArray[T_co]:
        return np.sum(self._array.array(), axis=self._array.iaxis(self._axis))

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        assert axis in self.axes
        return SummedArray(self._array.take(labels, axis), self._axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        assert axis in self.axes
        return SummedArray(self, axis)


class WeightedSumArray(BigArray[T_co]):
    """Weighted sum along multiple axes"""

    def __init__(
        self, array: BigArray[T_co], axes: Sequence[str], weights: NDArray[T_co]
    ):
        """:param array: input array sum
        :param axes: axes to sum along
        :param weights: :mod:`numpy` array of weights with shape matching `axes`
        """
        self._array = array
        self._axes = axes
        self._weights = weights

    def _index(self) -> IndexNd:
        index = self._array.index
        for ax in self._axes:
            index = index.drop(ax)
        return index

    def array(self) -> NDArray[T_co]:
        np_array = self._array.array()
        i_axes = tuple(self._array.iaxis(ax) for ax in self._axes)

        # noinspection PyUnreachableCode
        if __debug__:
            # Check that broadcasting will work
            for iax_weights, (iax, ax) in enumerate(zip(i_axes, self._axes)):
                if np_array.shape[iax] != self._weights.shape[iax_weights]:
                    raise ValueError(
                        "dimension mismatch for array and weights along axis '{}'".format(
                            ax
                        )
                    )

        bcast_shape = tuple(
            (np_array.shape[i] if i in i_axes else 1) for i in range(np_array.ndim)
        )
        bcast_weights = np.reshape(self._weights, bcast_shape)
        return np.sum(
            np_array * bcast_weights, axis=i_axes
        )  # Numpy supports summing along multiple axes

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        assert axis in self.axes
        return WeightedSumArray(
            self._array.take(labels, axis), self._axes, self._weights
        )

    def sum(self, axis: str) -> BigArray[T_co]:
        assert axis in self.axes
        return SummedArray(self, axis)


class SummedSeqArray(BigArray[T_co]):
    """An array resulting from the sum of a sequence of identical arrays"""

    def __init__(self, arrays: Sequence[BigArray[T_co]]):
        """
        :param arrays: sequence of arrays to sum
        """
        self._arrays = arrays

    def _index(self) -> IndexNd:
        if __debug__ and any(
            arr.index != self._arrays[0].index for arr in self._arrays
        ):
            raise IncompatibleIndexesError(
                "all arrays in SummedSeqArray must have identical indexes"
            )
        return self._arrays[0].index

    def array(self) -> NDArray[T_co]:
        # Use iterator and functools.reduce to allocate memory sparingly
        def iter_np_arrays() -> Iterator[NDArray[T_co]]:
            for arr in self._arrays:
                yield arr.array()

        return functools.reduce(operator.add, iter_np_arrays())

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return SummedSeqArray([arr.take(labels, axis) for arr in self._arrays])

    def sum(self, axis: str) -> BigArray[T_co]:
        # The sum traverses the sequence
        return SummedSeqArray([arr.sum(axis) for arr in self._arrays])


class ApplyArray(BigArray[T_co]):
    """An array formed by applying a function element-wise to an existing array,
    preserving shape and indexes but potentially changing the data type.
    """

    def __init__(self, array: BigArray[U], func: Callable[[NDArray[U]], NDArray[T_co]]):
        """
        :param array: array to apply function to
        :param func: function to apply element-wise to array
        """
        self._array = array
        self._func = func

    def _index(self) -> IndexNd:
        return self._array.index

    def array(self) -> NDArray[T_co]:
        return self._func(self._array.array())

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return ApplyArray(self._array.take(labels, axis), self._func)

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)


class ArrayAsSlabs(Generic[T_co]):
    """Split and recombine an array in slabs along a direction"""

    def __init__(self, array: BigArray[T_co], axis: str, slab_size: int):
        """:param array: source array
        :param axis: axis to form slabs along
        :param slab_size: maximum size of each slab
        """
        self._array = array
        self._axis = axis
        if slab_size < 1:
            raise ValueError("slab size must be >= 1")
        self._slab_size = slab_size

    def iter_slabs(self) -> Iterator[BigArray[T_co]]:
        """
        :return: iterator on array slabs
        """
        index1d = self._array.index1d(self._axis)
        num_points = index1d.size
        labels = index1d.labels

        for i_beg in range(0, num_points, self._slab_size):
            i_end = min(i_beg + self._slab_size, num_points)
            # Yield the slab obtained by taking these labels along the slicing axis
            yield self._array.take(labels[i_beg:i_end], axis=self._axis)

    def slabbed_and_recombined(self) -> BigArray[T_co]:
        """
        :return: a recombined array, representing the original array
            but internally restructured as a concatenation of slabs
        """
        return ConcatenatedArray(list(self.iter_slabs()), self._axis)


class CollapsedArray(BigArray[T_co]):
    """Collapse array along an axis, by applying a vector → scalar function along the axis"""

    def __init__(
        self, array: BigArray[U], func: Callable[[NDArray[U]], T_co], axis: str
    ):
        """:param array: input array to collapse
        :param func: scalar-valued function of vector argument, to apply along selected axis
        :param axis: axis to collapse along
        """
        self._array = array
        self._func = func
        self._axis = axis

    def _index(self) -> IndexNd:
        return self._array.index.drop(self._axis)

    def array(self) -> NDArray[T_co]:
        # Provided self._func returns as scalar, this will automatically collapse the axis
        return np.apply_along_axis(
            self._func, self._array.iaxis(self._axis), self._array.array()
        )

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        assert axis in self.axes
        return CollapsedArray(self._array.take(labels, axis), self._func, self._axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        assert axis in self.axes
        return SummedArray(self, axis)


@dataclass
class RemappedIndexArray(BigArray[T_co]):
    """An array with index labels remapped, according to provided remapping
    functions. Remapping is specified as an {ax: remap} dictionary, where keys
    are the axis names, and values are functions applied to labels along the
    corresponding axis to obtain the new values. The new resulting labels must
    be unique.
    """

    source: BigArray[T_co]
    remap: dict[str, Callable]

    def _index(self) -> IndexNd:
        index = self.source.index
        for ax, ax_func in self.remap.items():
            old_labels = self.source.labels_along_axis(ax)
            new_labels = tuple(ax_func(x) for x in old_labels)
            index = index.replace(ax, ItemsIndex1d(ax, new_labels))

        return index

    def array(self) -> NDArray[T_co]:
        return self.source.array()

    def take(self, labels: Sequence[object], axis: str) -> BigArray[T_co]:
        return TakeArray(self, labels, axis)

    def sum(self, axis: str) -> BigArray[T_co]:
        return SummedArray(self, axis)
