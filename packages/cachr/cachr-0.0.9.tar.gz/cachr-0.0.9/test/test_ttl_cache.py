import unittest
import time

from src.cachr.caches import TTLCache


class TestTTLEvictionPolicy(unittest.TestCase):
    def test_ttl_expiration(self):
        # Create a TTL cache with a 0.5-second expiration time
        ttl_cache = TTLCache(capacity=3, ttl_seconds=0.5)

        ttl_cache.put("a", 1)
        time.sleep(0.3)
        self.assertEqual(
            ttl_cache.get("a"),
            1,
            msg="Failed to retrieve value '1' for key 'a' before expiration",
        )

        time.sleep(0.3)
        self.assertIsNone(
            ttl_cache.get("a"), msg="Expected None after expiration of key 'a'"
        )

    def test_ttl_eviction_after_insert(self):
        # Create a TTL cache with a 0.5-second expiration time
        ttl_cache = TTLCache(capacity=2, ttl_seconds=0.5)

        ttl_cache.put("a", 1)
        ttl_cache.put("b", 2)
        time.sleep(0.6)  # Both "a" and "b" should expire

        ttl_cache.put("c", 3)
        self.assertIsNone(
            ttl_cache.get("a"), msg="Key 'a' should have expired and be None"
        )
        self.assertIsNone(
            ttl_cache.get("b"), msg="Key 'b' should have expired and be None"
        )
        self.assertEqual(
            ttl_cache.get("c"), 3, msg="Failed to retrieve value '3' for key 'c'"
        )

    def test_ttl_retains_valid_entries(self):
        # Create a TTL cache with a 0.5-second expiration time
        ttl_cache = TTLCache(capacity=2, ttl_seconds=0.5)

        ttl_cache.put("a", 1)
        ttl_cache.put("b", 2)
        time.sleep(0.3)
        ttl_cache.put(
            "c", 3
        )  # Should evict "a" as "b" is more recently used and not expired

        self.assertIsNone(ttl_cache.get("a"), msg="Key 'a' should have been evicted")
        self.assertEqual(
            ttl_cache.get("b"),
            2,
            msg="Key 'b' should be retained as it is still valid",
        )
        self.assertEqual(
            ttl_cache.get("c"), 3, msg="Failed to retrieve value '3' for key 'c'"
        )

    def test_ttl_expiration_for_recently_accessed(self):
        # Create a TTL cache with a 0.5-second expiration time
        ttl_cache = TTLCache(capacity=2, ttl_seconds=0.5)

        ttl_cache.put("a", 1)
        time.sleep(0.3)
        ttl_cache.get("a")  # Accessing "a" should not reset its expiration time

        time.sleep(0.3)
        self.assertIsNone(
            ttl_cache.get("a"),
            msg="Key 'a' should not have expired as it was accessed recently",
        )

    def test_ttl_mixed_operations(self):
        # Create a TTL cache with a 0.4-second expiration time
        ttl_cache = TTLCache(capacity=3, ttl_seconds=0.4)

        ttl_cache.put("a", 1)
        time.sleep(0.2)
        ttl_cache.put("b", 2)
        ttl_cache.put("c", 3)

        self.assertEqual(ttl_cache.get("a"), 1, msg="Key 'a' should still be available")

        time.sleep(0.3)
        self.assertIsNone(
            ttl_cache.get("a"), msg="Key 'a' should have expired after 0.4 seconds"
        )
        self.assertEqual(ttl_cache.get("b"), 2, msg="Key 'b' should still be available")

        ttl_cache.put("d", 4)
        ttl_cache.put("e", 4)  # Should evict "c" as it is the least recently used
        self.assertIsNone(ttl_cache.get("c"), msg="Key 'c' should have been evicted")
        self.assertEqual(
            ttl_cache.get("b"),
            2,
            msg="Key 'b' should still be available after adding 'd'",
        )
        self.assertEqual(
            ttl_cache.get("d"), 4, msg="Failed to retrieve value '4' for key 'd'"
        )


if __name__ == "__main__":
    unittest.main()
