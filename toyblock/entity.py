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

class EntityError(Exception):
    pass

class EntityNoTypeError(EntityError):
    def __init__(self, class_):
        self.class_ = class_
    
    def __str__(self):
        return "{} is not a type".format(self.class_)

class EntityNoInstanceError(EntityError):
    def __init__(self, instance, class_):
        self.instance = instance
        self.class_ = class_

    def __str__(self):
        return "{} is not an instance of {}".format(self.instance, self.class_)

class EntityComponentExistsError(EntityError):
    def __init__(self, class_, entity):
        self.class_ = class_
        self.entity = entity

    def __str__(self):
        return "Component {} already exists in entity {}".format(self.class_, self.entity)

class Entity(object):
    __slots__ = ('_component')
    def __init__(self):
        self._component = {}

    def add_component(self, class_, instance):
        """Add a component to this entity."""
        if not isinstance(class_, type):
            raise EntityNoTypeError(class_)
        if not isinstance(instance, class_):
            raise EntityNoInstanceError(instance, class_)
        if class_ in self._component:
            raise EntityComponentExistsError(class_, self)
        self._component[class_] = instance

    def get_component(self, class_):
        """Get a specific component."""
        return self._component.get(class_)

    def del_component(self, class_):
        """Delete a specific component.

        Return the deleted component(instance), None if not exists.
        """
        return self._component.pop(class_, None)
    
    def __contains__(self, item):
        return item in self._component
