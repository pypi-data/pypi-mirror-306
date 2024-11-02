from __future__ import annotations

from typing import Any, Iterator

import matplotlib.pyplot as plt
import pandas as pd

from pymusic.spec import (
    ChebNuFFTSignalModel,
    FixedPointNuFFTSolver,
    NoWindow,
    NuFFT1D,
    Signal,
)
from pymusic.spec.fft import FourierPairFromSignal
from pymusic.studies.nufft.utils import make_samplings, rms
from pymusic.studies.nufft.utils import rms as norm

num_points = 10000
tilde_sampling, unifm_sampling = make_samplings(num_points=num_points, gamma_approx=0.1)

sig = Signal(
    period=unifm_sampling.span,
    k_min=1,  # avoid 0 for spec_index < 0
    k_max=(unifm_sampling.num_points - 1) // 2,
    spec_index=0.0,
    real=False,
)

s = sig.signal(unifm_sampling.points)
s = s + 1j * s
s_tilde = sig.signal(tilde_sampling.points)
s_tilde = s_tilde + 1j * s_tilde

# Signal -> amplitudes
s_hat = FourierPairFromSignal(s, unifm_sampling).ampl
s_tilde_hat = FourierPairFromSignal(s_tilde, unifm_sampling).ampl

max_terms = 15


def make_fft(n: int) -> NuFFT1D:
    return NuFFT1D(
        window=NoWindow(),
        sampling_period=unifm_sampling.delta,
        signal_model=ChebNuFFTSignalModel(num_terms=n),
        spacing_tol=0.5,
        solver=FixedPointNuFFTSolver(verbosity=2),
    )


def gen_rows_ampl_to_signal() -> Iterator[dict[str, Any]]:
    for nterms in range(0, max_terms + 1):
        nufft = make_fft(nterms)
        # Estimate s(t_tilde) from s_hat, and compare with exact s_tilde
        s_tilde_nufft = nufft.signal_model.signal(tilde_sampling, unifm_sampling, s_hat)
        resid = s_tilde - s_tilde_nufft
        yield dict(nterms=nterms, relative_norm=norm(resid) / rms(s_tilde))


def gen_rows_signal_to_ampl() -> Iterator[dict[str, Any]]:
    for nterms in range(0, max_terms + 1):
        nufft = make_fft(nterms)
        plan = nufft.plan(sample_points=tilde_sampling.points)
        # Estimate amplitudes from s_tilde, and compare with exact amplitudes
        s_hat_nufft = plan.fourier_pair(signal=s_tilde)
        resid = s_hat - s_hat_nufft.ampl
        yield dict(nterms=nterms, relative_norm=norm(resid) / rms(s_hat))


def plot_test() -> None:
    fig, ax = plt.subplots()
    df_test_ampl_to_signal = pd.DataFrame(list(gen_rows_ampl_to_signal()))
    df_test_signal_to_ampl = pd.DataFrame(list(gen_rows_signal_to_ampl()))
    plt.semilogy(
        df_test_ampl_to_signal["nterms"].astype("int"),
        df_test_ampl_to_signal["relative_norm"],
        label="Ampl $\\rightarrow$ Signal",
        marker="s",
    )
    plt.semilogy(
        df_test_signal_to_ampl["nterms"].astype("int"),
        df_test_ampl_to_signal["relative_norm"],
        label="Signal $\\rightarrow$ Ampl",
        ls="--",
        marker="o",
    )
    ax.set_title(f"Chebyshev, {num_points} points")
    ax.axhline(1.0, color="gray")
    ax.set_xlim(0, max_terms)
    ax.set_ylim(1e-16, 10)
    ax.set_xlabel("Number of terms in expansion")
    ax.set_ylabel("Relative RMS error")
    print(df_test_ampl_to_signal)
    plt.legend()
    plt.show()


plot_test()
