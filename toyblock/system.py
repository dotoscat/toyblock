class System(object):
    slots = ('_class_', '_callable_', '_entities')
    def __init__(self, callable_, classes_):
        from collections import deque
        self._class_ = classes_
        self._callable_ = callable_
        self._entities = deque()

    def add_entity(self, entity):
        _class_ = self._class_
        for class_ in _class_:
            if class_ not in entity:
                return False
        self._entities.append(entity)
        return True

    def remove_entity(self, entity):
        if entity not in self._entities:
            return False
        self._entities.remove(entity)
        return True
        
    def run(self):
        entities = self._entities
        callable_ = self._callable_
        for entity in entities:
            components = entity.get_components()
            callable_(*components)

    def __len__(self):
        return len(self._entities)
