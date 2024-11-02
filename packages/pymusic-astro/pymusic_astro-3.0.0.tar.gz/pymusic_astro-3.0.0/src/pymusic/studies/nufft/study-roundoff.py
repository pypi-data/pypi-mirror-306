#!/usr/bin/env python

"""
Test roundoff error impact on Fourier differentiation,
as a function of number of samples and differentiation order.
"""

from __future__ import annotations

import typing

import numpy as np
import pandas as pd
import tqdm

from pymusic.spec import FourierPairFromSignal, Signal
from pymusic.spec.fft import SmartFourierPair, UniformSampling

if typing.TYPE_CHECKING:
    from typing import Iterable, Iterator


def rms(x: np.ndarray) -> np.ndarray:
    """L2 norm (as RMS) for a complex array"""
    return np.sqrt(np.mean(np.real(x * x.conj())))


def error_dicts(
    n_values: Iterable[int], ndiff_values: Iterable[int]
) -> Iterator[dict[str, int]]:
    for n in n_values:
        samples = UniformSampling(x0=0.0, num_points=n, delta=1.0)

        # Create a white noise signal, without aliasing!
        k_nyq = (n - 1) // 2  # Careful about Nyquist mode
        signal = Signal(period=samples.span, k_min=0, k_max=k_nyq, spec_index=0.0)

        # Compute signal in real space
        t = samples.points
        s = signal.signal(t)

        # Signal in Fourier space
        s_hat = SmartFourierPair(FourierPairFromSignal(s, samples))

        for ndiff in ndiff_values:
            # Differentiate in real space ...
            dn_s = signal.signal_diff(t, ndiff)
            # ... and in Fourier space
            dn_s_hat = s_hat.diff(ndiff)

            # Compare in real space
            dn_s_bar = dn_s_hat.signal  # Keep the imag part for error calc
            err = rms(dn_s - dn_s_bar) / rms(dn_s)
            yield dict(n=n, ndiff=ndiff, error=err)


n_values = [10**k for k in [1, 2, 3, 4]]
ndiff_values = range(1, 10 + 1)

errors = pd.DataFrame(
    list(
        tqdm.tqdm(
            error_dicts(n_values=n_values, ndiff_values=ndiff_values),
            total=len(n_values) * len(ndiff_values),
        )
    )
)

errors = errors.set_index(["n", "ndiff"])
print(errors)
