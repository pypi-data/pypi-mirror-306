from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, TypeAlias

import matplotlib.axes as mpla
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Arc

from pymusic.plotting import Plot

from .dumps import ParticleDump
from .transmat import TransilientMatrix

Color: TypeAlias = float | np.float64 | str


@dataclass(frozen=True)
class Spherical2DParticlesPlot(Plot):
    """Plot in (X,Z) space of particles from a 2D spherical simulation dump"""

    dump: ParticleDump
    color: Callable[[pd.DataFrame], Color | Sequence[Color]] = lambda df: [
        0.0 for _ in range(len(df))
    ]
    scale: Callable[[pd.DataFrame], float | Sequence[float]] = lambda df: [
        1.0 for _ in range(len(df))
    ]
    cmap: str = "jet"

    def draw_on(self, ax: mpla.Axes) -> None:
        df = self.dump.dataframe()
        r, theta = df["x1"], df["x2"]

        x = r * np.sin(theta)
        y = r * np.cos(theta)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")

        ax.scatter(
            x,
            y,
            c=self.color(df),  # type: ignore
            s=self.scale(df),
            linewidths=0.0,
            cmap=self.cmap,
        )


@dataclass(frozen=True)
class Spherical2DDomainBounds(Plot):
    """Plot of the bounds in (X,Z) space (outline) of 2D spherical simulation domain"""

    r_bounds: tuple[float, float]
    theta_bounds: tuple[float, float]
    expand_margin: float = 0.1
    color: str = "k"
    linewidth: float = 1.0

    def draw_on(self, ax: mpla.Axes) -> None:
        rmin, rmax = self.r_bounds

        xmin = rmin * np.min(np.sin(self.theta_bounds))
        xmax = rmax

        ymin = rmax * np.cos(self.theta_bounds[1])
        ymax = rmax * np.cos(self.theta_bounds[0])

        e = self.expand_margin * rmax
        ax.set_aspect("equal")
        ax.set_xlim(xmin - e, xmax + e)
        ax.set_ylim(ymin - e, ymax + e)

        # Draw contour of domain
        for r in self.r_bounds:
            ax.add_artist(
                Arc(
                    xy=(0.0, 0.0),
                    width=2.0 * r,
                    height=2.0 * r,
                    angle=0,
                    theta1=np.rad2deg(np.pi / 2 - self.theta_bounds[1]),
                    theta2=np.rad2deg(np.pi / 2 - self.theta_bounds[0]),
                    color=self.color,
                    lw=self.linewidth,
                )
            )
        for th in self.theta_bounds:
            ax.add_artist(
                Line2D(
                    [rmin * np.sin(th), rmax * np.sin(th)],
                    [rmin * np.cos(th), rmax * np.cos(th)],
                    color=self.color,
                    lw=self.linewidth,
                )
            )


@dataclass(frozen=True)
class TransilientMatrixPlot(Plot):
    """Basic plot of transilient matrix counts"""

    matrix: TransilientMatrix
    cmap: str = "magma"

    def draw_on(self, ax: mpla.Axes) -> None:
        mat = np.log10(self.matrix.counts_matrix() + 1e-30)
        bins = self.matrix.bin_edges()
        ax.pcolormesh(
            bins,
            bins,
            mat.T,
            vmin=0.0,
            vmax=np.quantile(mat, 0.997),
            rasterized=True,
            cmap=self.cmap,
        )


def safe_log10(x: np.ndarray) -> np.ndarray:
    return np.log10(np.maximum(x, 1e-30))


@dataclass(frozen=True)
class PropagatorMatrixPlot(Plot):
    """Plot of a transilient propagator matrix"""

    matrix: TransilientMatrix
    cmap: str = "RdPu"

    def draw_on(self, ax: mpla.Axes) -> None:
        prob = self.matrix.propagator_matrix().T  # Transpose to get (source, dest) axes
        mat = safe_log10(prob)
        bins = self.matrix.bin_edges()
        ax.pcolormesh(
            bins,
            bins,
            mat.T,
            vmin=-4.0,
            vmax=0.0,
            rasterized=True,
            cmap=self.cmap,
        )


@dataclass(frozen=True)
class MixingIndexMatrixPlot:
    """
    Plot of log10(Prob(r_f|r_i) / Prob(r_f)), which is 0 iff knowing r_i provides
    no additional information on r_f (i.e., radii r_i and r_f are fully mixed).
    """

    matrix: TransilientMatrix
    cmap: str = "PuOr"

    def r_range(self) -> tuple[float, float]:
        return self.matrix.bin_span()

    def draw_on(self, ax: mpla.Axes) -> None:
        joint = self.matrix.joint_prob()  # Prob(end=i, start=j)
        prob = self.matrix.propagator_matrix()  # Prob(end=i|start=j)
        p_end_i = joint.sum(axis=1)  # Prob(end=i)
        mat = (
            safe_log10(prob) - safe_log10(p_end_i[:, None])
        ).T  # Transpose to get 'start' axis first
        bins = self.matrix.bin_edges()
        ax.pcolormesh(
            bins,
            bins,
            mat.T,
            vmin=-1.0,
            vmax=1.0,
            rasterized=True,
            cmap=self.cmap,
        )


@dataclass(frozen=True, eq=False)
class TransmatRadiusDecoration(Plot):
    """Plot layer marking a given radius on a transilient matrix plot"""

    r: float
    style_kwargs = dict(color="k", lw=0.5, ls="--")

    def draw_on(self, ax: mpla.Axes) -> None:
        ax.axhline(self.r, **self.style_kwargs)  # type: ignore
        ax.axvline(self.r, **self.style_kwargs)  # type: ignore


@dataclass(frozen=True)
class TransmatAxesDecorations(Plot):
    """Plot layer adding transilient matrix plot decorations,
    also setting bounds and a title.
    """

    r_bounds: tuple[float, float]
    title: str = ""

    def draw_on(self, ax: mpla.Axes) -> None:
        ax.axis("square")
        ax.set_xlim(*self.r_bounds)
        ax.set_ylim(*self.r_bounds)
        ax.set_xlabel("initial $r$ [cm]")
        ax.set_ylabel("final $r$ [cm]")

        if self.title:
            ax.set_title(self.title)
