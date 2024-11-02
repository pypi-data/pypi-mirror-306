"""
:mod:`.exceptions`: exceptions for the :mod:`.big_array` module
===============================================================
"""


class BigArrayException(Exception):
    """Base exception for all :mod:`.big_array` related errors"""

    pass


class AxisError(BigArrayException, ValueError):
    """Invalid axis for array operation"""

    pass


class IndexLabelError(BigArrayException, KeyError):
    """Invalid label for index"""

    pass


class BigArrayShapeError(BigArrayException, ValueError):
    """Incompatible shape"""

    pass


class IncompatibleIndexesError(BigArrayException, ValueError):
    """Incompatible indexes"""

    pass


class BigArrayWarning(UserWarning):
    """Warnings related to big_array operations"""

    pass


class BigArrayPerformanceWarning(BigArrayWarning):
    """Performance-related warnings"""

    pass
