def cons(first, l):
    if not l:
        return [first]
    if isinstance(first, type(l[0])):
        return [first] + l
    raise ValueError("invalid cons(): {first} is not of type {type}".format(
        first = repr(first),
        type  = repr(type(l[0]).__name__))
    )

empty = []

def first(l):
    return l[0]

def second(l):
    return l[1]

def third(l):
    return l[2]

def fourth(l):
    return l[3]

def rest(l):
    return l[1:]

def reverse(l):
    return list(reversed(l))
