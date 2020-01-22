ORDER = 0


class RPC(object):
    def __init__(self, methods, args):
        self.method = methods
        self.args = args
