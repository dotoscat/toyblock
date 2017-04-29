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
        return "{} already exists in {}".format(self.class_, self.entity)

class Entity(object):
    __slots__ = ('_component', '_cache')
    def __init__(self):
        self._component = {}
        self._cache = []

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

    def get_components(self, classes):
        self._cache.clear()
        cache_append = self._cache.append
        component_get = self._component.get
        for class_ in classes:
            cache_append(component_get(class_))
        return self._cache

    def del_component(self, class_):
        """Delete a specific component.

        Return the deleted component(instance), None if not exists.
        """
        return self._component.pop(class_, None)
    
    def __contains__(self, item):
        return item in self._component
