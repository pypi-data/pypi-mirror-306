from __future__ import annotations

import operator
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property, reduce
from pathlib import Path

import h5py
import numpy as np
import tqdm

if typing.TYPE_CHECKING:
    from typing import Any, Iterable, Sequence

    from matplotlib.axes import Axes

    from .dumps import ParticleDump


class CountsMatrix(ABC):
    """Matrix of counts N(start=i, end=j) for particles starting in bin i,
    and ending in bin j, of a set of bins.
    This is the basic building block for transilient matrices using particle counts.
    """

    @abstractmethod
    def counts_matrix(self) -> np.ndarray:
        """Counts matrix N(start=i, end=j)"""

    @abstractmethod
    def bin_edges(self) -> np.ndarray:
        """Bin edges for this transilient counts matrix"""

    @abstractmethod
    def delta_t(self) -> float:
        """Time interval for this matrix"""


@dataclass(frozen=True, eq=False)
class ParticleDumpsCountsMatrix(CountsMatrix):
    """A CountsMatrix object defined by a start and end particle dumps,
    where particle position (and bin) is determined from a given particle data column.
    """

    pd0: ParticleDump
    pd1: ParticleDump
    column: str
    bins: np.ndarray = field(repr=False)

    def counts_matrix(self) -> np.ndarray:
        df0 = self.pd0.dataframe()[[self.column]]
        df1 = self.pd1.dataframe()[[self.column]]
        assert df0.index.name == df1.index.name == "gid"
        # Inner join on index (particle gid), so we only consider
        # particles present in *both* dumps
        df = df0.join(df1, how="inner", lsuffix="_0", rsuffix="_1")
        h, _, _ = np.histogram2d(
            x=df[self.column + "_0"].to_numpy(),
            y=df[self.column + "_1"].to_numpy(),
            bins=(self.bins, self.bins),
        )
        return h

    def bin_edges(self) -> np.ndarray:
        return self.bins

    def delta_t(self) -> float:
        return float(self.pd1.time - self.pd0.time)


@dataclass(frozen=True, eq=False)
class CachedCountsMatrix(CountsMatrix):
    """A caching decorator for CountsMatrix objects"""

    counts: CountsMatrix

    @cached_property
    def _cached_counts_matrix(self) -> np.ndarray:
        return self.counts.counts_matrix()

    @cached_property
    def _cached_bin_edges(self) -> np.ndarray:
        return self.counts.bin_edges()

    @cached_property
    def _cached_delta_t(self) -> float:
        return self.counts.delta_t()

    def counts_matrix(self) -> np.ndarray:
        return self._cached_counts_matrix

    def bin_edges(self) -> np.ndarray:
        return self._cached_bin_edges

    def delta_t(self) -> float:
        return self._cached_delta_t


@dataclass(frozen=True, eq=False)
class AccumulatedCountsMatrix(CountsMatrix):
    counts_seq: Sequence[CountsMatrix]
    delta_t_tol: float = 0.02
    show_progress: bool = True

    def _iter(self, it: Iterable[np.ndarray]) -> Iterable[np.ndarray]:
        if self.show_progress:
            return tqdm.tqdm(
                it,
                total=len(self.counts_seq),
                desc="AccumulatedCountsMatrix",
            )
        return it

    def counts_matrix(self) -> np.ndarray:
        return reduce(
            operator.add, self._iter(m.counts_matrix() for m in self.counts_seq)
        )

    def bin_edges(self) -> np.ndarray:
        def check(b1: np.ndarray, b2: np.ndarray) -> np.ndarray:
            if not np.all(b1 == b2):
                raise ValueError("inconsistent bins across CountsMatrix sequence")
            return b1

        return reduce(check, (m.bin_edges() for m in self.counts_seq))

    def delta_t(self) -> float:
        dts = [m.delta_t() for m in self.counts_seq]
        dt_mean = np.mean(dts)
        err = (np.max(dts) - np.min(dts)) / dt_mean
        if err > self.delta_t_tol:
            raise ValueError(
                f"Inconsistent dt: deviation {err} exceeds tolerance {self.delta_t_tol}"
            )
        return float(dt_mean)


