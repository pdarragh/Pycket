class symbol(object):
    def __init__(self, sym):
        self.name = str(sym)
        # Symbols must be connected all the way through.
        if (''.join(self.name.split()) != self.name or
            len(self.name) == 0):
            raise ValueError("invalid literal for symbol(): '{}'".format(sym))
    def __str__(self):
        return "'{}".format(self.name)
    def __repr__(self):
        return '{}'.format(self.name)
    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            return False
