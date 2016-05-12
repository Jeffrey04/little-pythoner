from operator import *

def primitive(func):
    def _decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError:
            return None

    return _decorator

@primitive
def isatom(atom):
    return and_(not_(isinstance(atom, tuple)),
                isinstance(atom, str))


@primitive
def car(l):
    """
    The Law of Car:
    The primitive car is defined only for non-empty lists
    """
    assert l
    assert isinstance(l, tuple)

    return l[0]


@primitive
def cdr(l):
    """
    The Law of Cdr:
    The primitive cdr is defined only for non-empty lists.
    The cdr of any non-empty lists is always another list.
    """
    assert l
    assert isinstance(l, tuple)

    return l[1:]


@primitive
def cons(s, l):
    """
    The Law of Cons
    The primitive cons takes two arguments.
    The second argument to cons must be a list. The result is a list.
    """
    assert isinstance(l, tuple)

    return (s, ) + l


@primitive
def isnull(l):
    """
    The Law of Null?
    The primitive null? is defined only for lists.
    """
    assert isinstance(l, tuple)

    return l == ()


@primitive
def iseq(alpha, beta):
    """
    The Law of Eq?
    The primitive eq? takes two arguments.
    Each must be a non-numeric atom.
    """
    assert isatom(alpha) and isatom(beta)

    return alpha == beta
