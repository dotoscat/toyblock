class Pool(object):
    __slots__ = ('_class_', '_avaliable', '_used', '_instance')
    def __init__(self, class_, maxlen, *args, **kargs):
        from collections import deque
        self._class_ = class_
        self._avaliable = deque(maxlen=maxlen)
        avaliable_append = self._avaliable.append
        for i in range(maxlen):
            instance = class_(*args, **kargs)
            avaliable_append(instance)
        self._instance = set(self._avaliable)
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
        if element not in self._instance or element not in self._used:
            return False
        self._used.remove(element)
        self._avaliable.append(element)
        return True
