"""
:mod:`.index`: 1D and nD indexing with arbitrary labels
=======================================================

This module contains classes to handle index objects,
which allow indexing 1D and nD arrays with arbitrary labels
along named axes (dimensions), similar to e.g. :class:`pandas.Index` objects.

The following nomenclature is roughly followed for comments and parameters and variables names:

 * *index*: an index object
 * *ordindex*: and ordinal integer index, e.g. for indexing numpy arrays
 * *label*: a label for indexing entries, can be integer, float, string, ...
 * *name* or *axis*: the name of a given index object, or name of axis for multidimensional index objects
"""

from __future__ import annotations

import typing
from abc import ABC, abstractmethod

from .exceptions import AxisError, IncompatibleIndexesError

if typing.TYPE_CHECKING:
    from typing import Sequence

    import numpy as np


class Index1d(ABC):
    """Base class for 1d index objects"""

    @property
    @abstractmethod
    def name(self) -> str:
        """:return: name of the index"""
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        """:return: size (number of elements) of the index"""
        pass

    @property
    @abstractmethod
    def labels(self) -> tuple:
        """:return: labels"""
        pass

    @abstractmethod
    def ordinal_index(self, label: object) -> int:
        """:return: ordinal index of label in this current index
        :param label: a label
        """
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @property
    def ndim(self) -> int:
        """:return: number of dimensions (axes) of index, 1 for a `Index1d`"""
        return 1

    @abstractmethod
    def renamed(self, new_name: str) -> Index1d:
        """:return: new 1d index with the name changed
        :param new_name: new index name
        """
        pass

    @abstractmethod
    def take(self, labels: Sequence[object]) -> Index1d:
        pass

    @staticmethod
    def concatenate(indexes: Sequence[Index1d]) -> Index1d:
        """Concatenate multiple 1d indexes into one. All indexes must have the same name,
        and the resulting labels must all be unique.

        :return: new 1d index formed by concatenation of multiple indexes
        :param indexes: indexes to concatenate
        """
        idx0 = indexes[0]
        if any(idx.name != idx0.name for idx in indexes):
            raise ValueError("all indexes to concatenate must have the same name")
        return ItemsIndex1d(idx0.name, sum((idx.labels for idx in indexes), tuple()))


class ItemsIndex1d(Index1d):
    """A 1d index based on an sequence of label items"""

    def __init__(self, name: str, labels: Sequence | np.ndarray):
        """:param name: index name
        :param labels: labels to use for indexing
        """
        self._name = name
        self._labels = labels
        if len(self._labels) != len(set(self._labels)):
            raise ValueError("index labels must be unique")

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return len(self._labels)

    @property
    def labels(self) -> tuple:
        return tuple(self._labels)

    def ordinal_index(self, label: object) -> int:
        return self.labels.index(label)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Index1d):
            return False
        if self is other:
            return True
        else:
            return (self.name == other.name) and (self.labels == other.labels)

    def renamed(self, new_name: str) -> ItemsIndex1d:
        return ItemsIndex1d(new_name, self.labels)

    def take(self, labels: Sequence[object]) -> ItemsIndex1d:
        return ItemsIndex1d(self.name, [lbl for lbl in self.labels if lbl in labels])


class IndexNd:
    """A Cartesian product of :class:`Index1d` objects"""

    def __init__(self, indexes1d: Sequence[Index1d]):
        """:param indexes1d: 1d index objects, one along each axis"""
        self._indexes = indexes1d

        if any(idx.ndim != 1 for idx in indexes1d):
            raise ValueError("indexes must all be 1D")

        # Check for duplicate axis names
        axes = self.axes
        if len(set(axes)) != len(axes):
            raise ValueError("names of axes must be unique")

    @property
    def axes(self) -> tuple[str, ...]:
        """:return: names of axes"""
        return tuple(idx.name for idx in self._indexes)

    def iaxis(self, axis: str) -> int:
        """:return: ordinal index of axis label
        :param axis: axis name
        """
        return dict((ax, iax) for (iax, ax) in enumerate(self.axes))[axis]

    @property
    def indexes1d(self) -> tuple[Index1d, ...]:
        """:return: 1d indexes along all axes"""
        return tuple(self._indexes)

    def index1d(self, axis: str) -> Index1d:
        """:return: 1d index object along desired axis
        :param axis: name of axis
        """
        return self._indexes[self.iaxis(axis)]

    @property
    def ndim(self) -> int:
        """:return: number of dimensions (axes) of index"""
        return len(self._indexes)

    @property
    def shape(self) -> tuple[int, ...]:
        """:return: n-dimensional shape of index"""
        return tuple(idx.size for idx in self._indexes)

    def size_along_axis(self, axis: str) -> int:
        """:return: size along specified axis
        :param axis: axis name
        """
        return self.index1d(axis).size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IndexNd):
            return False
        return (self is other) or (self.indexes1d == other.indexes1d)

    def insert(self, iax: int, index1d: Index1d) -> IndexNd:
        """:return: index with new 1d index inserted as new axis
        :param iax: new iaxis location occupied by inserted 1d index
        :param index1d: 1d index to insert
        """
        idx_list = list(self.indexes1d)
        idx_list.insert(iax, index1d)
        return IndexNd(idx_list)

    def drop(self, axis: object) -> IndexNd:
        """:return: index with axis dropped
        :param axis: axis label to drop
        """
        return IndexNd(tuple(idx for idx in self.indexes1d if idx.name != axis))

    def replace(self, axis: str, idx1d: Index1d) -> IndexNd:
        """:return: index with 1d index along axis replaced
        :param axis: axis name to replace
        :param idx1d: new index to use for this axis
        """
        iax = self.iaxis(axis)
        return self.drop(axis).insert(iax, idx1d)

    def take(self, labels: Sequence, axis: str) -> IndexNd:
        """:return: index keeping only the specified labels over the given axis
        :param labels: sequence of labels to keep along axis
        :param axis: axis to take along
        """
        return self.replace(axis, self.index1d(axis).take(labels))

    def squeeze(self, axis: str | None = None) -> IndexNd:
        """:return: index with size one dimensions removed, following :func:`numpy.squeeze` semantics
        :param axis: axis name to squeeze along
        """
        if axis is None:
            return IndexNd(tuple(idx for idx in self.indexes1d if idx.size != 1))

        sz = self.size_along_axis(axis)
        if sz != 1:
            raise AxisError(f"size along specified axis='{axis}' must be 1, have {sz}")

        return self.drop(axis)

    @staticmethod
    def concatenate(indexes: Sequence[IndexNd], axis: str) -> IndexNd:
        """:return: index formed by concatenating indexes along given axis label
        :param indexes: sequence of indexes to concatenate
        :param axis: axis name to concatenate along
        """
        # noinspection PyUnreachableCode
        if __debug__:
            # Check that all indexes are identical in directions other than axis
            indexes_wo_axis = [idx.drop(axis) for idx in indexes]
            if any(idx != indexes_wo_axis[0] for idx in indexes_wo_axis):
                raise IncompatibleIndexesError(
                    "indexes must be identical along all axes except concatenation axis"
                )

        new_idx1d_axis = Index1d.concatenate([idx.index1d(axis) for idx in indexes])
        return IndexNd(
            [
                (indexes[0].index1d(ax) if ax != axis else new_idx1d_axis)
                for ax in indexes[0].axes
            ]
        )
