class EntityError(Exception):
    pass

class EntityNoTypeError(EntityError):
    def __init__(self, class_):
        self.class_ = class_
    
    def __str__(self):
        return "{} is not a type".format(self.class_)

class Entity(object):
    __slots__ = ('_component')
    def __init__(self):
        self._component = {}

    def add_component(self, class_, instance):
        """Add a component to this entity.

        Return True if done.
        Return False if...
        1) instance is not an instance of class_
        2) class_ is not a type
        3) The type is already in the entity
        """
        if not isinstance(class_, type):
            raise EntityNoTypeError(class_)
        if not isinstance(instance, class_):
            return False
        if class_ in self._component:
            return False
        self._component[class_] = instance
        return True

    def get_component(self, class_):
        """Get a specific component."""
        return self._component.get(class_)

    def get_components(self):
        return self._component.values()

    def del_component(self, class_):
        """Delete a specific component.

        Return the deleted component(instance), None if not exists.
        """
        return self._component.pop(class_, None)
    
    def __contains__(self, item):
        return item in self._component