@dataclass(frozen=True, eq=False)
class H5FileCountsMatrix(CountsMatrix):
    file_name: str

    def _read(self, key: str) -> Any:
        if not Path(self.file_name).exists():
            raise FileNotFoundError(self.file_name)

        try:
            with h5py.File(self.file_name, mode="r") as f:
                return f[key][()]
        except KeyError:
            raise ValueError(
                f"{self.file_name}: invalid format, missing entry={key}"
            ) from None

    def counts_matrix(self) -> np.ndarray:
        return self._read("/counts")

    def bin_edges(self) -> np.ndarray:
        return self._read("/bin_edges")

    def delta_t(self) -> float:
        return self._read("/delta_t")

    # Own interface

    def write(self, counts: CountsMatrix) -> None:
        counts_matrix = counts.counts_matrix()
        bin_edges = counts.bin_edges()
        delta_t = counts.delta_t()
        with h5py.File(self.file_name, mode="w") as f:
            f.create_dataset("/counts", data=counts_matrix)
            f.create_dataset("/bin_edges", data=bin_edges)
            f.create_dataset("/delta_t", data=delta_t)


@dataclass(frozen=True, eq=False)
class DiskCachedCountsMatrix(CountsMatrix):
    counts: CountsMatrix
    cache_file_name: str

    @cached_property
    def _cache_file(self) -> H5FileCountsMatrix:
        Path(self.cache_file_name).parent.mkdir(parents=True, exist_ok=True)
        return H5FileCountsMatrix(self.cache_file_name)

    def _write_cache(self) -> None:
        self._cache_file.write(self.counts)

    def counts_matrix(self) -> np.ndarray:
        try:
            return self._cache_file.counts_matrix()
        except (ValueError, FileNotFoundError):
            self._write_cache()
            return self._cache_file.counts_matrix()

    def bin_edges(self) -> np.ndarray:
        try:
            return self._cache_file.bin_edges()
        except (ValueError, FileNotFoundError):
            self._write_cache()
            return self._cache_file.bin_edges()

    def delta_t(self) -> float:
        try:
            return self._cache_file.delta_t()
        except (ValueError, FileNotFoundError):
            self._write_cache()
            return self._cache_file.delta_t()


@dataclass(frozen=True, eq=False)
class ScaledUnitsCountsMatrix(CountsMatrix):
    """A CountsMatrix with space and time units divided by the provided factors"""

    counts: CountsMatrix
    length_scale: float = 1.0
    time_scale: float = 1.0

    def counts_matrix(self) -> np.ndarray:
        return self.counts.counts_matrix()

    def bin_edges(self) -> np.ndarray:
        return self.counts.bin_edges() / self.length_scale

    def delta_t(self) -> float:
        return self.counts.delta_t() / self.time_scale


@dataclass(frozen=True, eq=False)
class DownsampledCountsMatrix(CountsMatrix):
    """A CountsMatrix downsampled by the given integer factor, i.e. whose input bins
    are summed together in contiguous groups of `factor` into output bins.
    """

    counts: CountsMatrix
    factor: int

    def counts_matrix(self) -> np.ndarray:
        m = self.counts.counts_matrix()
        n = m.shape[0]
        f = self.factor
        assert n % f == 0
        assert m.shape == (n, n)
        n2 = n // f
        m2 = np.zeros((n2, n2), dtype=m.dtype)
        for i in range(f):
            for j in range(f):
                m2[:, :] += m[i::f, j::f]
        assert m2.sum() == m.sum()
        return m2

    def bin_edges(self) -> np.ndarray:
        b = self.counts.bin_edges()
        assert (b.size - 1) % self.factor == 0
        return b[:: self.factor]

    def delta_t(self) -> float:
        return self.counts.delta_t()


