import unittest
from typing import Any

from src.cachr import Cache, CacheStrategy


class TestCompose(unittest.TestCase):
    def test_get_existing_key(self):
        # Create Cache Strategy
        class PrintCache(CacheStrategy):
            def on_access(self, cache: "Cache", key: Any) -> None:
                print(f"accessing {key=}")

            def on_insert(self, cache: "Cache", key: Any) -> None:
                if len(cache.cache) >= cache.capacity:
                    self.evict(cache=cache)
                print(f"inserting {key=}")

            def evict(self, cache: "Cache") -> None:
                if cache.cache:
                    evicted = cache.cache.popitem(last=False)
                    print(f"evicted key={evicted[0]}")

        cache = Cache(capacity=2, cache_strategy=PrintCache())
        cache.put(key=1, value="one")
        cache.put(key=2, value="two")
        cache.get(key=1)
        cache.put(key=3, value="three")
        print(cache.size)
        self.assertEqual(first=2, second=cache.size, msg="Cache should be of size == 2")
        self.assertEqual(
            first="two", second=cache.cache.get(2), msg="'two' should be in cache"
        )
        self.assertEqual(
            first="three",
            second=cache.cache.get(3),
            msg="'three' should be in cache",
        )
        self.assertIsNone(obj=cache.get(1), msg="'one' should not be in cache")


if __name__ == "__main__":
    unittest.main()
