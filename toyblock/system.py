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

class System(object):
    __slots__ = ('_classes', '_callable_', '_entities', '_args', '_kwargs',
                '_entities_removed', '_entities_added', '_locked')
    def __init__(self, classes, callable_, *args, **kwargs):
        from collections import deque
        self._classes = classes
        self._callable_ = callable_
        self._entities = deque()
        self._args = args
        self._kwargs = kwargs
        self._locked = False
        self._entities_removed = deque()
        self._entities_added = deque()
		
    def add_entity(self, entity):
        if self._locked:
            self._entities_added.append(entity)
        else:
            self._entities.append(entity)

    def remove_entity(self, entity):
        if self._locked:
            self._entities_removed.append(entity)
        else:
            self._entities.remove(entity)
        
    def run(self):
        entities = self._entities
        callable_ = self._callable_
        classes = self._classes
        args = self._args
        kwargs = self._kwargs
        self._locked = True
        for entity in entities:
            components = entity.get_components(classes)
            callable_(self, entity, *components, *args, **kwargs)
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
