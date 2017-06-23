# Copyright (C) 2017  Oscar Triano 'dotoscat' <dotoscat (at) gmail (dot) com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from warnings import warn

class System(object):
    """
    A bunch of entities by themselves are useless. You must add them
    to a system, then interact with them.
    
    In the constructor is mandatory pass a callable. You can pass other arguments
    that will passed to the callable for each entity.
    
    .. note::
    
        The callable signature is (system, entity, *args, **kwargs).
    
    After you add at least one entity you can run the system anytime with the method *run()*
    """
    def __init__(self, callable_, *args, **kwargs):
        from collections import deque
        self._callable_ = callable_
        self._entities = deque()
        if len(args) or len(kwargs):
            warn("Pass arguments to 'run' method instead.", DeprecationWarning, stacklevel=2)
        self._args = args
        self._kwargs = kwargs
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
        
    def run(self, *args, **kwargs):
        """Run the system. In the callable is perfectly safe add or remove entities
        to the system.
        """
        entities = self._entities
        callable_ = self._callable_
        args = args if len(args) else self._args
        kwargs = kwargs if len(kwargs) else self._kwargs
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
