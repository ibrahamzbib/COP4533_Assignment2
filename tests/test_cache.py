import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cache_sim import simulate_fifo, simulate_lru, simulate_optff


class TestFIFO(unittest.TestCase):
    def test_hit_not_counted_as_miss(self):
        # item already in cache should not increment miss count
        self.assertEqual(simulate_fifo([1,2,3,1], 3), 3)

    def test_evicts_oldest_inserted(self):
        # cache: {1,2,3}, next miss should evict 1 (inserted first)
        self.assertEqual(simulate_fifo([1,2,3,4], 3), 4)


class TestLRU(unittest.TestCase):
    def test_hit_not_counted_as_miss(self):
        self.assertEqual(simulate_lru([1,2,3,1], 3), 3)

    def test_evicts_least_recently_used(self):
        # access 1 again before eviction — LRU should evict 2, not 1
        # cache after [1,2,3]: {1,2,3}. access 1 , LRU is now 2. insert 4 = evict 2
        self.assertEqual(simulate_lru([1,2,3,1,4], 3), 4)


class TestOPTFF(unittest.TestCase):
    def test_hit_not_counted_as_miss(self):
        self.assertEqual(simulate_optff([1,2,3,1], 3), 3)

    def test_evicts_farthest_next_use(self):
        # cache: {1,2,3}. next uses: 1 : index 4, 2 : index 5, 3: never. evict 3
        self.assertEqual(simulate_optff([1,2,3,4,1,2], 3), 4)

    def test_evicts_never_used_again(self):
        # item with no future use should be evicted over one that is needed soon
        # cache: {1,2}, 1 never appears again, 2 appears at index 3. evict 1
        self.assertEqual(simulate_optff([1,2,3,2], 2), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)