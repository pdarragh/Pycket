import re

# This is necessary so 're' is not imported with 'number'.
__all__ = ['number']

class number(object):
    def __init__(self, num):
        # Check if we got a fraction. Create those recursively.
        if isinstance(num, str):
            if num.find('/') >= 0:
                self.numerator   = number(num[:num.find('/')])
                self.denominator = number(num[num.find('/') + 1:])
                self.__reduce__()
                return
        # These are the different types of recognized numbers.
        integer     = re.compile(r"^-?\d+$")
        floating_nd = re.compile(r"^-?\d+.\d*$")
        floating_wd = re.compile(r"^-?\d*.\d+$")
        # Ensure our number is one of them.
        if not (re.match(integer,     str(num)) or
                re.match(floating_nd, str(num)) or
                re.match(floating_wd, str(num))):
            raise ValueError("invalid literal for number(): '{}'".format(num))
        # Is it an integer?
        if re.match(integer, str(num)):
            self.numerator   = int(num)
            self.denominator = 1
        # Must be a float.
        else:
            self.numerator   = float(num)
            self.denominator = 1
        # Be sure this number is reduced.
        self.__reduce__()
    def __str__(self):
        # Don't print the denominator if we have a simple value!
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return '{}/{}'.format(self.numerator, self.denominator)
    def __repr__(self):
        return self.__str__()
    def __reduce__(self):
        # Check we don't have an illegal formation.
        if self.denominator == 0:
            raise ZeroDivisionError("integer division or modulo by zero")
        if self.denominator == 1:
            if (self.numerator != 0 and
                float(self.numerator) == int(self.numerator)):
                self.numerator = int(self.numerator)
            return
        else:
            a = self.numerator
            b = self.denominator
            while b:
                a, b = b, a%b
            self.numerator   = int(float(self.numerator) / float(a))
            self.denominator = int(float(self.denominator) / float(a))
    def __nonzero__(self):
        return self.numerator != 0
    def __int__(self):
        return int(float(self))
    def __float__(self):
        return float(self.numerator) / float(self.denominator)
    def __add__(self, other):
        other = number(other)
        # Everything is stored as a fraction, so cross-multiply to add.
        # a/x + b/y = (ay + bx) / xy
        numerator   = (self.numerator * other.denominator) + (other.numerator * self.denominator)
        denominator = (self.denominator * other.denominator)
        return number('{}/{}'.format(numerator, denominator))
    def __mul__(self, other):
        other = number(other)
        # Multiply straight across.
        numerator   = (self.numerator * other.numerator)
        denominator = (self.denominator * other.denominator)
        return number('{}/{}'.format(numerator, denominator))
    def __sub__(self, other):
        other = number(other)
        return self.__add__(-other)
    def __div__(self, other):
        other = number(other)
        return self.__mul__(number('{}/{}'.format(other.denominator, other.numerator)))
    def __floordiv__(self, other):
        other = number(other)
        return number(float(self) // float(other))
    def __mod__(self, other):
        other = number(other)
        return number(float(self) % float(other))
    def __iadd__(self, other):
        other = number(other)
        self.numerator   = (self.numerator * other.denominator) + (other.numerator * self.denominator)
        self.denominator = (self.denominator * other.denominator)
        return self
    def __imul__(self, other):
        other = number(other)
        self.numerator   = (self.numerator * other.numerator)
        self.denominator = (self.denominator * other.denominator)
        return self
    def __isub__(self, other):
        other = number(other)
        self.__iadd__(-other)
        return self
    def __idiv__(self, other):
        other = number(other)
        self.__imul__(number('{}/{}'.format(other.denominator, other.numerator)))
        return self
    def __lt__(self, other):
        return float(self) < float(other)
    def __le__(self, other):
        return float(self) <= float(other)
    def __eq__(self, other):
        return float(self) == float(other)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __ge__(self, other):
        return float(self) >= float(other)
    def __gt__(self, other):
        return float(self) > float(other)
    def __neg__(self):
        return self * -1
    def __pos__(self):
        return self
    def __abs__(self):
        if self < 0:
            return -self
        return self