@dataclass(frozen=True, eq=False)
class TransilientMatrix(CountsMatrix):
    """A "smart decorator" to add all sorts of useful calculations to CountsMatrix"""

    counts: CountsMatrix

    # Implementation of CountsMatrix: just forward to `counts`

    def bin_edges(self) -> np.ndarray:
        return self.counts.bin_edges()

    def counts_matrix(self) -> np.ndarray:
        return self.counts.counts_matrix()

    def delta_t(self) -> float:
        return self.counts.delta_t()

    # Transilient matrix calculations

    def matrix(self) -> np.ndarray:
        """Return the transilient matrix, n(start=i, end=j), normalized to 1."""
        h = self.counts_matrix()
        return h / h.sum()

    def joint_prob(self) -> np.ndarray:
        """Return the joint probability Prob(end=i, start=j)"""
        return self.matrix().T

    def propagator_matrix(self) -> np.ndarray:
        """Return the propagator matrix, i.e. the conditional probability matrix
        whose element [i, j] is Prob(end=i | start=j)"""
        p_joint = self.joint_prob()
        p_start_j = p_joint.sum(axis=0)  # Prob(start=j)
        return p_joint / p_start_j[None, :]  # Prob(end=i | start=j)

    def bin_mids(self) -> np.ndarray:
        bins = self.bin_edges()
        return 0.5 * (bins[1:] + bins[:-1])

    def bin_span(self) -> tuple[float, float]:
        bins = self.bin_edges()
        return np.min(bins), np.max(bins)

    def antisym(self) -> np.ndarray:
        """Return the antisymmetric part of the matrix"""
        m = self.matrix()
        return 0.5 * (m - m.T)

    def psi0(self) -> np.ndarray:
        """The Psi vector of Ebert et al. 1989 (average scalar value per bin)
        at initial time"""
        m = self.matrix()
        return m.sum(axis=1)

    def kinematic_flux(self) -> np.ndarray:
        """Kinematic flux of Ebert et al. 1989, up to factors of delta_t and delta_z"""
        c_ij = self.joint_prob()
        psi = self.psi0()
        psi_i = psi[:, None]
        psi_j = psi[None, :]
        return np.cumsum(np.sum(c_ij * (psi_i - psi_j), axis=1))

    def cached(self) -> TransilientMatrix:
        """Returned a new TransilientMatrix with underlying CountsMatrix cached"""
        return TransilientMatrix(CachedCountsMatrix(self.counts))


@dataclass(frozen=True, eq=False)
class TransMatPenetrationDepth:
    mat: TransilientMatrix
    r_conv: float

    def profile(self) -> np.ndarray:
        m = self.mat.matrix()
        return m[self.mat.bin_mids() > self.r_conv, :].sum(axis=0)

    def penetration_depth(self) -> np.ndarray:
        profile = self.profile()
        prof_cut = 0.5 * profile.max()
        i: int = np.argmax(profile > prof_cut)  # type: ignore
        assert i > 0
        assert profile[i - 1] <= prof_cut and profile[i] > prof_cut
        r_cut = np.interp(
            prof_cut, profile[i - 1 : i + 1], self.mat.bin_mids()[i - 1 : i + 1]
        )
        depth = self.r_conv - r_cut
        return depth

    def plot_profile(self, ax: Axes, **kwargs: Any) -> None:
        ax.plot(self.mat.bin_mids(), self.profile(), **kwargs)
        ax.axvline(self.r_conv, ls="--", color="k")
        ax.set_xlabel("$r_f$ [cm]")
        ax.set_ylabel("Prob($r_f | r_i > r_\\mathrm{conv}$)")
        ax.set_yticks([])


@dataclass(frozen=True)
class DeltaT:
    delta_t: float
    tau_conv: float

    @property
    def n_tau_conv(self) -> float:
        return self.delta_t / self.tau_conv

    @property
    def label(self) -> str:
        return f"{self.n_tau_conv:#.3g} \\; \\tau_\\mathrm{{conv}}"
