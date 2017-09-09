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
    """This is raised when the entity belongs to a Pool."""
    def __init__(self, entity):
        self.entity = entity

    def __str__(self):
        return "{} belongs to {}".format(self.entity, self.entity.pool)

class Entity(object):
    """A bag where you group the components.
    
    Parameters:
        *instances (Any): Instances of any type
        pool (Pool or None): Pool which this entity belongs to.
        
    Returns:
        A new Entity instance.
        
    Raises:
        EntityComponentExistsError: If the type of a instance is already used.
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

        Parameters:
            instance (Any): An instance of any class.
        
        Raises:
            EntityBelongsToPoolError: If this entity belongs to a Pool.
            EntityComponentExistsError: If the type of instance is already used.
        """
        if self._pool is not None: raise EntityBelongsToPoolError(self)
        self._add_component(instance)

    def __getitem__(self, type_):
        """This is a convenient, less verbose, way to get a component
        and manipulate it.

        Parameters:
            type\_: Type of the instance
            
        Returns:
            Instance of *type_* if exists, otherwise *None*

        Example:
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
        """Delete a specific component. Remove and returns the instance of *type_*.

        Parameters:
            type\_: A instance of *type_*
        
        Returns:
            The removed instance from this entity, or None if not exists.
        """
        if self._pool is not None: raise EntityBelongsToPoolError(self)
        return self._components.pop(type_, None)

    def set(self, type_, dict_):
        """Convenient method for setting attributes to a component with a dict.
        
        Parameters:
            type\_: A instance of *type_*.
            dict\_: Dict to use for the component.
        
        Example:
            .. code-block:: python
            
                #  This is more easy
            
                player.set(Body, {'x': 32., 'y': 64.})
                
                #  than
                
                player[Body].x = 32.
                player[Body].y = 64.
                
        """
        component = self[type_]
        for key in dict_:
            setattr(component, key, dict_[key])

    def free(self):
        """
        Make this entity avaliable from its `Pool`. The entity it is
        removed from the systems that are asigned to :class:`Pool`. You
        can use this method inside a :class:`System` call.
        
        If this entity does not have a Pool then this method does nothing.
        
        Example:
            
            .. code-block:: python
            
                @toyblock.System
                def life(system, entity):
                    if entity[Life].is_over():
                        entity.free()
        """
        if self._pool is None: return
        self._pool._free(self)

    def __contains__(self, item):
        if isinstance(item, System): return item in self._systems
        return item in self._components

class System(object):
    """Define how are entities processed here.

    In the constructor is mandatory pass a callable.
    After you add at least one entity you can run the system calling it.
    
    Use this as a decorator is **encouraged**. See `Example`.
    
    Parameters:
        callable\_: A callable
    
    .. note::
    
        The signature for the callable is
        
        .. code-block:: python
        
            callable(system, entity, *args, **kwargs)

    Returns:
        A System instance which is callable.
    
    Raises:
        TypeError: If you do not pass a callable.
    
    Example:
        .. code-block:: python

            @toyblock.System
            def physics(system, entity, dt):
                pass
                # do your things here

            physics.add_entity(some_entity)
            # ...
            physics(get_delta_time())
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
        """Get the entities added to this system."""
        return self._entities

    def add_entity(self, entity):
        """Add an entity to this System.
        
        Parameters:
            entity (Entity)
        
        """
        if self in entity: return
        if self._locked:
            self._entities_added_append(entity)
        else:
            self._entities_append(entity)
            entity._add_system(proxy(self))

    def remove_entity(self, entity):
        """Remove an entity from this System.
        
        Parameters:
            entity (Entity)
        
        """
        if self not in entity: return
        if self._locked:
            self._entities_removed_append(entity)
        else:
            self._entities_remove(entity)
            entity._remove_system(self)

    def __call__(self, *args, **kwargs):
        """Run the system.
        
        It is perfectly safe add entities to the system or remove entities from the system.
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

class Pool(object):
    """Manage entities and manage systems related to entities.
    
    Parameters:
        maxlen (int): Total number of entities.
        types (iterable of classes):
        args_list (iterable): A list of args for the classes.
        kwargs_list (iterable): A list of kwargs for the classes.
        systems (iterable of System): Systems related with these entities.
    
    Returns:
        A instance of Pool.
        
    Example:
        .. code-block:: python
        
            class A:
                def __init__(self, a, b):
                    self.a = a
                    self.b = b
                    
            class B:
                def __init__(self, a=0):
                    self.a = a
                    
            class C:
                def __init__(self):
                    self.things = []
        
            args = ((1, 2),)
            kwargs = (None, {"a": 7})
            pool = toyblock.Pool(10, (A, B, C), args, kwargs, systems=(input, physics, touch, life))
    
    """
    def __init__(self, maxlen, types, args_list=(), kwargs_list=(), systems=None):
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

    def init(self, init_):
        """Called when :func:`get` returns a instance of :class:`Entity`.
        
        Parameters:
            init\_ (callable): Signature is init_(entity)
        
        Returns:
            The same callable passed as parameter.
            
        Raises:
            TypeError: if init\_ is not callable.
        """
        if not callable(init_):
            raise TypeError("Pass a callable object.")
        self._init = init_
        return init_

    def clean(self, clean_):
        """The clean function is called when an :class:`Entity` is freed.
        
        Parameters:
            clean\_ (callable): Signature is clean_(entity)
        
        Returns:
            The same callable passed as parameter.
            
        Raises:
            TypeError: if clean\_ is not callable.
        """
        if not callable(clean_):
            raise TypeError("Pass a callable object")
        self._clean = clean_
        return clean_

    def get(self):
        """Return a free :class:`Entity` if avaliable, None otherwise."""
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
        """
            .. deprecated:: 2.0.0
                Use :func:`Entity.free` instead.
        """
        warnings.warn("Use Entity.free() instead", DeprecationWarning, stacklevel=2)
        self._free(entity)

    def free_all(self):
        """Release all the used entities."""
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
