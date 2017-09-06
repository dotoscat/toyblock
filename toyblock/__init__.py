# Copyright (C) 2017  Oscar Triano 'dotoscat' <dotoscat (at) gmail (dot) com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ["Pool", "Entity", "System"]

from collections import deque
from weakref import proxy
import warnings
try:
    from itertools import zip_longest
except:
    print("Use Python3!")
    from itertools import izip_longest as zip_longest

class EntityError(Exception):
    pass

class EntityComponentExistsError(EntityError):
    """This exception is only raised when a type of a component already
    exists as key on the entity.
    """
    def __init__(self, class_, entity):
        self.class_ = class_
        self.entity = entity

    def __str__(self):
        return "Component {} already exists in entity {}".format(self.class_, self.entity)

class EntityBelongsToPoolError(EntityError):
    """This is raised when the entity belongs to a Pool"""
    def __init__(self, entity):
        self.entity = entity

    def __str__(self):
        return "{} belongs to {}".format(self.entity, self.entity.pool)

class Entity(object):
    """
        Entity use the instances as components and their types as key.

        :param instances: Instances of any type.
        :param pool: Pool which this entity belongs to.
        :type pool: Pool or None
        :returns: A new Entity instance.
        :raises EntityComponentExistsError: If the type of instance is already used
    """
    __slots__ = ('_components', '_pool', '_systems')

    def __init__(self, *instances, pool=None):
        self._pool = pool
        self._components = {}
        add_component = self.add_component
        for instance in instances:
            add_component(instance)
        self._systems = deque()

    @property
    def pool(self):
        """You can check whether this entity belongs to a Pool. Read only."""
        return self._pool

    def _add_system(self, system):
        self._systems.append(system)

    def _remove_system(self, system):
        self._systems.remove(system)

    def _add_component(self, instance):
        type_ = type(instance)
        if type_ in self._components:
            raise EntityComponentExistsError(type_, self)
        self._components[type_] = instance

    def add_component(self, instance):
        """Add a component instance to this entity.

            :param instance instance:

            :raises EntityBelongsToPoolError: If this entity belongs to a Pool.
            :raises EntityComponentExistsError: If the type of instance is already used.
        """
        if self._pool is not None: raise EntityBelongsToPoolError(self)
        self._add_component(instance)

    def __getitem__(self, type_):
        """
            This is a convenient, less verbose, way to get a component
            and manipulate it.

            :param type_: Type of the instance
            :returns: Instance of *type_* if exists, otherwise *None*

            .. code-block:: python

                entity = Entity(Body(), Graphic())
                entity[Body].x = 7.
        """
        return self._components.get(type_)

    def get_component(self, type_):
        """
            .. deprecated:: 2.0.0
                Use :func:`__getitem__` instead.
        """
        warnings.warn("Use __getitem__ instead", DeprecationWarning, stacklevel=2)
        return self.__getitem__(type_)

    def del_component(self, type_):
        """
        Delete a specific component. Remove and returns the instance of *type_*.

        :param type_: A instance of *type_*
        :returns: The removed instance from this entity,
            or None if not exists.
        """
        if self._pool is not None: raise EntityBelongsToPoolError(self)
        return self._components.pop(type_, None)

    def set_component(self, type_, dict_):
        """
        Convenient method for setting attributes to a component from a dict.
        
        :param type_: A instance of *type_*.
        :param dict_: Dict to use for the component.
        
        .. code-block:: python
            
            player.set_component[Body, {'x': 32., 'y': 64.}]
            
        """
        component = self[type_]
        for key in dict_:
            setattr(component, key, dict_[key])

    def free(self):
        """
        Make this entity avaliable from its `Pool`. The entity it is
        removed from the systems that are asigned to :class:`Pool`.
        
        If this entity does not have a Pool then this method does nothing. 
        """
        if self._pool is None: return
        self._pool._free(self)

    def __contains__(self, item):
        if isinstance(item, System): return item in self._systems
        return item in self._components

