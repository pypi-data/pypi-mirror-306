from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property

import numpy as np

if typing.TYPE_CHECKING:
    from typing import Callable, Iterator, TypeVar

    from numpy.typing import NDArray

    U = TypeVar("U", bound=np.number)


def midpoints(arr: np.ndarray) -> np.ndarray:
    return 0.5 * (arr[1:] + arr[:-1])


@dataclass(frozen=True)
class LineSection:
    """The line (row) of an ndarray with given `array_shape`, along a given `axis`,
    cutting through index `through_index`.
    """

    array_shape: tuple[int, ...]
    axis: int
    through_index: tuple[int, ...]

    @cached_property
    def line_shape(
        self,
    ) -> tuple[int,]:
        "Shape of the line section array"
        return (self.array_shape[self.axis],)

    @cached_property
    def slice(self) -> tuple[int | slice, ...]:
        "Slice to extract this line from an ndarray"
        return tuple(
            self.through_index[ax] if ax != self.axis else slice(None)
            for ax in range(len(self.array_shape))
        )

    def read(self, source: NDArray[U]) -> NDArray[U]:
        "Read the line from the given `source` ndarray and return it"
        assert source.shape == self.array_shape
        line = source[self.slice]
        assert line.shape == self.line_shape
        return line

    def write(self, line: NDArray[U], dest: NDArray[U]) -> None:
        "Write the line values in `line` into the given `dest` ndarray"
        assert dest.shape == self.array_shape
        assert line.shape == self.line_shape
        dest[self.slice] = line


def iter_lines(shape: tuple[int, ...], axis: int) -> Iterator[LineSection]:
    axes = range(len(shape))

    if axis not in axes:
        raise ValueError("invalid axis")

    iter_shape = tuple(shape[ax] if ax != axis else 1 for ax in axes)
    for through_index in np.ndindex(*iter_shape):
        yield LineSection(shape, axis, through_index)


@dataclass(frozen=True)
class PlaneSection:
    """The plane of an ndarray with given `array_shape`, with axes `(ax1, ax2)`,
    cutting through index `through_index`.
    """

    array_shape: tuple[int, ...]
    ax1: int
    ax2: int
    through_index: tuple[int, ...]

    def _swap_axes_if_needed(self, plane: NDArray[U]) -> NDArray[U]:
        if self.ax1 < self.ax2:
            return plane
        else:
            return plane.swapaxes(0, 1)

    @cached_property
    def plane_shape(self) -> tuple[int, int]:
        "Shape of the plane section array"
        return (self.array_shape[self.ax1], self.array_shape[self.ax2])

    @cached_property
    def slice(self) -> tuple[int | slice, ...]:
        """Slice to extract this plane from an ndarray. Note that this slice will
        *not* put the axes `ax1`, `ax2` in their expected order if `ax1 > ax2`.
        """

        return tuple(
            self.through_index[ax] if ax not in {self.ax1, self.ax2} else slice(None)
            for ax in range(len(self.array_shape))
        )

    def read(self, source: NDArray[U]) -> NDArray[U]:
        """Read the plane from the given `source` ndarray and return it.

        The resulting array always has axes `ax1`, `ax2` along its first and second
        dimension respectively, regardless of whether `ax1 < ax2`.
        """

        assert source.shape == self.array_shape
        plane = self._swap_axes_if_needed(source[self.slice])
        assert plane.shape == self.plane_shape
        return plane

    def write(self, plane: NDArray[U], dest: NDArray[U]) -> None:
        """Write the plane values from `plane` into the `dest` ndarray.

        The expected `plane` array always uses axes `ax1`, `ax2` along its first and
        second dimension respectively, regardless of whether `ax1 < ax2`.
        """
        assert dest.shape == self.array_shape
        assert plane.shape == self.plane_shape
        dest[self.slice] = self._swap_axes_if_needed(plane)


def iter_planes(shape: tuple[int, ...], ax1: int, ax2: int) -> Iterator[PlaneSection]:
    axes = range(len(shape))

    if ax1 == ax2:
        raise ValueError("axes ax1 and ax2 of plane must be different")

    if ax1 not in axes:
        raise ValueError("invalid ax1")

    if ax2 not in axes:
        raise ValueError("invalid ax2")

    iter_shape = tuple(shape[ax] if ax not in {ax1, ax2} else 1 for ax in axes)
    for through_index in np.ndindex(*iter_shape):
        yield PlaneSection(shape, ax1, ax2, through_index)


def apply_along_planes(
    func: Callable[[NDArray[U]], NDArray[U]],
    arr: NDArray[U],
    ax1: int,
    ax2: int,
    out: NDArray[U] | None = None,
) -> NDArray[U]:
    """Apply `func` to each plane of `arr` of axes `(ax1, ax2)` and return the result.

    `func` must return an array of the same dtype and shape as its input.
    The arrays passed to `func` will be 2-dimensional, their first axis correspond to `ax1`,
    their second axis to `ax2` (even when `ax1 > ax2`).

    `out` may safely refer to the same object as the input `arr`, in which case `arr` is
    overwritten in place.
    """

    if out is None:
        out = np.empty_like(arr)
    else:
        assert arr.shape == out.shape

    for plane in iter_planes(arr.shape, ax1, ax2):
        plane.write(plane=func(plane.read(source=arr)), dest=out)

    return out
