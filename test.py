import pycket

BRACES = {
    '{': '}',
    '[': ']',
    '(': ')',
}

def matching_brace(brace):
    for opening, closing in BRACES.iteritems():
        if brace == opening:
            return closing
        if brace == closing:
            return opening
    return None

def parse(text):
    result = sub_parse(text)[0]
    if not result:
        raise ValueError("invalid s-expression literal: {}".format(text))
    result = assimilate(result)
    return result

def assimilate(exp):
    """
    returns an new_sexp
    """
    if not exp:
        raise ValueError("nothing to assimilate")
    result = []
    index = 0
    while index < len(exp):
        subexp = exp[index]
        if isinstance(subexp, QUOTE):
            if index == len(exp):
                raise ValueError("invalid quoted expression")
            index += 1
            if isinstance(exp[index], QUOTE) or isinstance(exp[index], BACKTICK):
                raise ValueError("invalid quoted expression")
            if isinstance(exp[index], list):
                result.append(exp[index])
            else:
                result.append(pycket.symbol(exp[index]))
        elif isinstance(subexp, BACKTICK):
            if index == len(exp):
                raise ValueError("invalid quoted expression")
            index += 1
            if isinstance(exp[index], QUOTE) or isinstance(exp[index], BACKTICK):
                raise ValueError("invalid quoted expression")
            result.append(exp[index])
        else:
            if isinstance(subexp, list):
                result.append(assimilate(subexp))
            else:
                result.append(subexp)
        index += 1
    if len(result) == 0:
        raise ValueError("invalid assimilation: {}".format(exp))
    elif len(result) > 1:
        return new_sexp(result)
    else:
        return new_sexp(result[0])

class new_sexp(object):
    autoadds = [pycket.number, pycket.symbol, pycket.string]
    def __init__(self, value):
        if isinstance(value, list):
            self.value = []
            for exp in value:
                if isinstance(exp, new_sexp):
                    self.value.append(exp)
                else:
                    self.value.append(new_sexp(exp))
        elif type(value) in self.autoadds:
            self.value = value
        elif isinstance(value, new_sexp):
            self.value = value
        else:
            try:
                self.value = pycket.number(value)
            except:
                try:
                    self.value = pycket.symbol(value)
                except:
                    self.value = pycket.string(value)
    def is_list(self):
        return isinstance(self.value, list)

def sub_parse(text, index=0, opening=None):
    stack = []
    in_word = False
    while index < len(text):
        if text[index] == "'":
            stack.append(QUOTE())
            index += 1
        elif text[index] == "`":
            stack.append(BACKTICK())
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
        if c in BRACES.keys():
            inner, inner_index = sub_parse(text, index+1, c)
            stack.append(inner)
            index = inner_index + 1
            in_word = False
        elif c in BRACES.values():
            if opening != matching_brace(c):
                raise ValueError("unbalanced braces in s-expression")
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

class QUOTE(object):
    def __str__(self):
        return "QUOTE"
    def __repr__(self):
        return str(self)

class BACKTICK(object):
    def __str__(self):
        return "BACKTICK"
    def __repr__(self):
        return str(self)
