from __future__ import annotations

from lazympl.figure import Figure, MatrixOfPlotsFigure, SinglePlotFigure
from lazympl.plot import (
    FigureTeePlot,
    Plot,
    PlotIf,
    PlotIfElse,
    PlotOnSameAxes,
    WithAxisLabels,
    WithPlotTitle,
)

__all__ = [
    "Figure",
    "MatrixOfPlotsFigure",
    "SinglePlotFigure",
    "FigureTeePlot",
    "Plot",
    "PlotIf",
    "PlotIfElse",
    "PlotOnSameAxes",
    "WithAxisLabels",
    "WithPlotTitle",
    "latex_escape",
]


def latex_escape(s: str) -> str:
    return s.replace("_", r"\_")
