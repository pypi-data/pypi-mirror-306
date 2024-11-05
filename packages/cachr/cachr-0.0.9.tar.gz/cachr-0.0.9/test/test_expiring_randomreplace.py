import time
import unittest

from src.cachr.caches import RandomReplaceCache


class TestExpiringLRUCache(unittest.TestCase):
    def test_randomreplacement(self):
        cache = RandomReplaceCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 1)
        cache.put("c", 1)

        self.assertTrue(cache.size == 2, msg="One value should be evicted")

    def test_randomreplacement_decorator(self):
        @RandomReplaceCache(capacity=2)
        def times_two(val):
            return val * 2

        times_two(val=1)
        times_two(val=2)
        times_two(val=3)
        self.assertTrue(len(times_two.cache) == 2, msg="One value should be evicted")


if __name__ == "__main__":
    unittest.main()
