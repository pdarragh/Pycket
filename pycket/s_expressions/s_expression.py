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
    elif text[0] in _BRACES.keys():
        counts  = {brace : 0 for brace in _BRACES.keys()}
        r_index = 0
        for i in xrange(len(text)):
            char = text[i]
            if char in _BRACES.keys():
                counts[char] += 1
            elif char in _BRACES.values():
                counts[_matching_brace(char)] -= 1
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
    elif head[0] in _BRACES:
        # The head is a braced expression.
        return s_expression(head[1:-1])
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
            head = bare(head)
        return head

def _parse_s_exp(text):
    tail = text
    stack = []
    while tail:
        # Split the thing into a head and tail segment.
        head, tail = split_text(tail)
        head = read(head)
        stack.append(head)
    return stack

def quote(text):
    if not text:
        return None
    if text.startswith('('):
        return s_expression(text)
    else:
        return symbol(text)

def quasiquote(text):
    if not text:
        return None
    return s_expression(text)

class s_expression(object):
    def __init__(self, text):
        parsed = _parse_s_exp(text)
        if not text or not parsed:
            raise ValueError("invalid literal for s-expression: {}".format(text))
        if len(parsed) == 1:
            self.value = parsed[0]
        else:
            self.value = parsed
    def __str__(self):
        if self.is_list:
            return "'({})".format(' '.join([str(exp) for exp in self.value]))
        else:
            return str(self.value)
    def __repr__(self):
        return str(self)
    @property
    def is_list(self):
        return isinstance(self.value, list)
    @property
    def to_list(self):
        if self.is_list:
            return self.value
        else:
            raise ValueError("not a list: {}".format(self.value))

def s_exp_to_list(sexp):
    if not sexp.is_list:
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
