import unittest
from typing import Any, Dict

from src.cachr import Cache, CacheStrategy
from src.cachr.caches import Cache


class TestBaseCache(unittest.TestCase):
    def test_cache_info_works(self):
        # Create Cache Strategy
        @Cache(capacity=2)
        def add_two_things(a, b):
            return a + b

        # CacheInfo exists and is dict
        assert add_two_things.cache_info() is not None
        assert isinstance(add_two_things.cache_info(), Dict)

        # currsize, hits and misses gets registered
        add_two_things(3, 3)
        assert add_two_things.cache_info()["currsize"] == 1
        assert add_two_things.cache_info()["misses"] == 1
        assert add_two_things.cache_info()["hits"] == 0

        add_two_things(3, 3)
        assert add_two_things.cache_info()["currsize"] == 1
        assert add_two_things.cache_info()["misses"] == 1
        assert add_two_things.cache_info()["hits"] == 1

        add_two_things(6, 6)
        assert add_two_things.cache_info()["currsize"] == 2
        assert add_two_things.cache_info()["misses"] == 2
        assert add_two_things.cache_info()["hits"] == 1

    def test_can_clear_cache(self):
        # Create Cache Strategy
        @Cache(capacity=2)
        def add_two_things(a, b):
            return a + b

        # CacheInfo exists and is dict
        assert add_two_things.cache_info() is not None
        assert isinstance(add_two_things.cache_info(), Dict)

        # currsize, hits and misses gets registered
        add_two_things(3, 3)
        add_two_things(3, 3)
        add_two_things(6, 6)
        assert add_two_things.cache_info()["currsize"] == 2
        assert add_two_things.cache_info()["misses"] == 2
        assert add_two_things.cache_info()["hits"] == 1

        # Clear
        add_two_things.clear()
        assert add_two_things.cache_info()["currsize"] == 0
        assert add_two_things.cache_info()["misses"] == 0
        assert add_two_things.cache_info()["hits"] == 0


class TestBaseCacheEviction(unittest.TestCase):
    def test_cache_info_works(self):
        # Create Cache Strategy
        @Cache(capacity=2)
        def add_two_things(a, b):
            return a + b

        # CacheInfo exists and is dict
        assert add_two_things.cache_info() is not None
        assert isinstance(add_two_things.cache_info(), Dict)

        # currsize, hits and misses gets registered
        add_two_things(3, 3)
        assert add_two_things.cache.get((3, 3)) is not None
        add_two_things(4, 4)
        assert add_two_things.cache.get((3, 3)) is not None

        # on inserting the third value, the first should be evicted
        add_two_things(6, 6)
        assert add_two_things.cache.get((3, 3)) is None


if __name__ == "__main__":
    unittest.main()
