from __future__ import annotations

import typing
from dataclasses import dataclass

import numpy as np
from scipy.ndimage import zoom

from . import lic  # type: ignore
from . import stretch_funcs as pmstretch
from .figure import Plot

if typing.TYPE_CHECKING:
    from typing import Any, Callable, Protocol

    import matplotlib as mpl

    from .. import big_array as pma
    from .. import particles as pmp

    class BlendFunc(Protocol):
        def __call__(self, __arr1: np.ndarray, __arr2: np.ndarray) -> np.ndarray: ...

    class BlendCmapFunc(Protocol):
        def __call__(
            self, __arr1: np.ndarray, __arr2: np.ndarray, __cmap: mpl.colors.Colormap
        ) -> np.ndarray: ...


def pcolormesh_rgb(
    x: np.ndarray,
    y: np.ndarray,
    image: np.ndarray,
    axes: mpl.axes.Axes,
    **pcolormeshkwargs: Any,
) -> mpl.collections.QuadMesh:
    raveled_pixel_shape = (image.shape[0] * image.shape[1], image.shape[2])
    color_tuple = image.transpose((1, 0, 2)).reshape(raveled_pixel_shape)

    if color_tuple.dtype == np.uint8:
        color_tuple = color_tuple / 255.0

    index = np.tile(np.arange(image.shape[0]), (image.shape[1], 1))
    quad = axes.pcolormesh(
        x, y, index, color=color_tuple, linewidth=0, **pcolormeshkwargs
    )
    quad.set_array(None)
    return quad


def norm(x: np.ndarray) -> np.ndarray:
    return (x - x.mean()) / x.std()


def to_01(x: np.ndarray) -> np.ndarray:
    return np.clip(0.5 * (x + 1.0), 0.0, 1.0)


@dataclass(frozen=True)
class CustomBlend:
    def __call__(self, image: np.ndarray, perturb: np.ndarray) -> np.ndarray:
        perturb = norm(perturb)
        data = 2.0 * image - 1.0
        mag = np.abs(data)
        x0 = 0.3
        scale = 0.3 * (np.exp(1) / x0) * mag * np.exp(-mag / x0)
        return to_01(data * np.exp(perturb * scale))


@dataclass(frozen=True)
class OverlayBlend:
    strength: float = 0.5

    def __call__(self, image: np.ndarray, perturb: np.ndarray) -> np.ndarray:
        perturb = norm(perturb) * self.strength
        b = to_01(perturb)
        a = np.clip(image, 0, 1)
        mask = a < 0.5
        return mask * (2 * a * b) + (1 - mask) * (1 - 2 * (1 - a) * (1 - b))


@dataclass(frozen=True)
class BlendThenCmap:
    blend: BlendFunc

    def __call__(
        self, data: np.ndarray, perturb: np.ndarray, cmap: mpl.colors.Colormap
    ) -> np.ndarray:
        return cmap(self.blend(to_01(data), perturb))


@dataclass(frozen=True)
class CmapThenBlend:
    blend: BlendFunc

    def __call__(
        self, data: np.ndarray, perturb: np.ndarray, cmap: mpl.colors.Colormap
    ) -> np.ndarray:
        colors = cmap(to_01(data))
        image = np.dstack([self.blend(colors[:, :, i], perturb) for i in range(4)])
        # Copy alpha channel
        image[:, :, 3] = colors[:, :, 3]
        return image


@dataclass(frozen=True)
class ScalarAndVectorLicPlot:
    vector: pma.BigArray
    scalar: pma.BigArray
    cmap: mpl.colors.Colormap
    stretch: pmstretch.StretchFunc = pmstretch.LinearStretch(1.0)
    x1_remap: Callable = lambda x: x
    x2_remap: Callable = lambda x: x
    lic_upscale_factor: float = 1.0
    kernel_size: int | None = None
    random_seed: int = 42
    color_mode: BlendCmapFunc = BlendThenCmap(blend=CustomBlend())

    def _kernel(self) -> np.ndarray:
        if self.kernel_size is None:
            kernel_size = int(5 * self.lic_upscale_factor)
        else:
            kernel_size = self.kernel_size
        return np.sin(np.arange(kernel_size) * np.pi / kernel_size)

    def draw_on(self, ax: mpl.axes.Axes) -> None:
        x1 = np.array(self.vector.labels_along_axis("x1"))
        x2 = np.array(self.vector.labels_along_axis("x2"))
        assert self.vector.ndim == 3 and self.vector.shape[0] == 2
        v = self.vector.array()
        v1, v2 = (v[i, :, :] for i in range(2))

        dx1 = np.mean(np.diff(x1))
        dx2 = np.mean(np.diff(x2))
        assert np.allclose(np.diff(x1), dx1)
        assert np.allclose(np.diff(x2), dx2)

        upscale = lambda arr: zoom(arr, self.lic_upscale_factor)
        ux1, ux2 = upscale(x1), upscale(x2)
        # Upscale and transform velocities
        uv1 = upscale(v1) / dx1  # vr [cm/s -> pixel/s]
        uv2 = upscale(v2 / x1[:, None]) / dx2  # vtheta -> theta_dot [cm/s -> pixel/s]

        rng = np.random.default_rng(seed=self.random_seed)
        texture = rng.uniform(size=uv1.shape)
        kernel = self._kernel()
        lic_arr = lic.line_integral_convolution(
            uv1.astype("float32"),
            uv2.astype("float32"),
            texture.astype("float32"),
            kernel.astype("float32"),
        )

        assert self.scalar.ndim == 2
        up_c_data = zoom(
            self.scalar.array(),
            self.lic_upscale_factor,
            order=0,
        )
        img = self.color_mode(self.stretch(up_c_data), lic_arr, self.cmap)
        pcolormesh_rgb(
            self.x2_remap(ux2),
            self.x1_remap(ux1),
            img.swapaxes(0, 1),
            ax,
            shading="nearest",
        )


@dataclass(frozen=True, eq=False)
class ParticlesPlot(Plot):
    particle_data: pmp.ParticleDump
    axes: tuple[str, str] = ("x1", "x2")
    color_func: Callable = lambda df: "black"

    def draw_on(self, ax: mpl.axes.Axes) -> None:
        df = self.particle_data.dataframe()
        ax0, ax1 = self.axes
        ax.scatter(
            df[ax0].to_numpy(),
            df[ax1].to_numpy(),
            marker=".",
            s=5.0,
            c=self.color_func(df),
            edgecolors="none",
        )
