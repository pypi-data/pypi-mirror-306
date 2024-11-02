from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from pymusic.spec.fft import UniformSampling

from ...spec import GivenPointsSampling

if typing.TYPE_CHECKING:
    from ...spec.fft import Sampling, UniformSampling

# the 10 colors in the default matplotlib cycle, from the "tab10" cmap
COLORS = tuple(
    f"tab:{c}"
    for c in (
        "blue",
        "orange",
        "green",
        "red",
        "purple",
        "brown",
        "pink",
        "gray",
        "olive",
        "cyan",
    )
)


def rms(x: np.ndarray) -> np.ndarray:
    return np.sqrt(np.mean(np.abs(x) ** 2))


def max_abs(x: np.ndarray) -> np.ndarray:
    return np.max(np.abs(x))


SIM_T_TILDE = "krad1d2_dtrec2d2"


def load_sim(sim_name: str) -> tuple[np.ndarray, np.ndarray]:
    "Load dump times and signal data from one of the krad simulations"
    df = pd.read_hdf("krad-sims-timepoints.h5", key=sim_name)
    t_tilde = df["time"].to_numpy() * 1e-6  # Convert times to Ms
    s_tilde = df["data"].to_numpy()
    return t_tilde, s_tilde


def load_t_tilde() -> np.ndarray:
    t_tilde, _ = load_sim(SIM_T_TILDE)
    return t_tilde


def make_samplings(
    num_points: int, delta: float = 1.0, gamma_approx: float = 0.2, seed: int = 43
) -> tuple[Sampling, UniformSampling]:
    t_unifm = np.arange(0, num_points) * delta

    rng = np.random.default_rng(seed=seed)
    eps_linf = gamma_approx * delta
    eps = rng.uniform(low=-eps_linf, high=eps_linf, size=num_points)
    t_tilde = t_unifm + eps

    tilde_sampling = GivenPointsSampling(
        sample_points=t_tilde, span_=num_points * delta
    )
    unifm_sampling = UniformSampling(x0=0.0, num_points=num_points, delta=delta)
    return tilde_sampling, unifm_sampling
