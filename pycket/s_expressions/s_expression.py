import re

from ..primitives import *

__all__ = ['s_expression', 's_exp_to_list', 's_exp_to_num', 's_exp_to_sym', 's_exp_to_string']

_BRACES = {
    '{': '}',
    '[': ']',
    '(': ')',
}

def _matching_brace(brace):
    for opening, closing in _BRACES.iteritems():
        if brace == opening:
            return closing
        if brace == closing:
            return opening
    return None

def _parse_s_exp(text):
    result = _parsed_list_from_text(text)[0]
    if not result:
        raise ValueError("invalid s-expression literal: {}".format(text))
    result = _list_to_s_exp(result)
    return result

def _parsed_list_from_text(text, index=0, opening=None):
    stack = []
    in_word = False
    while index < len(text):
        if text[index] == "'":
            stack.append(_s_exp_quote())
            index += 1
        elif text[index] == "`":
            stack.append(_s_exp_backtick())
            index += 1
        elif text[index] == '"':
            next_index = text.find('"', index + 1)
            if next_index < 0:
                raise ValueError("unbalanced quotes in s-expression")
            stack.append(text[index + 1:next_index])
            index = next_index + 1
        if index >= len(text):
            break
        c = text[index]
        if c in _BRACES.keys():
            inner, inner_index = _parsed_list_from_text(text, index+1, c)
            stack.append(inner)
            index = inner_index + 1
            in_word = False
        elif c in _BRACES.values():
            if opening != _matching_brace(c):
                raise ValueError("unbalanced _BRACES in s-expression")
            return stack, index
        elif c == ' ':
            in_word = False
        else:
            if in_word:
                stack[-1] += c
            else:
                in_word = True
                stack.append(c)
        index += 1
    return stack, index

class _s_exp_quote(object):
    def __str__(self):
        return "_s_exp_quote"
    def __repr__(self):
        return str(self)

class _s_exp_backtick(object):
    def __str__(self):
        return "_s_exp_backtick"
    def __repr__(self):
        return str(self)

def _list_to_s_exp(exp):
    """
    returns an s_expression
    """
    if not exp:
        raise ValueError("nothing to do")
    result = []
    index = 0
    while index < len(exp):
        subexp = exp[index]
        if isinstance(subexp, _s_exp_quote):
            if index == len(exp):
                raise ValueError("invalid quoted expression")
            index += 1
            if isinstance(exp[index], _s_exp_quote) or isinstance(exp[index], _s_exp_backtick):
                raise ValueError("invalid quoted expression")
            if isinstance(exp[index], list):
                result.append(exp[index])
            else:
                result.append(symbol(exp[index]))
        elif isinstance(subexp, _s_exp_backtick):
            if index == len(exp):
                raise ValueError("invalid quoted expression")
            index += 1
            if isinstance(exp[index], _s_exp_quote) or isinstance(exp[index], _s_exp_backtick):
                raise ValueError("invalid quoted expression")
            result.append(exp[index])
        else:
            if isinstance(subexp, list):
                result.append(_list_to_s_exp(subexp))
            else:
                result.append(subexp)
        index += 1
    if len(result) == 0:
        raise ValueError("invalid assimilation: {}".format(exp))
    elif len(result) > 1:
        return s_expression(result)
    else:
        return s_expression(result[0])

class s_expression(object):
    autoadds = [number, symbol, string]
    def __init__(self, value):
        if isinstance(value, list):
            self.value = []
            for exp in value:
                if isinstance(exp, s_expression):
                    self.value.append(exp)
                else:
                    self.value.append(s_expression(exp))
        elif type(value) in self.autoadds:
            self.value = value
        elif isinstance(value, s_expression):
            self.value = value
        else:
            try:
                self.value = number(value)
            except:
                try:
                    self.value = symbol(value)
                except:
                    self.value = string(value)
    def __str__(self):
        if isinstance(self.value, list):
            return "'{}".format(' '.join([repr(exp) for exp in self.value]))
        else:
            return "'{}".format(repr(self.value))
    def is_list(self):
        return isinstance(self.value, list)

def s_exp_to_list(sexp):
    if not sexp.is_list():
        raise ValueError("s-exp->list: not a list: {}".format(sexp))
    return sexp.value

def s_exp_to_num(sexp):
    if not isinstance(sexp, s_expression) or not isinstance(sexp.value, number):
        raise ValueError("s-exp->num: not an s-expression: {}".format(sexp))
    return sexp.value

def s_exp_to_sym(sexp):
    if not isinstance(sexp, s_expression) or not isinstance(sexp.value, symbol):
        raise ValueError("s-exp->sym: not an s-expression: {}".format(sexp))
    return sexp.value

def s_exp_to_string(sexp):
    if not isinstance(sexp, s_expression) or not isinstance(sexp.value, string):
        raise ValueError("s-exp->string: not an s-expression: {}".format(sexp))
    return sexp.value
