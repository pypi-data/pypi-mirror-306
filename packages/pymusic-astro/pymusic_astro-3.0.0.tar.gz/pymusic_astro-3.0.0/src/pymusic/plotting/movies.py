from __future__ import annotations

import subprocess
import typing
from dataclasses import dataclass
from pathlib import Path

import tqdm

if typing.TYPE_CHECKING:
    from os import PathLike
    from typing import Iterable, Sequence

    from .figure import Figure


@dataclass(frozen=True)
class FfmpegMp4Movie:
    figures: Sequence[Figure]
    frames_dir: Path
    tune_preset: str = "animation"
    ctr: int = 30
    framerate: int = 20
    show_progress: bool = True

    @property
    def _frames_glob(self) -> Path:
        return self.frames_dir / "*.png"

    def render_to(self, movie_file: str | PathLike) -> None:
        if self.show_progress:
            iter_figs: Iterable[Figure] = tqdm.tqdm(
                self.figures, desc=f"Rendering frames for '{movie_file}'"
            )
        else:
            iter_figs = self.figures

        self.frames_dir.mkdir(parents=True, exist_ok=True)
        for i, fig in enumerate(iter_figs):
            fig.save_to(self.frames_dir / f"{i:05d}.png")

        if self.show_progress:
            print(f"Converting frames to '{movie_file}'")

        Path(movie_file).parent.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(self.framerate),
                "-pattern_type",
                "glob",
                "-i",
                str(self._frames_glob),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-crf",
                str(self.ctr),
                "-tune",
                self.tune_preset,
                "-loglevel",
                "error",
                str(movie_file),
            ]
        )
