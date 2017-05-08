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

class Pool(object):
    """
    A Pool is used for cache created objects and increase performance
    
    .. Note::
    
        This is an experimental class
    """
    __slots__ = ('_avaliable', '_used')
    def __init__(self, maxlen, types):
        from collections import deque
        from . import entity
        Entity = entity.Entity
        self._avaliable = deque(maxlen=maxlen)
        avaliable_append = self._avaliable.append
        for i in range(maxlen):
            entity = Entity()
            entity_add_component = entity.add_component
            for type_ in types:
                entity_add_component(type_())
            avaliable_append(entity)
        self._used = deque(maxlen=maxlen)

    def get(self):
        """Return a free instance if avaliable, None otherwise.
        """
        if not self._avaliable:
            return None
        element = self._avaliable.pop()
        self._used.append(element)
        return element

    def free(self, element):
        """Mark the instance to be avaliable and return True.

        Return False if it do not belong to the pool or is not used yet.
        """
        if element not in self._used:
            return False
        self._used.remove(element)
        self._avaliable.append(element)
        return True
