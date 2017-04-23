class Entity(object):
    __slots__ = ('_component')
    def __init__(self):
        self._component = {}

    def add_component(self, class_, instance):
        if not isinstance(class_, type):
            return False
        if not isinstance(instance, class_):
            return False
        if class_ in self._component:
            return False
        self._component[class_] = instance
        return True

    def get_component(self, class_):
        return self._component.get(class_)

    def del_component(self, class_):
        return self._component.pop(class_, None)
    
