"""
:mod:`pymusic.math.slicing`: slicing operations
===============================================

This module defines convenient functions to take slices of numpy arrays.
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    SliceElement = slice | int | None
    NSlice = tuple[SliceElement, ...]


def slice_axis(
    ndim: int, axis: int, on_axis: SliceElement, not_on_axis: SliceElement
) -> NSlice:
    """Assemble a tuple for numpy fancy indexing.
    The resulting tuple has the value `on_axis` on the slice's desired `axis`,
    and `not_on_axis` along all other axes.

    :param ndim: number of dimensions (axes) of resulting slice
    :param axis: axis to single out
    :param on_axis: what to place in the slice tuple in the position of `axis`
    :param not_on_axis: what to place in the slice tuple everywhere else
    :return: slicing tuple
    """
    assert 0 <= axis < ndim
    return axis * (not_on_axis,) + (on_axis,) + (ndim - axis - 1) * (not_on_axis,)


def slice_bcast_1d(ndim: int, axis: int) -> NSlice:
    """Assemble a tuple to align a 1D array along the desired `axis`, broadcasting along all other axes.

    :param ndim: number of dimensions (axes) of resulting slice
    :param axis: axis to align along
    :return: slicing tuple
    """
    return slice_axis(ndim, axis, slice(None), None)


def slice_take(ndim: int, axis: int, i: SliceElement) -> NSlice:
    """Assemble a tuple to slice an array at index `i` along the desired `axis`.

    This acts similarly to :func:`numpy.take`, but allows placing a slice on the left hand side of assignments.

    :param ndim: number of dimensions (axes) of resulting slice
    :param axis: axis to slice along
    :param i: index to take along `axis`
    :return: slicing tuple
    """
    return slice_axis(ndim, axis, i, slice(None))
