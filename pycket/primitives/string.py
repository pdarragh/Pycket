class string(object):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return '"{}"'.format(str(self.text))
    def __repr__(self):
        return self.text
