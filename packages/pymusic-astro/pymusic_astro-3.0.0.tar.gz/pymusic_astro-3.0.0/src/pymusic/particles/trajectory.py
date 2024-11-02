from __future__ import annotations

import typing
from dataclasses import dataclass

import pandas as pd
import tqdm

if typing.TYPE_CHECKING:
    from typing import Iterable, Sequence

    from .dumps import ParticleDump


@dataclass(frozen=True)
class SingleParticleTrajectory:
    gid: int
    dumps: Sequence[ParticleDump]
    show_progress: bool = True

    def dataframe(self) -> pd.DataFrame:
        def dump_to_series(dump: ParticleDump) -> pd.DataFrame:
            series = dump.dataframe().loc[self.gid, :]
            series["time"] = dump.time
            return series  # type: ignore

        if self.show_progress:
            iterdumps: Iterable[ParticleDump] = tqdm.tqdm(
                self.dumps,
                desc=f"Gathering trajectory for particle #{self.gid}",
            )
        else:
            iterdumps = self.dumps

        return (
            pd.concat(
                [dump_to_series(dump) for dump in iterdumps],
                axis=1,
            )
            .T.set_index("time")
            .sort_index()
        )
