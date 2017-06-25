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
from . import pool, entity
Pool = pool.Pool
Entity = entity.Entity

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
                
    def add_entity(self, entity):
        if self._locked:
            self._entities_added_append(entity)
        else:
            self._entities_append(entity)

    def remove_entity(self, entity):
        if self._locked:
            self._entities_removed_append(entity)
        else:
            self._entities_remove(entity)
        
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
        while len(entities_added):
            entity = entities_added.pop()
            entities.append(entity)
            
    def __contains__(self, entity):
        return entity in self._entities

    def __len__(self):
        return len(self._entities)

def system(callable_):
    """This is a decorator for System.
    
    Example of use:
    
    @toyblock.decorator
    def physics(system, entity, dt):
        # do your things here
    
    physics.add_entity(some_entity)
    
    # ...
    
    physics(get_delta_time())
    """
    if not callable(callable_):
        raise TypeError("Use this as a DECORATOR")
    return System(callable_)
