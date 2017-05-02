class Pool(object):
    """
    A Pool is used for cache created objects
    """
    __slots__ = ('_avaliable', '_used')
    def __init__(self, maxlen, classes):
        from collections import deque
        from entity import Entity
        self._avaliable = deque(maxlen=maxlen)
        avaliable_append = self._avaliable.append
        for i in range(maxlen):
            entity = Entity()
            entity_add_component = entity.add_component
            for class_ in classes:
                entity_add_component(class_, class_())
            avaliable_append(entity)
        self._used = deque(maxlen=maxlen)

    def get(self):
        """Return a free instance if avaliable, None otherwise.
        """
        if not self._avaliable:
            return None
        element = self._avaliable.pop()
        self._used.append(element)
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
