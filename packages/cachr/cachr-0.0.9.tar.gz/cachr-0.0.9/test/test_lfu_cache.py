import time
import unittest

from src.cachr.caches import LFUCache


class TestLRUCache(unittest.TestCase):
    def test_get_least_frquency_used_newest_key(self):
        cache = LFUCache(capacity=2)
        cache.put(key=1, value="one")
        time.sleep(0.01)
        cache.put(key=2, value="two")
        self.assertEqual(
            cache.cache.get(1),
            second="one",
            msg="Failed to retrieve an existing key with value 'one'",
        )
        cache.put(key=3, value="three")
        self.assertEqual(
            cache.cache.get(1),
            second=None,
            msg="Failed to retrieve an existing key with value 'one'",
        )

        cache = LFUCache(capacity=2)
        cache.put(key=2, value="two")
        time.sleep(0.01)
        cache.put(key=1, value="one")
        self.assertEqual(
            cache.cache.get(2),
            second="two",
            msg="Failed to retrieve an existing key with value 'one'",
        )
        cache.put(key=3, value="three")
        self.assertEqual(
            cache.cache.get(2),
            second=None,
            msg="Failed to retrieve an existing key with value 'two'",
        )

        # Assert gets most used
        cache = LFUCache(capacity=2)
        cache.put(key=1, value="one")
        time.sleep(0.01)
        cache.put(key=2, value="two")
        cache.put(key=1, value="one")
        self.assertEqual(
            cache.cache.get(2),
            second="two",
            msg="Failed to retrieve oldest, yet most frequenctly used key with value 'two'",
        )

    def test_get_non_existing_key(self):
        cache = LFUCache(capacity=2)
        cache.put(key=1, value="one")
        self.assertIsNone(
            cache.cache.get(2),
            msg="Expected None when trying to get a non-existing key",
        )

    def test_put_and_evict(self):
        cache = LFUCache(capacity=2)
        cache.put(key=1, value="one")
        cache.put(key=2, value="two")
        cache.put(key=3, value="three")  # This should evict key 1
        self.assertIsNone(
            cache.get(key=1), msg="Failed to evict the least recently used key"
        )
        self.assertEqual(
            cache.get(key=2), "two", msg="Failed to retrieve key '2' after eviction"
        )
        self.assertEqual(
            cache.get(key=3), "three", msg="Failed to retrieve newly added key '3'"
        )

    def test_put_and_evict_overflow(self):
        cache = LFUCache(capacity=2)
        cache.put(key=1, value="one")
        cache.put(key=2, value="two")
        cache.put(key=3, value="three")  # This should evict key 1
        cache.put(key=3, value="three")  # This should evict key 1
        cache.put(key=3, value="three")  # This should evict key 1
        cache.put(key=3, value="three")  # This should evict key 1
        self.assertIsNone(
            cache.get(key=1), msg="Failed to evict the least recently used key"
        )
        self.assertEqual(
            cache.get(key=2), "two", msg="Failed to retrieve key '2' after eviction"
        )
        self.assertEqual(
            cache.get(key=3), "three", msg="Failed to retrieve newly added key '3'"
        )

    def test_update_existing_key(self):
        cache = LFUCache(capacity=2)
        cache.put(key=1, value="one")
        cache.put(key=1, value="ONE")  # Update the value for key 1
        self.assertEqual(
            cache.get(key=1),
            "ONE",
            msg="Failed to update the value for an existing key",
        )

    def test_evict_order(self):
        cache = LFUCache(capacity=3)
        cache.put(key=1, value="one")
        cache.put(key=2, value=[2, 2])
        cache.put(key="three", value=3.0)
        cache.get(key=1)  # Access key 1 so it becomes the most recently used
        cache.put(
            key=4.0, value="four"
        )  # This should evict key 2, as it is the least recently used
        self.assertEqual(
            cache.get(key=1),
            "one",
            msg="Failed to retrieve key '1' after multiple operations",
        )
        self.assertIsNone(
            cache.get(key=2), msg="Expected key '2' to be evicted but it was not"
        )
        self.assertEqual(
            cache.get(key="three"), 3.0, msg="Failed to retrieve key 'three'"
        )
        self.assertEqual(
            cache.get(key=4.0),
            "four",
            msg="Failed to retrieve newly added key '4.0'",
        )

    def test_overwrite_value(self):
        cache = LFUCache(capacity=2)
        cache.put(key=1, value="one")
        cache.put(key=2, value="two")
        cache.put(key=1, value="ONE")  # Update value for key 1
        self.assertEqual(
            cache.get(key=1),
            "ONE",
            msg="Failed to overwrite the value for an existing key",
        )
        self.assertEqual(
            cache.get(key=2),
            "two",
            msg="Failed to retrieve key '2' after overwriting key '1'",
        )

    def test_cache_size(self):
        cache = LFUCache(capacity=1)
        cache.put(key="a", value="A")
        cache.put(key="b", value="B")  # This should evict key 'a'
        self.assertIsNone(
            cache.get(key="a"),
            msg="Failed to evict the key 'a' when cache size exceeded",
        )
        self.assertEqual(
            cache.get(key="b"),
            "B",
            msg="Failed to retrieve key 'b' after evicting key 'a'",
        )

    def test_non_hashable_key(self):
        cache = LFUCache(capacity=5)
        with self.assertRaises(TypeError):
            cache.put(key=[1, 2], value="A")

    def test_decorator_caching(self):
        @LFUCache(capacity=2)
        def add(x, y):
            return x + y

        # First call, result should be computed and cached
        self.assertEqual(
            first=add(1, 2), second=3, msg="Failed to cache result of add(1, 2)"
        )
        # Second call with same arguments, result should be retrieved from cache
        self.assertEqual(
            first=add(1, 2),
            second=3,
            msg="Failed to retrieve cached result of add(1, 2)",
        )
        # New call with different arguments, new result should be computed and cached
        self.assertEqual(
            first=add(2, 3), second=5, msg="Failed to cache result of add(2, 3)"
        )
        # First cached result should still be valid
        self.assertEqual(
            first=add(1, 2),
            second=3,
            msg="Failed to retrieve still-valid cached result of add(1, 2)",
        )
        # This new call should evict the oldest cache entry (for add(1, 2))
        self.assertEqual(
            first=add(3, 4), second=7, msg="Failed to cache result of add(3, 4)"
        )
        # Original add(1, 2) should now be evicted
        self.assertEqual(
            first=add(1, 2),
            second=3,
            msg="Failed to recompute result of add(1, 2) after eviction",
        )

    def test_overflow_identical_timestamp_and_frequencies(self):
        # create cache
        cache = LFUCache(capacity=2)

        # Same timestamp, same freq
        target_timestamp = time.time()
        target_frequency = 1
        for key in ["a", "b", "c"]:
            cache._cache_strategy.timestamps[key] = target_timestamp
            cache._cache_strategy.frequency_dict[key] = target_frequency
            cache.cache[key] = key.upper()

        # Assert that eviction handles cache
        self.assertEqual(
            first=3, second=len(cache.cache), msg="There should be 3 items in the cache"
        )
        cache._cache_strategy.evict(cache=cache)
        self.assertEqual(
            first=2,
            second=len(cache.cache),
            msg="There should be 2 items in the cache after evicting the last one",
        )

    def test_decorator_with_non_hashable_key(self):
        @LFUCache(capacity=2)
        def join_lists(a, b):
            return a + b

        with self.assertRaises(TypeError):
            # Attempt to use lists (non-hashable) as keys
            self.assertEqual(
                first=join_lists([1], [2]),
                second=[1, 2],
                msg="Failed to compute join_lists([1], [2]) with non-hashable keys",
            )
            self.assertEqual(
                first=join_lists([1], [2]),
                second=[1, 2],
                msg="Failed to compute join_lists([1], [2]) with non-hashable keys",
            )


if __name__ == "__main__":
    unittest.main()
