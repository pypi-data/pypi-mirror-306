from __future__ import annotations

import typing
from dataclasses import dataclass, field

import numpy as np

from .figure import Plot

if typing.TYPE_CHECKING:
    from typing import Protocol

    import matplotlib as mpl

    from .. import big_array as pma

    # same as Callable[[np.array], tuple[float, float]], to circumvent
    # bug in mypy
    class ArrayToBoundsFunc(Protocol):
        def __call__(self, __arr: np.ndarray) -> tuple[float, float]: ...


@dataclass(frozen=True)
class BoundsFromMinMax:
    def __call__(self, values: np.ndarray) -> tuple[float, float]:
        return np.min(values), np.max(values)


@dataclass(frozen=True)
class BoundsFromQuantiles:
    qmin: float = 0.0
    qmax: float = 1.0

    def __call__(self, values: np.ndarray) -> tuple[float, float]:
        # TYPE SAFETY: shape of tuple is known, but type of element
        # assumes an array of floats
        return tuple(np.quantile(values, [self.qmin, self.qmax]))  # type: ignore


@dataclass(frozen=True)
class FixedBounds:
    vmin: float
    vmax: float

    def __call__(self, values: np.ndarray) -> tuple[float, float]:
        return (self.vmin, self.vmax)


@dataclass(frozen=True)
class NoBounds:
    def __call__(self, values: np.ndarray) -> tuple[float, float]:
        return (float("nan"), float("nan"))


@dataclass(frozen=True)
class ArrayImagePlot(Plot):
    array: pma.BigArray
    axes: tuple[str, str]
    cmap: mpl.colors.Colormap | None = None
    color_bounds: ArrayToBoundsFunc = BoundsFromMinMax()
    with_colorbar: bool = True
    pcolormesh_kwargs: dict = field(default_factory=dict)

    def draw_on(self, ax: mpl.axes.Axes) -> None:
        x = np.asarray(self.array.labels_along_axis(self.axes[0]), dtype=np.float64)
        y = np.asarray(self.array.labels_along_axis(self.axes[1]), dtype=np.float64)

        if self.array.ndim != 2:
            raise ValueError(
                "ArrayImagePlot: can only draw 2d arrays, "
                f"but passed array has {self.array.ndim} dimensions"
            )

        if set(self.array.axes) != set(self.axes):
            raise ValueError(
                "ArrayImagePlot: requested axes {self.axes} "
                f"do not match passed array axes {self.array.axes}"
            )

        data = self.array.array()
        assert self.array.axes == tuple(self.axes) or self.array.axes == tuple(
            reversed(self.axes)
        )
        if self.array.axes == tuple(reversed(self.axes)):
            data = data.T

        vmin, vmax = self.color_bounds(data)
        im = ax.pcolormesh(
            x,
            y,
            data.T,
            cmap=self.cmap,
            vmin=vmin,
            vmax=vmax,
            shading="gouraud",
            rasterized=True,
            **self.pcolormesh_kwargs,
        )

        ax.set_xlabel(self.axes[0])
        ax.set_ylabel(self.axes[1])

        if self.with_colorbar:
            assert ax.figure is not None
            ax.figure.colorbar(im, ax=ax)
