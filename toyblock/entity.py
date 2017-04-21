class Entity(object):
    __slots__ = ('__component')
    def __init__(self):
        self.__component = {}

    def add_component(self, class_, instance):
        if not isinstance(class_, type):
            return False
        if not isinstance(instance, class_):
            return False
        if class_ in self.__component:
            return False
        self.__component[class_] = instance
        return True

    def get_component(self, class_):
        return self.__component[class_]

    def del_component(self, class_):
        del self.__component[class_]
