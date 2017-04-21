class Pool(object):
    __slots__ = ('__class_', '__avaliable', '__used', '__instance')
    def __init__(self, class_, maxlen, *args, **kargs):
        self.__class_ = class_
        self.__avaliable = set()
        avaliable_add = self.__avaliable.add
        for i in range(maxlen):
            instance = class_(*args, **kargs)
            avaliable_add(instance)
        self.__used = set()

    def get(self):
        """Return a free instance if avaliable, None otherwise.
        """
        if not self.__avaliable:
            return None
        element = self.__avaliable.pop()
        self.__used.add(element)
        return element

    def free(self, element):
        """Mark the instance to be avaliable and return True

        Return False if it do not belong to the pool or is not used yet.
        """
        if element not in self.__instance or element not in self.__used:
            return False
        element = self.__used.pop()
        self.__avaliable.append(element)
        return True
