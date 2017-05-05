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
			self.x = 0.1
			
	class B:
		def __init__(self):
			self.b = 0	

	entity = toyblock.Entity()
	#We add a component using the type as first argument and an instance of that type
	entity.add_component(A, A())
	entity.add_component(B, B()) #The order does not matter here
			
	def multiply_with_time(entity, b, a, time):
		"""This will be the callable for our system."""
		b.b = a.x*2*time()
		
	main_system = toyblock.System((B, A), multiply_with_time, time) #Here the order DOES matter
	main_system.add_entity(entity)
	main_system.run() #Run the system
	# This is the basics

Pool
----

Toyblock provides you a Pool. A Pool helps you to manage large groups of entities
(such bullets or enemies) and caches them for speed

::

	a_pool = toyblock.Pool(1000, (B, A)) # A pool of 1000 entities with A and B component
	a_entity = a_pool.get() # Get an avaliable entity