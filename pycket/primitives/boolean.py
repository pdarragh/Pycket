class boolean(object):
    def __init__(self, boolval):
        if isinstance(boolval, str):
            if boolval.lower() == '#t':
                self.value = True
            elif boolval.lower() == '#f':
                self.value = False
            else:
                raise ValueError("invalid literal for boolean(): '{}'".format(boolval))
        else:
            self.value = bool(boolval)
    def __str__(self):
        return '#t' if self.value else '#f'
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return self.value == other.value
    def __nonzero__(self):
        return self.value == True
