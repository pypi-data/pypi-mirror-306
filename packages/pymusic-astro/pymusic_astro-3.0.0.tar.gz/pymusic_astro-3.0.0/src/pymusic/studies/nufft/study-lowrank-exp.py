from __future__ import annotations

import typing
import warnings
from abc import ABC, abstractmethod
from functools import cached_property, lru_cache

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import dblquad, quad
from scipy.special import eval_chebyt, eval_legendre, jn

from pymusic.spec.nufft import _sum_primed

if typing.TYPE_CHECKING:
    from typing import Iterable


class Domain:
    def __init__(self, gamma: float = 0.5):
        self.gamma = gamma

    def grid(self, n: int) -> tuple[np.ndarray, np.ndarray]:
        x = np.linspace(-self.gamma, self.gamma, n, endpoint=True)
        y = np.linspace(0, 2 * np.pi, n, endpoint=True)
        return x, y

    def mesh_grid(self, n: int) -> tuple[np.ndarray, np.ndarray]:
        x, y = self.grid(n)
        return x[:, None], y[None, :]


class Function(ABC):
    @property
    @abstractmethod
    def domain(self) -> Domain:
        pass

    @abstractmethod
    def eval(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        pass

    def eval_grid(self, n: int) -> np.ndarray:
        x, y = self.domain.mesh_grid(n)
        return self.eval(x, y)

    def plot(self, n: int = 300, title: str | None = None) -> None:
        fig, axs = plt.subplots(nrows=1, ncols=2)

        x, y = self.domain.grid(n)
        f = self.eval_grid(n)

        im0 = axs[0].pcolormesh(x, y, f.real[:-1, :-1])  # , vmin=-4, vmax=4)
        im1 = axs[1].pcolormesh(x, y, f.imag[:-1, :-1])  # , vmin=-4, vmax=4)
        axs[0].set_title("Real")
        axs[1].set_title("Imag")

        for ax in axs.flat:
            ax.set_xlabel(r"$x = N \epsilon_j$")
            ax.set_ylabel(r"$y = 2 \pi k / N$")

        if title is not None:
            fig.suptitle(title)


class ExactFunction(Function):
    def __init__(self, domain: Domain):
        self._domain = domain

    @property
    def domain(self) -> Domain:
        return self._domain

    def eval(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.exp(-1j * x * y)


class Basis(ABC):
    def __init__(self, order: int):
        self.order = order

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def orders(self) -> Iterable[int]:
        return range(self.order)

    @abstractmethod
    def p_unnorm(self, m: int, u: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def weight(self, u: np.ndarray) -> np.ndarray:
        pass

    @lru_cache
    def norm(self, m: int) -> float:
        warnings.warn(
            "Basis:norm() uses @lru_cache, rather use @cached_property or similar to avoid global cache state"
        )

        def inner(u: np.ndarray) -> np.ndarray:
            return self.p_unnorm(m, u) ** 2 * self.weight(u)

        return np.sqrt(quad(inner, -1.0, 1.0)[0])

    def p(self, m: int, u: np.ndarray) -> np.ndarray:
        return self.p_unnorm(m, u) / self.norm(m)


class ChebyshevBasis(Basis):
    def p_unnorm(self, m: int, u: np.ndarray) -> np.ndarray:
        return eval_chebyt(m, u)

    def weight(self, u: np.ndarray) -> np.ndarray:
        return 1.0 / np.sqrt(1.0 - u**2)

    @property
    def name(self) -> str:
        return f"Chebyshev({self.order})"


class LegendreBasis(Basis):
    def p_unnorm(self, m: int, u: np.ndarray) -> np.ndarray:
        return eval_legendre(m, u)

    def weight(self, u: np.ndarray) -> np.ndarray:
        return np.asarray(1.0)

    @property
    def name(self) -> str:
        return f"Legendre({self.order})"


class BasisFit(Function):
    def __init__(self, sol: Function, basis: Basis):
        self.sol = sol
        self.basis = basis

    @property
    def domain(self) -> Domain:
        return self.sol.domain

    def _f0(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.exp(-1j * x * np.pi)  # "Compensation" term

    @cached_property
    def _coefs(self) -> np.ndarray:
        def coef(mx: int, my: int) -> np.ndarray:
            gamma = self.domain.gamma

            def f_inner(u: np.ndarray, v: np.ndarray) -> np.ndarray:
                x = u * gamma
                y = np.pi * (v + 1.0)
                return (
                    (self.sol.eval(x, y) / self._f0(x, y))
                    * self.basis.p(mx, u)
                    * self.basis.p(my, v)
                    * self.basis.weight(u)
                    * self.basis.weight(v)
                )

            re = dblquad(lambda u, v: f_inner(u, v).real, -1.0, 1.0, -1.0, 1.0)[0]
            im = dblquad(lambda u, v: f_inner(u, v).imag, -1.0, 1.0, -1.0, 1.0)[0]
            return re + 1j * im

        return np.array(
            [[coef(mx, my) for my in self.basis.orders] for mx in self.basis.orders]
        )

    def eval(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        c = self._coefs
        gamma = self.domain.gamma
        f = np.asarray(0.0)
        for mx in self.basis.orders:
            for my in self.basis.orders:
                u = x / gamma
                v = y / np.pi - 1.0
                f += (c[mx, my] * self.basis.p(mx, u) * self.basis.p(my, v)) * self._f0(
                    x, y
                )

        return f

    def plot_bfuncs(self) -> None:
        fig, ax = plt.subplots()
        for m in self.basis.orders:
            u = np.linspace(-1, 1, 1000)
            ax.plot(u, self.basis.p(m, u), label=str(m))
            ax.legend()


def study(order: int = 5) -> None:
    domain = Domain()
    func_exact = ExactFunction(domain)

    func_exact.plot(title="Exact")

    for basis in [ChebyshevBasis(order), LegendreBasis(order)]:
        func_fitted = BasisFit(func_exact, basis)
        func_fitted.plot(title=basis.name)

        func_fitted.plot_bfuncs()
        plt.title(basis.name)

    plt.show()


class PaperFunction(Function):
    def __init__(self, domain: Domain, order: int):
        self._domain = domain
        self.order = order

    @property
    def domain(self) -> Domain:
        return self._domain

    def a_pr_coef(self, p: int, r: int) -> float:
        if abs(p - r) % 2 == 0:
            x = -self.domain.gamma * np.pi / 2.0
            return 4.0 * (1j**r) * jn((p + r) / 2, x) * jn((r - p) / 2, x)
        else:
            return 0.0

    def eval(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        u = x / self.domain.gamma
        v = y / np.pi - 1.0
        return _sum_primed(
            _sum_primed(
                self.a_pr_coef(p, r)
                * np.exp(-1j * np.pi * x)
                * eval_chebyt(p, u)
                * eval_chebyt(r, v)
                for r in range(self.order)
            )
            for p in range(self.order)
        )


def test_paper_expansion() -> None:
    domain = Domain()
    func_exact = ExactFunction(domain)

    for order in range(20):
        func_paper = PaperFunction(domain, order=order)
        x, y = domain.mesh_grid(100)
        f1 = func_exact.eval(x, y)
        f2 = func_paper.eval(x, y)
        err = f1 - f2
        errnorm = np.sqrt(np.mean(np.real(err * err.conj())))
        print(f"order={order:2d} err={errnorm:5e}")

        # func_exact.plot(title="Exact")
        # func_paper.plot(title="Paper")


test_paper_expansion()
# study(order=5)

plt.show()
