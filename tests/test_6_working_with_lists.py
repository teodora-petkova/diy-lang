# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises

from diylang.evaluator import evaluate
from diylang.parser import parse
from diylang.types import DiyLangError, Environment


def test_creating_lists_by_quoting():
    """TEST 6.1: One way to create lists is by quoting.

    We have already implemented `quote` so this test should already be
    passing.

    The reason we need to use `quote` here is that otherwise the expression
    would be seen as a call to the first element -- `1` in this case, which
    obviously isn't even a function.
    """

    assert_equals(parse("(1 2 3 #t)"),
                  evaluate(parse("'(1 2 3 #t)"), Environment()))


def test_creating_list_with_cons():
    """TEST 6.2: The `cons` functions prepends an element to the front of a
    list."""

    result = evaluate(parse("(cons 0 '(1 2 3))"), Environment())
    assert_equals(parse("(0 1 2 3)"), result)

def test_creating_list_with_cons_does_not_modify_initial_list():
    """TEST 6.2.1: The `cons` functions prepends an element to the front of a list without modifying the intial list."""

    env = Environment({"initial_list": [1, 2, 3]})

    result = evaluate(parse("(cons 0 initial_list)"), env)
    assert_equals(parse("(0 1 2 3)"), result)

    assert_equals([1, 2, 3], env.lookup("initial_list"))


def test_creating_longer_lists_with_only_cons():
    """TEST 6.3: `cons` needs to evaluate it's arguments.

    Like all the other special forms and functions in our language, `cons` is
    call-by-value. This means that the arguments must be evaluated before we
    create the list with their values.
    """

    result = evaluate(
        parse("(cons 3 (cons (- 4 2) (cons 1 '())))"), Environment())
    assert_equals(parse("(3 2 1)"), result)


def test_getting_first_element_from_list():
    """TEST 6.4: `head` extracts the first element of a list."""

    assert_equals(1, evaluate(parse("(head '(1))"), Environment()))
    assert_equals(1, evaluate(parse("(head '(1 2 3 4 5))"), Environment()))


def test_getting_first_element_from_empty_list():
    """TEST 6.5: If the list is empty there is no first element, and `head
    should raise an error."""

    with assert_raises(DiyLangError):
        evaluate(parse("(head (quote ()))"), Environment())


def test_getting_head_from_value():
    """TEST 6.6: Must be list to get `head`."""

    with assert_raises(DiyLangError):
        evaluate(parse("(head #t)"), Environment())


def test_getting_tail_of_list():
    """TEST 6.7: `tail` returns the tail of the list.

    The tail is the list retained after removing the first element.
    """

    assert_equals([2, 3], evaluate(parse("(tail '(1 2 3))"), Environment()))
    assert_equals([], evaluate(parse("(tail '(1))"), Environment()))


def test_getting_tail_from_empty_list():
    """TEST 6.8: If the list is empty there is no tail, and `tail` should raise
    an error."""

    with assert_raises(DiyLangError):
        evaluate(parse("(tail (quote ()))"), Environment())


def test_getting_tail_from_value():
    """TEST 6.9: Must be list to get `tail`."""

    with assert_raises(DiyLangError):
        evaluate(parse("(tail 1)"), Environment())


def test_checking_whether_list_is_empty():
    """TEST 6.10: The `empty` form checks whether or not a list is empty."""

    assert_equals(False, evaluate(parse("(empty '(1 2 3))"), Environment()))
    assert_equals(False, evaluate(parse("(empty '(1))"), Environment()))

    assert_equals(True, evaluate(parse("(empty '())"), Environment()))
    assert_equals(True, evaluate(parse("(empty (tail '(1)))"), Environment()))

    assert_equals(False, evaluate(
        parse("(empty somelist)"), Environment({"somelist": [1, 2, 3]})))
    assert_equals(
        True,
        evaluate(parse("(empty somelist)"), Environment({"somelist": []})))


def test_getting_empty_from_value():
    """TEST 6.11: Must be list to see if empty."""

    with assert_raises(DiyLangError):
        evaluate(parse("(empty 321)"), Environment())
