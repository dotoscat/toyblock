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

from collections import OrderedDict

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

class Entity(object):
    """Entity use the type of the instances used as components as key
    for the instance.
    
    You will not find two instances of the same kind in a entity.
    
    You can pass different instances to the constructor.
        
    `Entity(MyBody(x, y), CoolGraphics())`
    
    """
    __slots__ = ('_components')
    def __init__(self, *instances):
        self._components = {}
        add_component = self.add_component
        for instance in instances:
            add_component(instance)

    def add_component(self, instance):
        """Add a component instance to this entity.
        
        It raises 'EntityComponentExistsError' if the type of instance is already used.
        """
        type_ = type(instance)
        if type_ in self._components:
            raise EntityComponentExistsError(type_, self)
        self._components[type_] = instance

    def get_component(self, type_):
        """Get a specific component."""
        return self._components.get(type_)

    def del_component(self, type_):
        """Delete a specific component.

        Return the deleted component(instance), None if not exists.
        """
        return self._components.pop(type_, None)
    
    def __contains__(self, item):
        return item in self._components
