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

class D(object):
    def __init__(self, v, d=0):
        self.v = v
        self.d = d

class PoolTest(unittest.TestCase):
    def test1_get(self):
        unique = Pool(2, (A,))
        instance = unique.get()
        self.assertEqual(isinstance(instance, Entity), True)

    def test2_empty(self):
        empty = Pool(0, (A,))
        self.assertEqual(empty.get(), None)

    def test3_free(self):
        pool = Pool(3, (A,))
        instance = pool.get()
        self.assertTrue(pool.free(instance))
        
    def test5_var_args(self):
        
        args = (
            None,
            ((1,), {'d': 7}),
            None
        )
        
        pool = Pool(1000, (A, D, C), args)
        one = pool.get()
        one_d = one.get_component(D)
        self.assertEqual(one_d.v, 1)
        self.assertEqual(one_d.d, 7)
        self.assertEqual(one.get_component(A).a, 0)

    def test6_single_args(self):
        args = (
            ((1,), None),
        )
        
        pool = Pool(10, (D, A), args)
        

class EntityTest(unittest.TestCase):
    def setUp(self):
        self.a = A()
        self.b = B()
        self.c = C()
        self.entity = Entity()

    def test1_add_component(self):
        self.entity.add_component(self.a)
        
    def test2_get_component(self):
        self.entity.add_component(self.a)
        self.assertEqual(self.entity.get_component(A), self.a)

    def test3_EntityComponentExistsError(self):
        self.entity.add_component(self.a)
        self.assertRaises(toyblock.entity.EntityComponentExistsError,
                          self.entity.add_component, A())
    
    def test4_entity_creation_with_components(self):
        entity = Entity(self.a, self.b)
        self.assertEqual(entity.get_component(A), self.a)
        self.assertEqual(entity.get_component(B), self.b)

class SystemTest(unittest.TestCase):
    def setUp(self):

        def update(system, entity, random):
            self.assertEqual(random, "Hello!")
            a = entity.get_component(A)
            b = entity.get_component(B)
            b.b += 1
            a.a = b.b*2
            a.system = system
        
        self.hello = "Hello!"        
        self.system = System(update)
        
    def _add_entities_to_system(self):
        for entity in self.entities:
            entity.add_component(A())
            entity.add_component(B())
            self.system.add_entity(entity)
        
    def test1_add_entities(self):
        self.entities = [Entity() for i in range(100)]
        self._add_entities_to_system()
        self.assertEqual(len(self.system._entities), 100)

    def test2_run_system(self):
        entity = Entity()
        entity.add_component(A())
        entity.add_component(B())
        self.system.add_entity(entity)
        self.system(self.hello)
        self.assertEqual(entity.get_component(A).a, 2)
        self.assertEqual(entity.get_component(A).system, self.system)
        
    def test3_manipulate_entities(self):
        one = Entity()
        two = Entity()
    
        def do_something(system, entity, two):
            system.remove_entity(entity)
            system.add_entity(two)
            self.assertFalse(two in entity)
    
        system = System(do_something)
        system.add_entity(one)
        system(two)
        self.assertFalse(one in system)
        self.assertTrue(two in system)
        
    def test4_run_varargs(self):
        
        i = 2
        
        def update(system, entity, number):
            a = entity.get_component(A)
            a.a += number
            
        system = System(update)
        entity = Entity(A())
        system.add_entity(entity)
        system(i)
        a = entity.get_component(A)
        self.assertEqual(a.a, 2)
