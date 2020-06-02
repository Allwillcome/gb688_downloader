from . import GB, HDB


class Client:
    def __init__(self, t):
        self.type = t

    def create(self):
        if self.type == 'gb':
            return GB()
        elif self.type == 'hb':
            return HDB('hbba')
        elif self.type == 'db':
            return HDB('dbba')