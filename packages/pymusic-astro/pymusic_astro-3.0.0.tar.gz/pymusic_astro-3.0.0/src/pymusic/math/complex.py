"""
:mod:`pymusic.math.complex`: utilities for complex numbers
==========================================================

"""

from __future__ import annotations

import numpy as np


def abs2(z: np.ndarray) -> np.ndarray:
    """Square modulus of an array of complex numbers"""
    return np.real(z * np.conj(z))
