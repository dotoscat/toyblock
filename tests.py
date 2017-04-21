import unittest
from toyblock import Pool, Entity

class A(object):
    def __init__(self):
        self.x = 0

class B(object):
    def __init__(self):
        self.x = 0

class C(object):
    def __init__(self):
        self.x = 0

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

class EntityTest(unittest.TestCase):
    def setUp(self):
        self.a = A()
        self.b = B()
        self.c = C()

    def test_add_component(self):
        entity = Entity()
        self.assertTrue(entity.add_component(A, self.a))

    def test_get_component(self):
        entity = Entity()
        self.assertTrue(entity.add_component(A, self.a))
        self.assertEqual(entity.get_component(A), self.a)
