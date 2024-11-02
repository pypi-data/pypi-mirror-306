import numpy
from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize("src/pymusic/plotting/lic.pyx"),
    include_dirs=[numpy.get_include()],
)