class System(object):
    """
    A bunch of entities by themselves are useless. You must add them
    to a system, then interact with them.

    In the constructor is mandatory pass a callable. You can pass other arguments
    that will passed to the callable for each entity.

    .. note::

        The callable signature is (system, entity, *args, **kwargs).

    After you add at least one entity you can run the system calling it*
    """
    def __init__(self, callable_):
        if not callable(callable_):
            raise TypeError("Pass a callable object to the constructor")
        self._callable_ = callable_
        self._entities = deque()
        self._locked = False
        self._entities_removed = deque()
        self._entities_added = deque()

        #Remap some methods
        self._entities_added_append = self._entities_added.append
        self._entities_append = self._entities.append
        self._entities_removed_append = self._entities_removed.append
        self._entities_remove = self._entities.remove

    @property
    def entities(self):
        return self._entities

    def add_entity(self, entity):
        if self in entity: return
        if self._locked:
            self._entities_added_append(entity)
        else:
            self._entities_append(entity)
            entity._add_system(proxy(self))

    def remove_entity(self, entity):
        if self not in entity: return
        if self._locked:
            self._entities_removed_append(entity)
        else:
            self._entities_remove(entity)
            entity._remove_system(self)

    def __call__(self, *args, **kwargs):
        """Run the system. In the callable is perfectly safe add or remove entities
        to the system.
        """
        if self._locked: return
        entities = self._entities
        callable_ = self._callable_
        self._locked = True
        for entity in entities:
            callable_(self, entity, *args, **kwargs)
        self._locked = False
        entities_removed = self._entities_removed
        entities_added = self._entities_added
        while len(entities_removed):
            entity = entities_removed.pop()
            entities.remove(entity)
            entity._remove_system(self)
        while len(entities_added):
            entity = entities_added.pop()
            entities.append(entity)
            entity._add_system(proxy(self))

    def __contains__(self, entity):
        return self in entity

    def __len__(self):
        return len(self._entities)

def system(callable_):
    """This is a decorator for System.

    Example of use:

    @toyblock.system
    def physics(system, entity, dt):
        # do your things here

    physics.add_entity(some_entity)

    # ...

    physics(get_delta_time())
    """
    if not callable(callable_):
        raise TypeError("Use this as a DECORATOR")
    return System(callable_)

class Pool(object):
    """
    A Pool is used for cache created objects and increase performance.
    """
    def __init__(self, maxlen, types, args_list=(), kwargs_list=(), systems=None):
        """
        Parameters:

        maxlen: Number of entities (Number).
        types: Types for the entities (Sequence) with the classes.
        args_for_types: Tuples of args for the instances of types
        [(args, kwargs), ...]

        Example of use

        args = ((1, 2),)
        kwargs = (None, {"a": 7})
        pool = toyblock.Pool(10, (A, B, C), args, kwargs)
        """
        self._init = None
        self._clean = None
        self._systems = systems
        self._avaliable = deque(maxlen=maxlen)
        avaliable_append = self._avaliable.append
        EMPTY_TUPLE = ()
        EMPTY_DICT = {}
        for i in range(maxlen):
            entity = Entity(pool=proxy(self))
            entity_add_component = entity._add_component
            for type_, type_args, type_kwargs in zip_longest(types, args_list, kwargs_list):
                args = EMPTY_TUPLE if type_args is None else type_args
                kwargs = EMPTY_DICT if type_kwargs is None else type_kwargs
                instance = type_(*args, **kwargs)
                entity_add_component(instance)
            avaliable_append(entity)
        self._used = deque(maxlen=maxlen)

        #Remap methods to be used directly
        self._avaliable_pop = self._avaliable.pop
        self._used_append = self._used.append
        self._used_remove = self._used.remove
        self._avaliable_append = self._avaliable.append

    def init(self, init):
        if not callable(init):
            raise TypeError("Use this as a DECORATOR")
        self._init = init
        return init

    def clean(self, clean):
        if not callable(clean):
            raise TypeError("Use this as a DECORATOR")
        self._clean = clean
        return clean

    def get(self):
        """Return a free Entity if avaliable, None otherwise.
        """
        if not self._avaliable:
            return None
        entity = self._avaliable_pop()
        self._used_append(entity)
        if self._init is not None:
            self._init(entity)
        if self._systems is None:
            return entity
        for system in self._systems:
            system.add_entity(entity)
        return entity

    def free(self, entity):
        warnings.warn("Use Entity.free() instead", DeprecationWarning, stacklevel=2)
        self._free(entity)

    def free_all(self):
        while len(self._used):
            self._free(self._used[0])

    def _free(self, entity):
        """Mark the instance to be avaliable."""
        if entity not in self._used: return
        self._used.remove(entity)
        self._avaliable.append(entity)
        if self._clean is not None:
            self._clean(entity)
        if self._systems is None: return
        for system in self._systems:
            system.remove_entity(entity)
