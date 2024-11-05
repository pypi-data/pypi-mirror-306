import collections
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Optional, Callable

from . import policies


@dataclass
class _CacheInfo:
    maxsize: int
    hits: int = 0
    misses: int = 0

    def __init__(self, maxsize: int):
        self.maxsize = maxsize

    def reset(self):
        self.hits = 0
        self.misses = 0
        self.maxsize = self.maxsize

    def as_dict(self, cur_size: int):
        return {
            "hits": self.hits,
            "misses": self.misses,
            "maxsize": self.maxsize,
            "currsize": cur_size,
        }


class Cache:
    cache: OrderedDict
    capacity: int
    _cache_info: _CacheInfo
    _cache_strategy: policies.CacheStrategy

    def __init__(
        self,
        capacity: int,
        cache_strategy: policies.CacheStrategy = policies.DefaultEvictionPolicy(),
    ):
        self.cache: OrderedDict[Any, Any] = OrderedDict()
        self.capacity: int = capacity
        self._cache_strategy = cache_strategy
        self._cache_info = _CacheInfo(maxsize=capacity)

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve value from cache by provided key - cache hit or miss."""

        if key not in self.cache:
            self._cache_info.misses += 1
            return None
        self._cache_info.hits += 1
        self._cache_strategy.on_access(self, key)
        return self.cache.get(key)

    def put(self, key: Any, value: Any) -> None:
        """Insert a key-value pair into the cache."""

        if key in self.cache:
            # Overwrite
            self._cache_strategy.on_access(self, key)
        else:
            # Add
            self._cache_strategy.on_insert(self, key)
        self.cache[key] = value

    # region CONVENIENCE METHODS
    def clear(self):
        self.cache.clear()
        self._cache_info.reset()

    @property
    def size(self) -> int:
        """Return the number of items in the cache"""
        return len(self.cache)

    # endregion

    def __get_cache_info(self):
        return self._cache_info.as_dict(cur_size=self.size)

    def __refresh_cache(self):
        """Calls the evict method to refresh the cache; rid it of all expired or exess keys"""
        self._cache_strategy.evict(cache=self)

    # def __reset_cache_info(self) -> None:
    #     self._cache_info.reset()

    # region DECORATOR
    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # The ars and kwargs will be the key of the cache
            key = args + tuple(kwargs.items())

            # Try to retrieve result from cache
            result = self.get(key)

            # If key not in cache: retrieve and return
            if result is None:
                result = func(*args, **kwargs)
                self.put(key=key, value=result)
            return result

        # Add convenience methods on the cache
        wrapper.cache_info = self.__get_cache_info
        wrapper.clear = self.clear
        wrapper.cache = self.cache
        # wrapper.reset = self.__reset_cache_info
        wrapper.refresh = self.__refresh_cache

        return wrapper

    # endregion


class LRUCache(Cache):
    def __init__(self, capacity: int):
        super().__init__(capacity=capacity, cache_strategy=policies.LRUEvictionPolicy())


class TTLCache(Cache):
    def __init__(self, capacity: int, ttl_seconds: float):
        super().__init__(
            capacity=capacity,
            cache_strategy=policies.TTLEvictionPolicy(ttl_seconds=ttl_seconds),
        )


class SlidingWindowCache(Cache):
    def __init__(self, capacity: int, expiration_seconds: float):
        super().__init__(
            capacity=capacity,
            cache_strategy=policies.SlidingWindowEvictionPolicy(
                expiration_seconds=expiration_seconds
            ),
        )


class LFUCache(Cache):
    def __init__(
        self,
        capacity: int,
    ):
        super().__init__(capacity=capacity, cache_strategy=policies.LFUEvictionPolicy())


class RandomReplaceCache(Cache):
    def __init__(
        self,
        capacity: int,
    ):
        super().__init__(
            capacity=capacity, cache_strategy=policies.RandomEvictionPolicy()
        )
