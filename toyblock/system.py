class System(object):
    slots = ('_classes', '_callable_', '_entities')
    def __init__(self, callable_, classes):
        from collections import deque
        self._classes = classes
        self._callable_ = callable_
        self._entities = deque()

    def add_entity(self, entity):
        classes = self._classes
        for class_ in classes:
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
        classes = self._classes
        for entity in entities:
            components = entity.get_components(classes)
            callable_(entity, *components)

    def __len__(self):
        return len(self._entities)
