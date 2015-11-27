#!/usr/bin/env python

import argparse
import atexit
import readline

from types import ModuleType, TypeType, FunctionType

import pycket

safe_list = {
    x : y for x, y in pycket.__dict__.iteritems()
    if not x.startswith('_')
    if not isinstance(y, ModuleType)
}

functions = {
    x : y for x, y in safe_list.iteritems()
    if isinstance(y, FunctionType)
}

types = {
    x : y for x, y in safe_list.iteritems()
    if isinstance(y, TypeType)
}

def custom_eval(statement):
    return eval(statement, {'__builtins__': None}, safe_list)

def lookup(value):
    raise ValueError("{}: free variable".format(value))

def parse_primitive(primitive):
    if primitive[0] == "'":
        # It's a symbol.
        return pycket.symbol(primitive[1:])
    if primitive[0] == "`":
        # It's an s-expression.
        return
    try:
        # Is it a number?
        return pycket.number(primitive)
    except:
        # Maybe it's in the local namespace?
        lookup(primitive)

def parse_input(user_input):
    if not user_input.startswith('('):
        return parse_primitive(user_input)
    return custom_eval(user_input)

if __name__ == '__main__':
    print("Safe List:")
    for x, y in safe_list.iteritems():
        print('    {}: {}'.format(x, y))
    print("Functions:")
    for x, y in functions.iteritems():
        print('    {}: {}'.format(x, y))
    print("Types:")
    for x, y in types.iteritems():
        print('    {}: {}'.format(x, y))
    while(True):
        try:
            user_input = raw_input('>>> ')
            if not user_input:
                continue
            result = parse_input(user_input)
            print('~ {}'.format(type(result).__name__))
            print('{}'.format(result))
        except KeyboardInterrupt:
            print
            break
        except EOFError:
            print
            break
        except Exception as e:
            print(e.message)
