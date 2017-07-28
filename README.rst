==============
TOYBLOCK 2.0.0
==============

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
- *toyblock.Entity.get_component(_type_of_instance_)* **Deprecated**
- *toyblock.Entity[_type_of_instance_]*
- *toyblock.Entity.del_component(_type_of_instance_)*
- *toyblock.Entity.free()*
- *toyblock.Entity.pool*

*toyblock.System*
.................

Define the system behavior with *callable_*.

*callable_* signature is *(system, entity, *args, **kwargs)*

First you add entities to a system, then you call the system,
passing any number of variables to the callable.

- *toyblock.System(callable_)*
- *toyblock.System.add_entity(entity)*
- *toyblock.System.remove_entity(entity)*
- *toyblock.System.__call__(\*args, \*\*kwargs)*
- *toyblock.System.__contains__(entity)*
- *toyblock.System.__len__()*

@toyblock.system
++++++++++++++++

Toyblock provides you a convenient decorator for building a System

::

    @toyblock.system
    def a_system(system, entity):
        # do stuff

    a_system.add_entity(a_entity)
    a_system() # Run the system

*toyblock.Pool*
...............

A pool of entities that helps you to cache the entities and manage them automatically.
You provide args and kwargs for each one of the entity's component. You can add
systems which entities will be added or removed from them automatically when an
entity is returned from its or freed.

- *toyblock.Pool(number_of_entities, [type_list], [args_list], systems=[system_list])*
- *toyblock.Pool.get()*
- *toyblock.Pool.free(_entity_)* **Deprecated**
- *toyblock.Pool.init(callable_)*

Pool example
++++++++++++

::

    args = ((32, 32), (640,))
    kwargs = (None, None, {"visible": False})
    my_systems = (physics, graphics)

    my_pool = toyblock.Pool(100, (Body, Jump, Graphics), args, kwargs, my_systems)
    # You can omit 'args' and 'kwargs' if don't need any.
    a_entity = my_pool.get() # Automatically the entity will be added to the systems
    # ... More stuff
    a_entity.free() # Avaliable again from its pool and automatically removed from the systems

@Pool.init
++++++++++

Each time when Pool's get is called this function will be called for the returned entity.

::

    a_pool = toyblock.Pool(4, (Body, Graphic))
    @a_pool.init
    def init_car(entity):
        body = entity[Body]
        body.vel = 0.0

@Pool.clean
+++++++++++

This decorator is called when an entity is freed.

::

    a_pool = toyblock.Pool(4, (Body, Graphic))
    @a_pool.clean
    def reset_car(entity):
        entity[Damage].damage = 0

Toyblock example usage
----------------------

::

    from time import time
    import toyblock

    #Our components for an entity 'bullet'
    class Body:
        def __init__(self):
            self.x = 0.0
            self.y = 0.0
            self.vel_x = 0.0
            self.vel_y = 0.0

        def update(dt):
            # update

    class Collision:
        def __init__(self, radius):
            self.x = 0.0
            self.y = 0.0
            self.radius = radius
        def collides_with(another):
            # return true or false
        def update(x, y):
            # update

    class Graphic:
        def __init__(self, sprite, animation):
            self.sprite = sprite
            self.animation = animation

        def update_position(x, y):
            self.sprite.set_position(x, y)

    @toyblock.system
    def physics(system, entity, dt):
        body = entity[Body]
        body.update(dt)

    @toyblock.system
    def collision(system, entity, hero):
        body = entity[Body]
        collision = entity[Collision]
        hero_collision = hero[Collision]
        if collision.collides_with(hero_collision):
            entity.free()

    @toyblock.system
    def draw(system, entity, canvas):
        body = entity[Body]
        graphic = entity[Graphic]
        graphic.update_position(body.x, body.y)
        canvas.draw(graphic)

    bullets = Pool(100, (Body, Graphic), systems=(physics, collision, draw))
    @bullet.init
    def bullet_init(entity):
        entity[Graphic].animation.step = 0

    # .... More setup

    while playing:
        # Spawn bullets and move hero
        physics(time())
        collision(hero)
        draw(canvas)

Run tests
---------

At the project's root

::

    python -m unittest

License
-------

..  image:: https://www.gnu.org/graphics/lgplv3-147x51.png
    :alt: LGPL-3.0
