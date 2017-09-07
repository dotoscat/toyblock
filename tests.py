import unittest
import toyblock
from toyblock import Entity, Pool, System

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
        self.assertEqual(instance.pool, unique)
        self.assertEqual(isinstance(instance, Entity), True)

    def test2_empty(self):
        empty = Pool(0, (A,))
        self.assertEqual(empty.get(), None)

    def test3_free(self):
        pool = Pool(3, (A,))
        instance = pool.get()
        pool.free(instance)

    def test5_var_args(self):
        args = (None, (1,), None)
        kwargs = (None, {'d': 7})
        pool = Pool(1000, (A, D, C), args, kwargs)
        one = pool.get()
        one_d = one[D]
        self.assertEqual(one_d.v, 1)
        self.assertEqual(one_d.d, 7)
        self.assertEqual(one[A].a, 0)

    def test6_single_args(self):
        args = (
            ((1,), None),
        )

        pool = Pool(10, (D, A), args)

    def test7_system_management(self):

        @System
        def system_a(system, entity):
            print("I am A", entity, entity.pool)

        @System
        def system_b(system, entity):
            print("I am B", entity, entity.pool)

        pool = toyblock.Pool(3, (A, B), systems=(system_a, system_b))
        system_a()
        system_b()
        uno = pool.get()
        system_a()
        system_b()
        uno.free()
        system_a()
        system_b()

    def test8_entity_init(self):

        class One:
            def __init__(self):
                self.a = 0
                self.b = 0

        @System
        def system(system, entity):
            one = entity[One]
            self.assertEqual(one.a, 7)
            self.assertEqual(one.b, 12)

        pool = toyblock.Pool(10, (One,), systems=(system,))

        @pool.init
        def init_one(entity):
            one = entity[One]
            one.a = 7
            one.b = 12

        pool.get()
        system()

    def test9_entity_clean(self):

        class Accumulator:
            def __init__(self):
                self.step = 0

        @System
        def accumulate(system, entity):
            accu = entity[Accumulator]
            accu.step += 1

        pool = toyblock.Pool(4, (Accumulator,), systems=(accumulate,))
        @pool.init
        def init(entity):
            accu = entity[Accumulator]
            accu.step += 1
        @pool.clean
        def clean(entity):
            accu = entity[Accumulator]
            accu.step += 1

        entity = pool.get()
        accumulate()
        entity.free()
        accu = entity[Accumulator]
        self.assertEqual(accu.step, 3)

    def test10_free_all(self):
        class Times:
            times = 0

        pool = toyblock.Pool(10, (A,))

        @pool.clean
        def clean_object(entity):
            Times.times += 1

        for i in range(10): pool.get()
        pool.free_all()
        self.assertEqual(Times.times, 10)

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
        self.assertEqual(self.entity[A], self.a)

    def test3_EntityComponentExistsError(self):
        self.entity.add_component(self.a)
        self.assertRaises(toyblock.EntityComponentExistsError,
                          self.entity.add_component, A())

    def test4_entity_creation_with_components(self):
        entity = Entity(self.a, self.b)
        self.assertEqual(entity[A], self.a)
        self.assertEqual(entity[B], self.b)

    def test5_set_component(self):
        class G(object):
            def __init__(self):
                self.a = 0
                self.b = 0
                self.c = 0

        entity = Entity()
        entity.add_component(G())
        entity.set(G, {"a": 1, "b": 2, "c": 3})
        g = entity[G]
        self.assertEqual(g.a, 1)
        self.assertEqual(g.b, 2)
        self.assertEqual(g.c, 3)

class SystemTest(unittest.TestCase):
    def setUp(self):

        @System
        def system(system, entity, random):
            self.assertEqual(random, "Hello!")
            a = entity[A]
            b = entity[B]
            b.b += 1
            a.a = b.b*2
            a.system = system

        self.system = system
        self.hello = "Hello!"

    def _add_entities_to_system(self):
        for entity in self.entities:
            entity.add_component(A())
            entity.add_component(B())
            self.system.add_entity(entity)

    def test1_add_entities(self):
        self.entities = [Entity() for i in range(100)]
        self._add_entities_to_system()
        self.assertEqual(len(self.system.entities), 100)

    def test2_run_system(self):
        entity = Entity()
        entity.add_component(A())
        entity.add_component(B())
        self.system.add_entity(entity)
        self.system(self.hello)
        self.assertEqual(entity[A].a, 2)
        self.assertEqual(entity[A].system, self.system)

    def test3_manipulate_entities(self):
        one = Entity()
        two = Entity()

        @System
        def system(system, entity, two):
            system.remove_entity(entity)
            system.add_entity(two)
            self.assertFalse(two in entity)

        system.add_entity(one)
        system(two)
        self.assertFalse(one in system)
        self.assertTrue(two in system)

    def test4_run_varargs(self):

        i = 2

        @System
        def system(system, entity, number):
            a = entity[A]
            a.a += number

        entity = Entity(A())
        system.add_entity(entity)
        system(i)
        a = entity[A]
        self.assertEqual(a.a, 2)

    def test5_decorator(self):

        @System
        def print_entity(system, entity):
            print(entity)

        print_entity.add_entity(Entity())
        print_entity()
