from pycket import string, symbol, number, boolean
from string import whitespace

def quote(text):
    if not text:
        return None
    return s_exp(text)

def quasiquote(text):
    if not text:
        return None
    return s_exp(text)

BRACES = {
    '{': '}',
    '[': ']',
    '(': ')',
}

DELIMITERS = [
    '"',
    ',',
    '\'',
    '`',
    ';'
]

#TODO
# `read` should return a 2-tuple: (head, tail)
# The `head` contains a fully-parsed representation of the first full object
# `read` can pull out of the text, such as a symbol, number, s-expression, etc.
# `tail` contains the unconsumed text in its entirety.

# Returns 2-tuple: the first "word", which is fully-parsed, and the remainder
# of the text.
#
# This would make sense as a generator.
def split_text(text):
    # Ensure we have something.
    if not text:
        return None, None
    # If we start with a quote, we should get everything through the next quote.
    if text.startswith('"'):
        try:
            r_quote = text[1:].find('"')
        except:
            raise ValueError("incomplete quoted expression: {}".format(text))
        if r_quote < 0:
            raise ValueError("unbalanced quoted text: {}".format(text))
        head = text[:r_quote + 2]
        try:
            tail = text[r_quote + 2:]
        except:
            tail = None
    # Check if we have a brace.
    elif text[0] in BRACES.keys():
        counts  = {brace : 0 for brace in BRACES.keys()}
        r_index = 0
        for i in xrange(len(text)):
            char = text[i]
            if char in BRACES.keys():
                counts[char] += 1
            elif char in BRACES.values():
                counts[matching_brace(char)] -= 1
            if sum(counts.values()) == 0:
                r_index = i
                break
        if r_index <= 0:
            raise ValueError("unbalanced braces in text: {}".format(text))
        head = text[:r_index + 1]
        try:
            tail = text[r_index + 1:]
        except:
            tail = None
    elif text.startswith('\'') or text.startswith('`'):
        quotemark = text[0]
        head, tail = split_text(text[1:])
        if not head:
            raise ValueError("invalid quote form: {}".format(text))
        head = "{}{}".format(quotemark, head)
    else:
        # Find everything up to the first whitespace.
        split = text.split(None, 1)
        if len(split) == 1:
            head = split[0]
            tail = None
        else:
            head, tail = split
    if tail:
        tail = tail.strip()
    return head, tail

def read(text):
    head, tail = split_text(text)
    if not head:
        return None
    if head[0] == '"':
        # The head is a quoted expression.
        return string(head[1:-1])
    elif head[0] in BRACES:
        # The head is a braced expression.
        return s_exp(head[1:-1])
    elif head[0] == "'":
        # The head is a quote form.
        return quote(head[1:])
    elif head[0] == '`':
        # The head is a quasiquote form.
        return quasiquote(head[1:])
    else:
        # The head is something else; hopefully a primitive form.
        try:
            head = number(head)
        except:
            head = symbol(head)
        return head

def parse(text):
    tail = text
    stack = []
    while tail:
        # Split the thing into a head and tail segment.
        head, tail = split_text(tail)
        head = read(head)
        stack.append(head)
    return stack

def matching_brace(brace):
    for opening, closing in BRACES.iteritems():
        if brace == opening:
            return closing
        if brace == closing:
            return opening
    return None

class s_exp(object):
    def __init__(self, text):
        result = parse(text)
        if not text or not result:
            raise ValueError("invalid literal for s-expression: {}".format(text))
        if len(result) == 1:
            self.interior = result[0]
        else:
            self.interior = result
    def __str__(self):
        if self.is_list():
            return '({})'.format(' '.join([str(exp) for exp in self.interior]))
        else:
            return str(self.interior)
    def __repr__(self):
        return str(self)
    def is_list(self):
        return isinstance(self.interior, list)
    def to_list(self):
        if self.is_list():
            return self.interior
        else:
            raise ValueError("not a list: {}".format(self.interior))
