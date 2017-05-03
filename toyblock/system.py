class System(object):
    __slots__ = ('_classes', '_callable_', '_entities', '_args', '_kwargs')
    def __init__(self, classes, callable_, *args, **kwargs):
        from collections import deque
        self._classes = classes
        self._callable_ = callable_
        self._entities = deque()
        self._args = args
        self._kwargs = kwargs

    def add_entity(self, entity):
        self._entities.append(entity)

    def remove_entity(self, entity):
        self._entities.remove(entity)
        
    def run(self):
        entities = self._entities
        callable_ = self._callable_
        classes = self._classes
        args = self._args
        kwargs = self._kwargs
        for entity in entities:
            components = entity.get_components(classes)
            callable_(entity, *components, *args, **kwargs)

    def __contains__(self, entity):
        return entity in self._entities

    def __len__(self):
        return len(self._entities)
