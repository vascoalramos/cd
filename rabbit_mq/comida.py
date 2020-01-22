import uuid


class Hamburger(object):
    def __init__(self):
        self.id = uuid.uuid1()

    def __repr__(self):
        return "Sou um hamburguer com id = {}".format(self.id)
