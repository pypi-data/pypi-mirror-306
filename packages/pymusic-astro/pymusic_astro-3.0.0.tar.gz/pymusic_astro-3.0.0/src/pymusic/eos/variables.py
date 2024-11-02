from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

import numpy as np

from .interp import BivariateScalar
from .table import Table

if TYPE_CHECKING:
    from typing import Callable, Mapping

F = TypeVar("F", float, np.ndarray)  # scalar field generic type


@dataclass(frozen=True)
class DTState(Generic[F]):
    rho: F
    t: F

    @property
    def q(self) -> F:
        return self.rho - 2.0 * self.t + 12.0


@dataclass(frozen=True)
class QTState(Generic[F]):
    q: F
    t: F

    @property
    def rho(self) -> F:
        return self.q + 2.0 * self.t - 12.0


@dataclass(frozen=True)
class DEState(Generic[F]):
    rho: F
    e: F

    @property
    def v(self) -> F:
        return 20.0 + self.rho - 0.7 * self.e


@dataclass(frozen=True)
class VEState(Generic[F]):
    v: F
    e: F

    @property
    def rho(self) -> F:
        return self.v - 20.0 + 0.7 * self.e


@dataclass(frozen=True)
class LogDensityAtQT(BivariateScalar):
    def __call__(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        return QTState(q, t).rho

    def dx(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        """drho/dq|t = 1"""
        return np.asarray(1.0)

    def dy(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        """drho/dt|q = -2"""
        return np.asarray(-2.0)


@dataclass(frozen=True)
class LogTempAtQT(BivariateScalar):
    def __call__(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        return t

    def dx(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        """dt/dq|t = 0"""
        return np.asarray(0.0)

    def dy(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        """dt/dt|q = 1"""
        return np.asarray(1.0)


@dataclass(frozen=True)
class LogTotalPressureAtQT(BivariateScalar):
    p_gas_qt: BivariateScalar
    a_rad: float = 7.5657e-15  # 4*sigma/c, in CGS

    def _pressures(
        self, q: np.ndarray, t: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        press_gas = 10.0 ** self.p_gas_qt(q, t)
        temp4 = 10.0 ** (4.0 * t)
        press_rad = self.a_rad * temp4 / 3.0
        press_tot = press_gas + press_rad
        return press_gas, press_rad, press_tot

    def __call__(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        _, _, press_tot = self._pressures(q, t)
        return np.log10(press_tot)

    def _d(
        self, q: np.ndarray, t: np.ndarray, dp_gas: np.ndarray, dt: float
    ) -> np.ndarray:
        """Return d(logPtot)/dx given d(logPgas)/dx, d(logT)/dx"""
        press_gas, press_rad, press_tot = self._pressures(q, t)
        return ((press_gas * dp_gas) + (4.0 * press_rad * dt)) / press_tot

    def dx(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        return self._d(
            q,
            t,
            dp_gas=self.p_gas_qt.dx(q, t),
            dt=0.0,  # dt/dq|t = 0
        )

    def dy(self, q: np.ndarray, t: np.ndarray) -> np.ndarray:
        return self._d(
            q,
            t,
            dp_gas=self.p_gas_qt.dy(q, t),
            dt=1.0,  # dt/dt|q = 1
        )


@dataclass(frozen=True)
class DEDerivativesFromQTFuncs(Table):
    qt_at_ve: Table
    qt_funcs: Mapping[str, BivariateScalar]
    e_qt_func: BivariateScalar

    def coords(self) -> Mapping[str, np.ndarray]:
        return self.qt_at_ve.coords()

    def arrays(self) -> Mapping[str, np.ndarray]:
        # Eval derivatives wrt (q,t) at (v,e) node points
        qt_at_ve = self.qt_at_ve.arrays()
        q, t = qt_at_ve["logQ"], qt_at_ve["logT"]
        df_dq = {name: func.dx(q, t) for (name, func) in self.qt_funcs.items()}
        df_dt = {name: func.dy(q, t) for (name, func) in self.qt_funcs.items()}

        # Compute Jacobian matrix (q,t) -> (d,e)
        #   [dF/dq] = [ dF/dd * dd/dq + dF/de * de/dq ]
        #   [dF/dt] = [ dF/dd * dd/dt + dF/de * de/dt ]
        # In matrix form:
        #   [dF/d(q,t)] = J      * [dF/d(d,e)]  which inverts to:
        #   [dF/d(d,e)] = J^{-1} * [dF/d(q,t)]
        # with J = [[dd/dq, de/dq], [dd/dt, de/dt]] (in row order)
        # Recall:
        #   q = d - 2t + 12,
        # Therefore:
        #   dd/dq|t = 1
        #   dd/dt|q = 2
        # and:
        #   J  = [[1, de/dq|t], [2, de/dt|q]]
        #     := [[1, e_q], [2, e_t]]
        # which inverts to:
        #   J^{-1} = [[e_t, -e_q], [-2, 1]] / (e_t - 2e_q)

        e_q = self.e_qt_func.dx(q, t)
        e_t = self.e_qt_func.dy(q, t)

        # Check condition numbers of change of variables
        one = np.ones_like(e_q)
        matrices = np.array([[one, e_q], [2.0 * one, e_t]]).T  # Shape (..., 2, 2)
        cond = np.linalg.cond(matrices).T
        assert cond.shape == e_q.shape
        qs = [0.0, 0.01, 0.5, 0.99, 1.0]
        print(
            "Quantiles of log10(condnum) in Jacobian: "
            + ", ".join(
                f"q[{q}]={v:.3g}"
                for q, v in zip(qs, np.nanquantile(np.log10(cond), qs))
            )
        )

        # Solve system
        jm1_dq, jm1_dt = e_t, -e_q
        jm1_eq, jm1_et = -2.0, 1.0
        inv_det = 1.0 / (e_t - 2.0 * e_q)

        return {
            **{
                f"d{name}/dlogD|E": inv_det
                * (jm1_dq * df_dq[name] + jm1_dt * df_dt[name])
                for name in self.qt_funcs
            },
            **{
                f"d{name}/dlogE|D": inv_det
                * (jm1_eq * df_dq[name] + jm1_et * df_dt[name])
                for name in self.qt_funcs
            },
        }


@dataclass(frozen=True)
class WithDerivedArrays:
    table: Table
    field_funcs: Mapping[str, Callable]

    def coords(self) -> Mapping[str, np.ndarray]:
        return self.table.coords()

    def arrays(self) -> Mapping[str, np.ndarray]:
        arrays = self.table.arrays()
        return {
            **arrays,
            **{field: func(arrays) for (field, func) in self.field_funcs.items()},
        }
