# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The DiyLangError class you can have for free :)
"""


class DiyLangError(Exception):
    """General DIY Lang error class."""
    pass

class Closure:

    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body

    def __repr__(self):
        return "<closure/%d>" % len(self.params)


class Environment:

    def __init__(self, variables=None):
        self.bindings = variables if variables else {}

    def lookup(self, symbol):

        if symbol not in self.bindings:
            raise DiyLangError("%s" %symbol)

        return self.bindings[symbol]

    def extend(self, variables):
        new_environment = Environment(self.bindings.copy());
        new_environment.bindings.update(variables)
        return new_environment

    def set(self, symbol, value):
        if symbol in self.bindings:
            raise DiyLangError("already defined")
        self.bindings[symbol]= value


class String:
    """
    Simple data object for representing DIY Lang strings.

    Ignore this until you start working on part 8.
    """

    def __init__(self, val=""):
        self.val = val

    def __str__(self):
        return '"{}"'.format(self.val)

    def __eq__(self, other):
        return isinstance(other, String) and other.val == self.val
