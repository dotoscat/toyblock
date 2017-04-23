import unittest
from toyblock import Pool, Entity, System

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

class SystemTest(unittest.TestCase):
    def setUp(self):

        def update(a, b):
            a.x += 1
            b.x = a.x*2
            #print(a.x, b.x)
        
        self.system = System(update, (A, B))
        self.entities = [Entity() for i in range(100)]

    def test1_add_entities(self):
        for entity in self.entities:
            self.assertTrue(entity.add_component(A, A()))
            self.assertTrue(entity.add_component(B, B()))
            self.assertTrue(self.system.add_entity(entity))
        self.assertEqual(len(self.system._entities), 10)
        for i in range(10):
            self.system.run()
        print(self.system._entities)

    def test2_run_system(self):
        print(self.system._entities)
        for i in range(10):
            self.system.run()

def esto(uno, dos):
    uno.x += 1
    dos.x += 1

class Ahuevo:
    def __init__(self):
        self.system = System(esto, (A, B))
        self.entities = [Entity() for i in range(10)]
        for i in self.entities:
            i.add_component(A, A())
            i.add_component(B, B())
            self.system.add_entity(i)
        
