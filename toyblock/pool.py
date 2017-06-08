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

class Pool(object):
    """
    A Pool is used for cache created objects and increase performance.
    """
    __slots__ = ("_avaliable", "_used", "_avaliable_pop",
        "_used_append", "_used_remove", "_avaliable_append")
    def __init__(self, maxlen, types, args_for_types=()):
        """
        Parameters:
        
        maxlen: Number of entities (Number).
        types: Types for the entities (Sequence) with the classes.
        args_for_types: Tuples of args for the instances of types
        [(args, kwargs), ...]
        
        Example of use
        
        arguments = (
            (
                (1, 2),
                None
            ),
            (
                None,
                {"a": 7}
            ),
            None
        )
        
        pool = toyblock.Pool(10, (A, B, C), arguments)
        
        """
        from collections import deque
        from . import entity
        try:
            from itertools import zip_longest
        except:
            from itertools import izip_longest as zip_longest
        Entity = entity.Entity
        self._avaliable = deque(maxlen=maxlen)
        avaliable_append = self._avaliable.append
        EMPTY_TUPLE = ()
        EMPTY_DICT = {}
        EMPTY_ARGS = (None, None)
        for i in range(maxlen):
            entity = Entity()
            entity_add_component = entity.add_component
            for pair in zip_longest(types, args_for_types):
                type_, type_args = pair
                args, kwargs = EMPTY_ARGS if type_args is None else type_args
                args = EMPTY_TUPLE if args is None else args
                kwargs = EMPTY_DICT if kwargs is None else kwargs
                instance = type_(*args, **kwargs)
                entity_add_component(instance)
            avaliable_append(entity)
        self._used = deque(maxlen=maxlen)
        
        #Remap methods to be used directly
        self._avaliable_pop = self._avaliable.pop
        self._used_append = self._used.append
        self._used_remove = self._used.remove
        self._avaliable_append = self._avaliable.append

    def get(self):
        """Return a free instance if avaliable, None otherwise.
        """
        if not self._avaliable:
            return None
        element = self._avaliable_pop()
        self._used_append(element)
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
