from __future__ import annotations

from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np

from pymusic.spec import (
    ChebNuFFTSignalModel,
    NoWindow,
    NuFFT1D,
    Signal,
    TaylorNuFFTSignalModel,
)
from pymusic.spec.fft import FourierPairFromSignal
from pymusic.studies.nufft.utils import COLORS, make_samplings
from pymusic.studies.nufft.utils import rms as norm

num_points = 10000
gamma_approx = 0.1
tilde_sampling, unifm_sampling = make_samplings(
    num_points=num_points, gamma_approx=gamma_approx
)


def make_signal(k_max_over_n: float = 0.5, spec_index: float = 0.0) -> Signal:
    return Signal(
        period=unifm_sampling.span,
        k_min=1,  # avoid 0 for spec_index < 0
        k_max=int(k_max_over_n * (num_points - 1)),  # -1 to stay clear of Nyquist
        spec_index=spec_index,
        real=False,
    )


Sig = namedtuple("Sig", ["name", "signal", "color"])
FFT = namedtuple("FFT", ["name", "factory", "style"])

signals = [
    Sig(
        name=r"$a(\omega) \sim 1$",
        signal=make_signal(k_max_over_n=0.5, spec_index=0.0),
        color=COLORS[0],
    ),
    # Sig(
    #     name="white_noise_half",
    #     signal=make_signal(k_max_over_n=0.25, spec_index=0.0),
    #     color=COLORS[1],
    # ),
    # Sig(
    #     name="slope -1",
    #     signal=make_signal(k_max_over_n=0.5, spec_index=-1.0),
    #     color=COLORS[2],
    # ),
    Sig(
        name=r"$a(\omega) \sim \omega^{-2}$",
        signal=make_signal(k_max_over_n=0.5, spec_index=-2.0),
        color=COLORS[3],
    ),
    # Sig(
    #     name="slope -3",
    #     signal=make_signal(k_max_over_n=0.5, spec_index=-3.0),
    #     color=COLORS[4],
    # ),
]


ffts = [
    FFT(
        name="Taylor",
        factory=lambda n: NuFFT1D(
            window=NoWindow(),
            sampling_period=unifm_sampling.delta,
            signal_model=TaylorNuFFTSignalModel(num_terms=n),
            spacing_tol=0.2,
        ),
        style=dict(ls="-", marker="s"),
    ),
    FFT(
        name="Chebyshev",
        factory=lambda n: NuFFT1D(
            window=NoWindow(),
            sampling_period=unifm_sampling.delta,
            signal_model=ChebNuFFTSignalModel(num_terms=n),
            spacing_tol=0.2,
        ),
        style=dict(ls="--", marker="o"),
    ),
]

fig_rms, ax_rms = plt.subplots(figsize=(6, 7))

for sig in signals:
    nmax = 15
    ns = range(nmax + 1)

    s_t_tilde = sig.signal.signal(tilde_sampling.points)
    s_t_unifm = sig.signal.signal(unifm_sampling.points)

    for fft in ffts:

        def resid(n: int) -> np.ndarray:
            nufft = fft.factory(n)
            ampl = FourierPairFromSignal(s_t_unifm, unifm_sampling).ampl
            plan = nufft.plan(sample_points=tilde_sampling.points)
            ampl_nufft = plan.fourier_pair(s_t_tilde).ampl
            return norm(ampl_nufft - ampl) / norm(ampl)

        ax_rms.semilogy(
            ns,
            [resid(n) for n in ns],
            label=f"{sig.name}, {fft.name}",
            color=sig.color,
            **fft.style,
        )

ax_rms.legend()
ax_rms.axhline(1.0, color="gray")
ax_rms.set_ylim(1e-16, 10)
ax_rms.set_xlabel("Number of terms in expansion")
ax_rms.set_ylabel(
    "Relative RMS error on Fourier coefficients, after fixed-point convergence"
)
ax_rms.set_title(rf"$N={num_points}, |\epsilon| \leq {gamma_approx:3g}$")
fig_rms.tight_layout()
fig_rms.savefig(f"nterms_np{num_points}.pdf", transparent=True)

plt.show()
