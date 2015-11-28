#!/usr/bin/env python

import argparse
import atexit
import readline

from types import ModuleType, TypeType, FunctionType

import pycket
from pycket.s_expressions.s_expression import _parse_s_exp as parse_sexp

safe_list = {
    x : y for x, y in pycket.__dict__.iteritems()
    if not x.startswith('_')
    if not isinstance(y, ModuleType)
}
def _replace_in_safe_list(d):
    for new_name, old_name in d.iteritems():
        safe_list[new_name] = safe_list.pop(old_name)

typenames = set([key for key in safe_list if isinstance(safe_list[key], TypeType)])

types = {
    typename : safe_list.pop(typename) for typename in typenames
}

# Replace functions named 'is_X' with 'X?'
tests = {
    '{}?'.format(test[3:]) : test for test in safe_list
    if test.startswith('is_')
}
_replace_in_safe_list(tests)
# Replace functions named 'X_bang' with 'X!'
bangs = {
    '{}!'.format(bang[:-5]) : bang for bang in safe_list
    if bang.endswith('_bang')
}
_replace_in_safe_list(bangs)
# Replace functions named 'X_to_Y' with 'X->Y'
converts = {
    convert.replace('_to_', '->') : convert for convert in safe_list
}
_replace_in_safe_list(converts)
# Replace functions named 'X_Y_Z' with 'X-Y-Z'
# This should generally be the last replacement.
kebobs = {
    kebob.replace('_', '-') : kebob for kebob in safe_list
}
_replace_in_safe_list(kebobs)

functions = {
    x : y for x, y in safe_list.iteritems()
    if isinstance(y, FunctionType)
}

def custom_eval(sexp):
    if not sexp.is_list():
        raise RuntimeError("cannot execute: {}".format(sexp))
    l = s_exp_to_list(sexp)
    return eval(
        '{func}({args})'.format(
            l[0].value,
            ', '.join([arg.value for arg in l[1:]])
        ),
        {'__builtins__': None},
        safe_list
    )

def lookup(value):
    raise ValueError("{}: free variable".format(value))

def parse_primitive(sexp):
    return sexp

def parse_input(user_input):
    sexp = parse_sexp(user_input)
    print("sexp: {}".format(sexp))
    print("sexp.value: {}".format(sexp.value))
    if user_input[0] == '(':
        return custom_eval(sexp)
    else:
        return sexp

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
            user_input = raw_input('>>> ').strip()
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
