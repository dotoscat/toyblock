import unittest
from toyblock import Pool

class A:
    pass

class B:
    pass

class PoolTest(unittest.TestCase):
    def test_get(self):
        unique = Pool(A, 1)
        instance = unique.get()
        self.assertEqual(isinstance(instance, A), True)

    def test_empty(self):
        empty = Pool(A, 0)
        self.assertEqual(empty.get(), None)

    def test_free(self):
        pool = Pool(A, 3)
        instance = pool.get()
        self.assertTrue(pool.free(instance))
