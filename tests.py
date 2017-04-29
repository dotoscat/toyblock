import unittest
from toyblock import Pool, Entity, System
import toyblock.entity

class A(object):
    def __init__(self):
        self.a = 0

class B(object):
    def __init__(self):
        self.b = 0

class C(object):
    def __init__(self):
        self.c = 0

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
        self.entity = Entity()

    def test1_add_component(self):
        self.entity.add_component(A, self.a)
        
    def test2_get_component(self):
        self.entity.add_component(A, self.a)
        self.assertEqual(self.entity.get_component(A), self.a)

    def test3_EntityNoTypeError(self):
        self.assertRaises(toyblock.entity.EntityNoTypeError,
                          self.entity.add_component,
                          None, self.a)

    def test4_EntityNoInstanceError(self):
        self.assertRaises(toyblock.entity.EntityNoInstanceError,
                          self.entity.add_component,
                          A, self.b)

    def test5_EntityComponentExistsError(self):
        self.entity.add_component(A, self.a)
        self.assertRaises(toyblock.entity.EntityComponentExistsError,
                          self.entity.add_component,
                          A, A())

class SystemTest(unittest.TestCase):
    def setUp(self):

        def update(entity, b, a):
            b.b += 1
            a.a = b.b*2
        
        self.system = System(update, (B, A))
        self.entities = [Entity() for i in range(100)]

    def test1_add_entities(self):
        for entity in self.entities:
            entity.add_component(A, A())
            entity.add_component(B, B())
            self.system.add_entity(entity)
        self.assertEqual(len(self.system._entities), 100)

    def test2_run_system(self):
        self.test1_add_entities()
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
        
