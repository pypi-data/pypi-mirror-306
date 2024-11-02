"""
:mod:`pymusic.spec`: tools for spectral analysis
================================================

.. automodule:: pymusic.spec.fft
   :members:

.. automodule:: pymusic.spec.windows
   :members:

.. automodule:: pymusic.spec.spherical_harmonics
   :members:

.. automodule:: pymusic.spec.wedge_harmonics

.. automodule:: pymusic.spec.wedge_harmonics_array
   :members:


"""

from .fft import *
from .nufft import *
from .spherical_harmonics import *
from .wedge_harmonics import *
from .wedge_harmonics_array import WedgeHarm1DArray
from .windows import *
