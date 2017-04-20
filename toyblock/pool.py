class Pool(object):
    __slots__ = ('class_', 'avaliable', 'used')
    def __init__(self, class_, maxlen, *args, **kargs):
        from collections import deque
        self.class_ = class_
        self.avaliable = deque(
            [class_(*args, **kargs) for i in range(maxlen)],
            maxlen
            )
        self.used = deque(maxlen=maxlen)

    def get(self):
        if not self.avaliable:
            return None
        element = self.avaliable.pop()
        self.used.append(element)
        return element

    def free(self, element):
        if not isinstance(element, self.class_) or element not in self.used:
            return False
        element = self.used.pop()
        self.avaliable.append(element)
        return True
