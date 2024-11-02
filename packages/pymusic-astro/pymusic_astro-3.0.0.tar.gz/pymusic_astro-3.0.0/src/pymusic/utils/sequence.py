from __future__ import annotations

from dataclasses import dataclass
from itertools import islice
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from typing import Iterable, Iterator, Sequence


T = TypeVar("T")


def all_equal_or_empty(lst: Sequence) -> bool:
    return len(lst) == 0 or lst.count(lst[0]) == len(lst)


def all_equal(lst: Sequence) -> bool:
    return 0 < len(lst) == lst.count(lst[0])


def pairwise(it: Iterable[T]) -> Iterator[tuple[T, T]]:
    """Iterate over successive pairs (a, b), (b, c), (c, d), ...
    of an iterator (a, b, c, d, ...)

    Note that `itertools.pairwise` exists in Python >= 3.10 but is implemented
    here for convenience.
    """
    single_it = iter(it)
    b = next(single_it)
    for x in single_it:
        a, b = b, x
        yield a, b


@dataclass(frozen=True, eq=False)
class LaggedPairs(Generic[T]):
    """Iterable over all pairs of a sequence `seq` which produces:
        (seq[0    ], seq[lag      ]), (seq[lag      ], seq[2*lag      ]), ...
        (seq[shift], seq[lag+shift]), (seq[lag+shift], seq[2*lag+shift]), ...
        ...
    i.e jumping forward by `lag` starting from 0, and shifting the starting
    index (initially 0) by `shift` when wrapping around.

    This is useful e.g. for time-averaged lagged quantities. Pairwise iteration is
    useful e.g. together with caching, to reuse items of the sequence. In this
    case, caching should be applied inside the sequence `seq` before passing to
    this object.
    """

    seq: Sequence[T]
    lag: int
    shift: int

    def __post_init__(self) -> None:
        if self.lag <= 0:
            raise ValueError(
                f"{type(self).__name__}: invalid lag={self.lag}, must be > 0"
            )

    def __iter__(self) -> Iterator[tuple[T, T]]:
        istarts = range(0, self.lag, self.shift) if self.shift > 0 else [0]
        for istart in istarts:
            for item0, item1 in pairwise(islice(self.seq, istart, None, self.lag)):
                yield item0, item1

    def __len__(self) -> int:
        return sum(1 for _ in self)


@dataclass(frozen=True, eq=False)
class EquispacedProgressLags:
    """Iterable over a sequence of integers (representing "lags", for instance
    an integer number of uniform timesteps) such that the resulting lags are
    (approximately) equispaced in "progress" (akin to e.g. extent of reaction
    in chemistry), where progress is taken to scale as:

        progress ~ lag ** progress_exponent

    progress_exponent=2.0 corresponds for instance to a diffusive process.

    The iterator produces `num_lags` lags in the range [`min_lag`, `max_lag`].
    Lags smaller than min_lag are clipped to min_lag; this is done for
    convenience because zero lag can be problematic in other objects and
    analyses.
    """

    max_lag: int
    num_lags: int
    progress_exponent: float = 2.0
    min_lag: int = 1

    def __post_init__(self) -> None:
        assert self.num_lags > 0
        assert self.progress_exponent > 0
        assert self.max_lag > 0

    def __len__(self) -> int:
        return self.num_lags

    def __iter__(self) -> Iterator[int]:
        for i in range(self.num_lags):  # 0 <= i <= num_lags-1
            progress = (i + 1) / self.num_lags  # 0 < progress <= 1
            u = progress**self.progress_exponent  # 0 < u <= 1
            lag = max(self.min_lag, int(round(u * self.max_lag)))
            yield lag
