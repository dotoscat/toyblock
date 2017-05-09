========
TOYBLOCK
========

Toyblock is yet another entity component system written in pure Python
being fast as possible.

Installation
------------

::

    pip install toyblock

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

	entity = toyblock.Entity(A(), B()) #The order does not matter here
			
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

Pool
----

Toyblock provides you a Pool. A Pool helps you to manage large groups of entities
(such bullets or enemies) and caches them for speed. Actually this is an experimental feature.

::

	a_pool = toyblock.Pool(1000, (B, A)) # A pool of 1000 entities with A and B component
	a_entity = a_pool.get() # Get an avaliable entity
    a_pool.free(a_entity)
