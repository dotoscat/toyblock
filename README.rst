========
TOYBLOCK
========

..  image:: toyblock_logo.png
    :alt: TOYBLOCK

Toyblock is yet another entity component system written in pure Python
being fast as possible.

Installation
------------

::

    pip install toyblock

API
---

*toyblock.Entity*
.................

It's just a bag for components to be used with *toyblock.System*.

- *toyblock.Entity([_instance_, ...])*
- *toyblock.Entity.add_component(_instance_)*
- *toyblock.Entity.get_component(_type_of_instance_)*
- *toyblock.Entity.del_component(_type_of_instance_)*

*toyblock.Pool*
...............

A pool of entities that helps you to cache the entities and manage them.
Here you pass the classes or types for instanciate them and create the
entities. You can provide a list of arguments (args and kwargs) for the
instances.

- *toyblock.Pool(number_of_entities, ([_type_of_instance, ...]), [(tuple_args|None, dict_kwargs|None) | None, ...])*
- *toyblock.Pool.get()*
- *toyblock.Pool.free(_entity_)*

Pool example
++++++++++++

::

    arguments = (
        ((32, 32), {"visible": False}),
        (640, None),
        # You can omit arguments for the third class or just None
    )
    
    my_pool = toyblock.Pool(100, (Body, Jump, Graphics), arguments)
    # You can omit 'arguments' too if the classes do not need any.
    a_entity = my_pool.get()
    my_pool.free(a_entity)

Example usage
-------------

::

    from time import time
    import toyblock

    #Our components for the entity
    class A:
        def __init__(self):
            self.x = 1
            
    class B:
        def __init__(self):
            self.b = 0    

    entity = toyblock.Entity(A(), B()) #The order does not matter
            
    def multiply_with_time(system, entity, time):
        """This will be the callable for our system."""
        
        b = entity.get_component(B)
        a = entity.get_component(A)
        b.b = a.x*2*time()
        if b.b > 3:
            system.remove_entity(entity)
        
    main_system = toyblock.System(multiply_with_time, time)
    main_system.add_entity(entity)
    main_system.run() #Run the system

License
-------

..  image:: https://www.gnu.org/graphics/lgplv3-147x51.png
    :alt: LGPL-3.0
