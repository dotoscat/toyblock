class Pool(object):
    __slots__ = ('__class_', '__avaliable', '__used')
    def __init__(self, class_, maxlen, *args, **kargs):
        from collections import deque
        self.__class_ = class_
        self.__avaliable = deque(
            [class_(*args, **kargs) for i in range(maxlen)],
            maxlen
            )
        self.__used = deque(maxlen=maxlen)

    def get(self):
        if not self.__avaliable:
            return None
        element = self.__avaliable.pop()
        self.__used.append(element)
        return element

    def free(self, element):
        if not isinstance(element, self.__class_) or element not in self.__used:
            return False
        element = self.__used.pop()
        self.__avaliable.append(element)
        return True
