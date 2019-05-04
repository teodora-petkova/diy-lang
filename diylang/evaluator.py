# -*- coding: utf-8 -*-

from .types import Environment, DiyLangError, Closure, String
from .ast import is_boolean, is_atom, is_symbol, is_list, is_closure, \
    is_integer, is_string
from .parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports,
making your work a bit easier. (We're supposed to get through this thing
in a day, after all.)
"""

math_expressions = ["eq", "-", "+", "*", "/", "//", "mod", ">"]

def evaluate(ast, env):
    #print(ast)

    if is_boolean(ast):
        return ast
    elif is_integer(ast):
        return ast
    elif is_symbol(ast):
        return env.lookup(ast)
    elif is_closure(ast):
        return evaluate_closure(ast, env)
    elif is_list(ast):
        if len(ast) == 0:
            raise DiyLangError()
        elif is_closure(ast[0]):
            return evaluate_closure_with_free_variables(ast, env)
        elif ast[0] == "quote":
            return ast[1]
        elif ast[0] == "atom":
            return is_atom(evaluate(ast[1], env))
        elif ast[0] == "define":
            return evaluate_define_expression(ast, env)
        elif ast[0] == "lambda":
            return evaluate_lambda_expression(ast, env)
        elif ast[0] == "if":
            return evaluate_if_expression(ast, env)
        elif is_math_expression(ast):
            return evaluate_math_expression(ast, env)
        elif ast[0] == "cons":
            return evaluate_cons(ast, env)
        elif ast[0] == "head":
            return evaluate_head(ast, env)
        elif ast[0] == "tail":
            return evaluate_tail(ast, env)
        elif ast[0] == "empty":
            return evaluate_empty(ast, env)
        elif is_function_in_environment(ast, env):
            return evaluate_function_in_environment(ast, env)
        elif is_list(ast[0]):
            expressions_list = [evaluate(ast[0], env)]
            expressions_list.extend([param for param in ast[1:]])
            return evaluate(expressions_list, env)
        else:
          raise DiyLangError("not a function")
    else:
        raise DiyLangError("Wrong number of arguments")

    """Evaluate an Abstract Syntax Tree in the specified environment."""
    #raise NotImplementedError("DIY")\

def is_math_expression(ast):
    return ast[0] in math_expressions

def evaluate_math_expression(ast, env):

    op = ast[0]
    arg1 = evaluate(ast[1], env)
    arg2 = evaluate(ast[2], env)

    if op == "eq":

      if is_list(arg1) :
          return False
      else:
          return arg1 == arg2

    else:

      if not is_integer(arg1) or not is_integer(arg2):
          raise DiyLangError()

      if op == "+":
          return arg1 + arg2
      elif op == "-":
          return arg1 - arg2
      elif op == "*":
          return arg1 * arg2
      elif op == "/":
          return arg1 // arg2
      elif op == "mod":
          return arg1 % arg2
      elif op == ">":
          return arg1 > arg2

def evaluate_define_expression(ast, env):
    if len(ast) != 3:
        raise DiyLangError("Wrong number of arguments")
    if not is_symbol(ast[1]):
        raise DiyLangError("not a symbol")
    env.set(ast[1], evaluate(ast[2], env))

def evaluate_if_expression(ast, env):
    if evaluate(ast[1], env) == True:
        return evaluate(ast[2], env)
    else:
        return evaluate(ast[3], env)

def evaluate_lambda_expression(ast, env):
    if len(ast) != 3:
        raise DiyLangError("Wrong number of arguments")
    if not is_list(ast[1]):
      raise DiyLangError()
    return Closure(env, ast[1], ast[2])

def evaluate_closure(ast, env):
    new_env = Environment(ast.env.bindings)
    new_env = new_env.extend(env.bindings)
    return evaluate(ast.body, new_env)

def evaluate_closure_with_free_variables(ast, env):
    params_names = ast[0].params
    params_values = ast[1:]
    if len(params_names) != len(params_values) :
        raise DiyLangError("wrong number of arguments, expected %s got %s" % (len(params_names), len(params_values)))

    evaluated_params_values = [evaluate(p, env) for p in params_values]
    params_name_value_pairs = dict(zip(params_names, evaluated_params_values))
    new_env = Environment(params_name_value_pairs)

    return evaluate(ast[0], new_env)

# (define add (lambda (x y) (+ x y)))
# (add 1 2)
# 3
def is_function_in_environment(ast, env):
    return is_symbol(ast[0]) and env.lookup(ast[0]) != None

def evaluate_function_in_environment(ast, env):
    function_name = ast[0]
    function_expression_in_environment = env.lookup(ast[0])
    expressions_list = [function_expression_in_environment]
    expressions_list.extend([param for param in ast[1:]])
    return evaluate(expressions_list, env)

def evaluate_cons(ast, env):
    head = evaluate(ast[1], env)
    tail = evaluate(ast[2], env)
    return [head] + tail

def evaluate_head(ast, env):
    expected_list = evaluate(ast[1:][0], env)
    if not is_list(expected_list):
        raise DiyLangError()
    if len(expected_list) == 0 :
        raise DiyLangError()
    return expected_list[0]

def evaluate_tail(ast, env):
    expected_list = evaluate(ast[1:][0], env)
    if not is_list(expected_list):
        raise DiyLangError()
    if len(expected_list) == 0 :
        raise DiyLangError()
    return expected_list[1:]

def evaluate_empty(ast, env):
    expected_list = evaluate(ast[1], env)
    if not is_list(expected_list):
        raise DiyLangError()
    if len(expected_list) == 0 :
        return True
    else:
        return False
