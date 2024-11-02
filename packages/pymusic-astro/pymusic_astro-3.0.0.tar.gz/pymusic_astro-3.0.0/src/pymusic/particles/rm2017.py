"""
Objects and functions for the study of IGW particle diffusion following the
methodology of Rogers & McElwaine 2017 (hereafter RM17).

See:

 - [RM17] Rogers, T.M., McElwaine, J.N., 2017. On the Chemical Mixing Induced by
    Internal Gravity Waves. The Astrophysical Journal Letters 848, L1.
    https://doi.org/10.3847/2041-8213/aa8d13
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Iterator, Sequence

import numpy as np
import pandas as pd
import tqdm
from numpy.typing import NDArray

import pymusic.particles as pmp

F = NDArray[np.float64]
N = NDArray[np.int32]
B = NDArray[np.bool_]


def w_cubic(u: F) -> F:
    """Cubic interpolation kernel on [-1, 1], with w(0)==1 and integral 1."""
    t = np.abs(u)
    nonzero = t < 1.0
    w = np.zeros_like(u)
    w[nonzero] = (lambda t: (1.0 + 2.0 * t) * (1.0 - t) * (1.0 - t))(t[nonzero])
    return w


@dataclass(frozen=True)
class RGrid:
    """A uniform radial grid"""

    r_min: float
    r_max: float
    nfaces: int

    @property
    def delta_r(self) -> float:
        assert self.nfaces >= 2
        return (self.r_max - self.r_min) / (self.nfaces - 1)

    def faces(self) -> F:
        return np.linspace(self.r_min, self.r_max, self.nfaces, endpoint=True)

    def face_left_of(self, r: F) -> N:
        return np.floor((r - self.r_min) / self.delta_r).astype(np.int32)

    def r_of_face(self, i: NDArray[np.int32]) -> F:
        return self.r_min + i * self.delta_r

    def has_face(self, i: NDArray[np.int32]) -> NDArray[np.bool_]:
        return (i >= 0) & (i < self.nfaces)


@dataclass(frozen=True)
class CubicSplineHistograms:
    """Computes histograms for various weights, given fixed particle positions,
    using a cubic spline kernel."""

    grid: RGrid
    rp: F

    @cached_property
    def _f0_f1(self) -> tuple[N, N]:
        # Only faces just left and right of the particle will receive contributions
        f0 = self.grid.face_left_of(self.rp)
        f1 = f0 + 1
        return f0, f1

    @cached_property
    def _u0_u1(self) -> tuple[F, F]:
        f0, f1 = self._f0_f1
        u0 = (self.rp - self.grid.r_of_face(f0)) / self.grid.delta_r
        u1 = (self.rp - self.grid.r_of_face(f1)) / self.grid.delta_r
        return u0, u1

    @cached_property
    def _msk0_msk1(self) -> tuple[B, B]:
        f0, f1 = self._f0_f1
        msk0 = self.grid.has_face(f0)
        msk1 = self.grid.has_face(f1)
        return msk0, msk1

    @cached_property
    def _ker0_ker1(self) -> tuple[F, F]:
        msk0, msk1 = self._msk0_msk1
        u0, u1 = self._u0_u1
        ker0 = w_cubic(u0[msk0])
        ker1 = w_cubic(u1[msk1])
        return ker0, ker1

    def histogram_of(self, w: F) -> F:
        msk0, msk1 = self._msk0_msk1
        f0, f1 = self._f0_f1
        ker0, ker1 = self._ker0_ker1
        f0msk = f0[msk0]
        f1msk = f1[msk1]
        mass0 = np.bincount(f0msk, weights=w[msk0] * ker0, minlength=self.grid.nfaces)
        mass1 = np.bincount(f1msk, weights=w[msk1] * ker1, minlength=self.grid.nfaces)
        return (mass0 + mass1).astype(np.float64)


class DisplProfile(ABC):
    """I am an abstract particle displacement profile,
    following the quantities `n`, `P`, `Q` of RM17."""

    @property
    @abstractmethod
    def tau(self) -> float:
        """Return the lag `tau` (in sim time units) for this displacement profile"""

    @abstractmethod
    def dataframe(self) -> pd.DataFrame:
        """Return a pandas DataFrame with columns:
        - `r`: the grid radius profile point
        - `n`: the profile of average trajectory counts [Eq. (1)]
        - `P`: the profile of average trajectory displacement [Eq. (2)]
        - `Q`: the profile of average trajectory squared displacement [Eq. (3)]
        """


@dataclass(frozen=True)
class DisplProfileFromDumpPair(DisplProfile):
    """Given two particle dumps, I can compute a dataframe of n(r), P(r) and
    Q(r) quantities from eqs (1)--(3) of RM17."""

    p_init: pmp.ParticleDump
    p_final: pmp.ParticleDump
    grid: RGrid
    r_coord: str = "x1"

    @cached_property
    def tau(self) -> float:
        tau = self.p_final.time - self.p_init.time
        assert tau >= 0.0
        return tau

    def dataframe(self) -> pd.DataFrame:
        rp_i_s = self.p_init.dataframe()[self.r_coord]
        rp_f_s = self.p_final.dataframe()[self.r_coord]

        assert rp_i_s.index.name == rp_f_s.index.name == "gid"
        gid = rp_i_s.index
        rp_i = rp_i_s[gid].to_numpy()
        rp_f = rp_f_s[gid].to_numpy()
        delta_r = rp_i - rp_f

        h = CubicSplineHistograms(self.grid, rp_i)
        return pd.DataFrame(
            {
                "r": self.grid.faces(),
                "n": h.histogram_of(np.ones_like(rp_i)),
                "P": h.histogram_of(delta_r),
                "Q": h.histogram_of(delta_r**2),
            }
        ).set_index("r")


@dataclass(frozen=True)
class SummedDisplProfile(DisplProfile):
    profiles: Sequence[DisplProfile]
    show_progress: bool = True
    max_tau_deviation: float = 0.05

    @cached_property
    def tau(self) -> float:
        taus = np.array([p.tau for p in self.profiles])
        tau_mean = taus.mean()
        tau_dev = np.max(np.abs(taus / tau_mean - 1.0))
        if tau_dev > self.max_tau_deviation:
            raise ValueError(
                f"SummedDisplProfile: `tau` deviation across profiles is {tau_dev}, "
                f"which exceeds max_tau_deviation={self.max_tau_deviation}"
            )
        return tau_mean

    def _iter_profiles(self) -> Iterator[DisplProfile]:
        if self.show_progress:
            yield from tqdm.tqdm(
                self.profiles,
                desc="SummedDisplProfile",
                unit="prof",
            )
        else:
            yield from self.profiles

    def dataframe(self) -> pd.DataFrame:
        return sum(p.dataframe() for p in self._iter_profiles())  # type: ignore


@dataclass(frozen=True)
class CachedDisplProfile(DisplProfile):
    profile: DisplProfile

    @cached_property
    def tau(self) -> float:
        return self.profile.tau

    @cached_property
    def _df(self) -> pd.DataFrame:
        return self.profile.dataframe()

    def dataframe(self) -> pd.DataFrame:
        return self._df
