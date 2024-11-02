from __future__ import annotations

import typing
from collections import OrderedDict
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from typing import Any, Hashable


@dataclass
class _CacheStats:
    requests: int = 0
    hits: int = 0
    evictions: int = 0


class LRUCache:
    def __init__(self, size: int):
        self.size = size
        self.cache: OrderedDict = OrderedDict()
        self.stats = _CacheStats()

    def __getitem__(self, key: Hashable) -> Any:
        self.stats.requests += 1
        value = self.cache.pop(key)
        self.cache[key] = value
        self.stats.hits += 1
        return value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.stats.requests += 1
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.size:
                self.cache.popitem(last=False)
                self.stats.evictions += 1
        self.cache[key] = value
