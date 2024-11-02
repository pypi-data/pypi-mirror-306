from __future__ import annotations

import typing
from abc import ABC, abstractmethod

import numpy as np

if typing.TYPE_CHECKING:
    from numpy.typing import ArrayLike


class NonUniformGridError(ValueError):
    pass


def find_uniform_delta(arr: np.ndarray, rtol: float = 1e-7) -> float:
    """Returns uniform delta between consecutive elements of array,
    raises `NonUniformGridError` if delta is not uniform within specified tolerance.

    :param rtol: relative tolerance between grid deltas
    :return: uniform delta between consecutive elements of array
    """
    delta = (arr[-1] - arr[0]) / (len(arr) - 1)
    if not np.allclose(np.diff(arr), delta, rtol=rtol, atol=0.0):
        raise NonUniformGridError
    return delta


class Grid1D(ABC):
    """Base class for one-dimensional grids"""

    def equals(self, other: Grid1D) -> bool:
        """
        :param other: other grid to test for equality, `__eq__` is implemented
        from this method, assuming non equality for objects of other types.
        """
        return bool(
            self.num_faces() != other.num_faces()
            and np.all(self.face_points() == other.face_points())
            and np.all(self.cell_points() == other.cell_points())
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid1D):
            return False
        return self.equals(other)

    @abstractmethod
    def bounds(self) -> tuple[float, float]:
        """:return: bounds (xmin, xmax) of the grid"""
        pass

    @abstractmethod
    def num_cells(self) -> int:
        """:return: number of cells"""
        pass

    @abstractmethod
    def num_faces(self) -> int:
        """:return: number of faces"""
        pass

    @abstractmethod
    def span(self) -> float:
        """:return: span (width) of the grid"""
        pass

    @abstractmethod
    def face_points(self) -> np.ndarray:
        """:return: array of face point locations"""
        pass

    def cell_centers(self) -> np.ndarray:
        """:return: array of geometrical cell center locations"""
        faces = self.face_points()
        lft_faces, rgt_faces = faces[:-1], faces[1:]
        return 0.5 * (lft_faces + rgt_faces)

    @abstractmethod
    def cell_points(self) -> np.ndarray:
        """:return: array of cell point locations"""
        pass

    def cell_widths(self) -> np.ndarray:
        """:return: array of cell widths"""
        return np.diff(self.face_points())

    def is_cell_centered(self) -> bool:
        return np.allclose(self.cell_points(), self.cell_centers())


class UniformGrid1D(Grid1D):
    """A one-dimensional grid with regular spacing (equal-width cells)"""

    def __init__(
        self, xmin: float, xmax: float, num_cells: int, cell_points_loc: float
    ):
        """
        :param xmin: lower bound of grid (left wall location of leftmost cell)
        :param xmax: upper bound of grid (right wall location of rightmost cell)
        :param num_cells: number of cells
        :param cell_points_loc: centering of cell points within cells;
           values of 0.0, 0.5 and 1.0 correspond to
           left-staggered, centered, and right-staggered grids, respectively
        """
        assert num_cells > 0
        assert 0.0 <= cell_points_loc <= 1.0
        assert xmax >= xmin
        self._xmin = xmin
        self._xmax = xmax
        self._ncells = num_cells
        self._cell_points_loc = cell_points_loc

    def equals(self, other: Grid1D) -> bool:
        if isinstance(other, UniformGrid1D):
            return (
                np.allclose(self.bounds(), other.bounds(), rtol=1e-13, atol=1e-13)
                and self._ncells == other._ncells
                and self._cell_points_loc == other._cell_points_loc
            )
        return super().equals(other)

    def bounds(self) -> tuple[float, float]:
        return (self._xmin, self._xmax)

    def num_cells(self) -> int:
        return self._ncells

    def num_faces(self) -> int:
        return self.num_cells() + 1

    def span(self) -> float:
        return np.abs(self._xmax - self._xmin)

    def center(self) -> float:
        return 0.5 * (self._xmin + self._xmax)

    def spacing(self) -> float:
        """:return: spacing (cell width) of the grid"""
        return self.span() / self.num_cells()

    def face_points(self) -> np.ndarray:
        return np.linspace(self._xmin, self._xmax, self.num_faces(), endpoint=True)

    def cell_points(self) -> np.ndarray:
        faces = self.face_points()
        lft_faces, rgt_faces = faces[:-1], faces[1:]
        return (
            1.0 - self._cell_points_loc
        ) * lft_faces + self._cell_points_loc * rgt_faces

    def is_cell_centered(self) -> bool:
        return self._cell_points_loc == 0.5

    @staticmethod
    def from_cell_points(
        cell_points: ArrayLike, cell_points_loc: float
    ) -> UniformGrid1D:
        """
        :return: new regular grid constructed from given cell points
        :param cell_points: locations of cell points
        :param cell_points_loc: centering of cell points within cells, see :meth:`__init__`
        """
        assert 0.0 <= cell_points_loc <= 1.0
        cell_points_arr = np.sort(cell_points)
        spacing = find_uniform_delta(cell_points_arr)
        xmin = cell_points_arr[0] - spacing * cell_points_loc
        xmax = cell_points_arr[-1] + spacing * (1.0 - cell_points_loc)
        return UniformGrid1D(
            xmin, xmax, len(cell_points_arr), cell_points_loc=cell_points_loc
        )

    @staticmethod
    def from_face_points(
        face_points: ArrayLike, cell_points_loc: float
    ) -> UniformGrid1D:
        """
        :return: new regular grid constructed from given face points
        :param cell_points: locations of cell points
        :param cell_points_loc: centering of cell points within cells, see :meth:`__init__`
        """
        assert 0.0 <= cell_points_loc <= 1.0
        face_points_arr = np.sort(face_points)
        _ = find_uniform_delta(face_points_arr)  # check for uniform spacing
        return UniformGrid1D(
            face_points_arr[0],
            face_points_arr[-1],
            face_points_arr.size - 1,
            cell_points_loc,
        )


class ArbitraryGrid1D(Grid1D):
    def __init__(self, points: np.ndarray):
        self._points = points

    def equals(self, other: Grid1D) -> bool:
        if self.num_faces() != other.num_faces():
            return False
        if isinstance(other, ArbitraryGrid1D):
            return bool(np.all(self.face_points() == other.face_points()))
        return super().equals(other)

    def bounds(self) -> tuple[float, float]:
        return (np.min(self._points), np.max(self._points))

    def num_cells(self) -> int:
        return self.num_faces() - 1

    def num_faces(self) -> int:
        return len(self._points)

    def span(self) -> float:
        a, b = self.bounds()
        return b - a

    def face_points(self) -> np.ndarray:
        return self._points

    def cell_points(self) -> np.ndarray:
        return self.cell_centers()
