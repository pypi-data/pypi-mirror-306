from __future__ import annotations

import numpy as np


def first_zeros_up_from_0(r: np.ndarray, vr: np.ndarray) -> np.ndarray:
    """
    For an array `vr[r, theta]`, return locations `r0[theta]` of the first zero
    of `vr` encountered from `r=0` towards increasing `r`.
    For `theta` values for which no zero crossing is found, `r0[theta]` is set to 0.

    :param r: a 1D array of strictly increasing `r` coordinates
    :param vr: a 2D array of values with axes `[r, theta]`
    :returns: the 1D array `r0[theta] >= 0` of `r` coordinates of zero crossings
    :raises ValueError:
    """

    if not np.all(np.diff(r) > 0.0):
        raise ValueError("r must be strictly increasing")

    if not (np.min(r) < 0.0 and np.max(r) > 0.0):
        raise ValueError("r must change sign")

    # Keep radii from last r <= 0 and up
    # This is to ensure we don't capture zero crossings for r < 0
    icut: int = np.argmax(r > 0.0) - 1  # type: ignore
    r, vr = r[icut:], vr[icut:, :]

    # First index i such that vr[i] * vr[i+1] <= 0
    # Note that it might be that there is no such index; in this case,
    # i[theta] will be set to 0 through the behaviour of argmax.
    # This corner case will be handled later on.
    i = np.argmax(vr * np.roll(vr, -1, axis=0) <= 0, axis=0)

    # Linear interpolation of zero crossing between i and i+1
    vr_i = np.take_along_axis(vr, i[None, :], axis=0).squeeze(axis=0)
    vr_ip1 = np.take_along_axis(vr, i[None, :] + 1, axis=0).squeeze(axis=0)
    u = np.abs(vr_i) / (np.abs(vr_i) + np.abs(vr_ip1))
    r_cut = r[i] * (1 - u) + r[i + 1] * u
    r0 = np.maximum(r_cut, 0.0)

    # Detect and handle case of no zero crossing
    r0[vr_i * vr_ip1 > 0.0] = 0.0
    return r0
