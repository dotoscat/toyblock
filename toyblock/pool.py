class Pool(object):
    __slots__ = ('__class_', '__avaliable', '__used')
    def __init__(self, class_, maxlen, *args, **kargs):
        from collections import deque
        self.__class_ = class_
        self.__avaliable = deque(maxlen=maxlen)
        avaliable_append = self.__avaliable.append
        for i in range(maxlen):
            avaliable_append(class_(*args, **kargs))
        self.__used = deque(maxlen=maxlen)

    def get(self):
        """Return a free instance if avaliable, None otherwise.
        """
        if not self.__avaliable:
            return None
        element = self.__avaliable.pop()
        self.__used.append(element)
        return element

    def free(self, element):
        """Mark the instance to be avaliable and return True

        Return False if it do not belong to the pool or is not used yet.
        """
        if not isinstance(element, self.__class_) or element not in self.__used:
            return False
        element = self.__used.pop()
        self.__avaliable.append(element)
        return True
