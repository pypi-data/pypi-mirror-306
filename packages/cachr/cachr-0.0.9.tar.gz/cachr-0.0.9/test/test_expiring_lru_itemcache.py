import time
import unittest

from src.cachr.caches import TTLCache


class TestExpiringLRUCache(unittest.TestCase):
    def test_expiration(self):
        cache = TTLCache(capacity=2, ttl_seconds=0.5)
        cache.put("a", 1)
        time.sleep(0.3)
        self.assertEqual(
            cache.get("a"),
            1,
            msg="Failed to retrieve value '1' for key 'a' before expiration",
        )
        time.sleep(0.3)
        self.assertIsNone(
            cache.get("a"), msg="Expected None after expiration of key 'a'"
        )

    def test_cache_eviction_after_expiration(self):
        cache = TTLCache(capacity=2, ttl_seconds=0.5)
        cache.put("a", 1)
        cache.put("b", 2)
        time.sleep(0.6)  # Both "a" and "b" should expire
        cache.put("c", 3)  # Should not evict "a" or "b" since they are expired
        self.assertIsNone(cache.get("a"), msg="Key 'a' should have expired and be None")
        self.assertIsNone(cache.get("b"), msg="Key 'b' should have expired and be None")
        self.assertEqual(
            cache.get("c"), 3, msg="Failed to retrieve value '3' for key 'c'"
        )

    def test_cache_retains_valid_entries(self):
        cache = TTLCache(capacity=2, ttl_seconds=0.5)
        cache.put("a", 1)
        cache.put("b", 2)
        time.sleep(0.3)
        cache.put(
            "c", 3
        )  # Should evict "a" as "b" is more recently used and not expired
        self.assertIsNone(cache.get("a"), msg="Key 'a' should have been evicted")
        self.assertEqual(
            cache.get("b"), 2, msg="Key 'b' should be retained as it is still valid"
        )
        self.assertEqual(
            cache.get("c"), 3, msg="Failed to retrieve value '3' for key 'c'"
        )

    def test_no_expiration_for_recently_accessed(self):
        cache = TTLCache(capacity=2, ttl_seconds=0.5)
        cache.put("a", 1)
        time.sleep(0.3)
        cache.get("a")  # Accessing "a" should not refresh its expiration time
        time.sleep(0.3)
        self.assertIsNone(
            cache.get("a"),
            msg="Key 'a' should have expired despice being accessed recently",
        )

    def test_mixed_operations_with_expiration(self):
        cache = TTLCache(capacity=3, ttl_seconds=0.4)
        cache.put("a", 1)

        time.sleep(0.2)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 1, msg="Key 'a' should still be available")
        time.sleep(0.3)
        self.assertIsNone(
            cache.get("a"), msg="Key 'a' should have expired after 0.4 seconds"
        )
        self.assertEqual(cache.get("b"), 2, msg="Key 'b' should still be available")
        cache.put("d", 4)
        cache.put("e", 4)  # Should evict "c" as it is the least recently used
        self.assertIsNone(cache.get("c"), msg="Key 'c' should have been evicted")
        self.assertEqual(
            cache.get("b"),
            2,
            msg="Key 'b' should still be available after adding 'd'",
        )
        self.assertEqual(
            cache.get("d"), 4, msg="Failed to retrieve value '4' for key 'd'"
        )
        time.sleep(0.4)

    def test_decorator_caching(self):
        @TTLCache(ttl_seconds=0.1, capacity=2)
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
        time.sleep(0.3)
        add.refresh()
        self.assertEqual(
            first=0,
            second=add.cache_info().get("currsize"),
            msg="All items in cache should have expired by now",
        )


if __name__ == "__main__":
    unittest.main()
