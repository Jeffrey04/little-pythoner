from operator import *

def isatom(atom):
    return not isinstance(atom, tuple) and (isinstance(atom, str)
                                            or (isinstance(atom, int) and atom >= -1))

def cons(head, tail):
    """
    The Law of Cons
    The primitive cons takes two arguments.
    The second argument to cons must be a list. The result is a list.
    """
    assert isinstance(tail, tuple)

    return (head, ) + tail

def car(_list):
    """
    The Law of Car:
    The primitive car is defined only for non-empty lists
    """
    assert _list
    assert isinstance(_list, tuple)

    return _list[0]

def cdr(_list):
    """
    The Law of Cdr:
    The primitive cdr is defined only for non-empty lists.
    The cdr of any non-empty lists is always another list.
    """
    assert _list
    assert isinstance(_list, tuple)

    return _list[1:]

def isnull(_list):
    """
    The Law of Null?
    The primitive null? is defined only for lists.
    """
    assert isinstance(_list, tuple)

    return _list == ()

def iseq(alpha, beta):
    """
    The Law of Eq?
    The primitive eq? takes two arguments.
    Each must be a non-numeric atom.
    """
    assert isatom(alpha) and isatom(beta)

    return alpha == beta

def islat(_list):
    assert isinstance(_list, tuple)

    return (True if isnull(_list)
            else islat(cdr(_list)) if isatom(car(_list))
            else False)

def ismember(atom, lat):
    """
    The First Commandment
    Always ask null? as the first question in expressing any function
    """
    assert isatom(atom) and islat(lat)

    return (False if isnull(lat)
            else or_(iseq(car(lat), atom),
                     ismember(atom, cdr(lat))))

def rember(atom, lat):
    """
    The Second Commandment
    Use cons to build lists
    """
    assert isatom(atom) and islat(lat)

    return (() if isnull(lat)
            else cdr(lat) if iseq(atom, car(lat))
            else cons(car(lat), rember(atom, cdr(lat))))

def firsts(lat):
    """
    The Third Commandment
    When building a list, describe the first typical
    element, and then cons it onto the natural recursion
    """
    return (() if isnull(lat)
            else cons(car(car(lat)), firsts(cdr(lat))))

def insertR(new, old, lat):
    assert isatom(new) and isatom(old) and islat(lat)

    return (() if isnull(lat)
            else cons(car(lat),
                      cons(new, cdr(lat)) if iseq(old, car(lat))
                      else insertR(new, old, cdr(lat))))

def insertL(new, old, lat):
    assert isatom(new) and isatom(old) and islat(lat)

    return (() if isnull(lat)
            else cons(new, lat) if iseq(car(lat), old)
            else cons(car(lat), insertL(new, old, cdr(lat))))

def subst(new, old, lat):
    assert isatom(new) and isatom(old) and islat(lat)

    return (() if isnull(lat)
            else cons(new, cdr(lat)) if iseq(old, car(lat))
            else cons(car(lat), subst(new, old, cdr(lat))))

def subst2(new, o1, o2, lat):
    assert isatom(new) and isatom(o1) and isatom(o2) and islat(lat)

    return (() if isnull(lat)
            else cons(new, cdr(lat)) if or_(iseq(o1, car(lat)), iseq(o2, car(lat)))
            else cons(car(lat), subst(new, o1, o2, cdr(lat))))

def multirember(atom, lat):
    assert isatom(atom) and islat(lat)

    return (() if isnull(lat)
            else multirember(atom, cdr(lat)) if iseq(atom, car(lat))
            else cons(car(lat), multirember(atom, cdr(lat))))

def multiinsertR(new, old, lat):
    assert isatom(new) and isatom(old) and islat(lat)

    return (() if isnull(lat)
            else cons(old, cons(new,
                                multiinsertR(new, old, cdr(lat)))) if iseq(old, car(lat))
            else cons(car(lat), multiinsertR(new, old, cdr(lat))))

def multiinsertL(new, old, lat):
    """
    The Fourth Commandment (preliminary)
    Always change at least one argument when recurring.
    It must be changed closer to termination.
    The changing argument must be tested in the termination condition:
        when using cdr, test termination with null?
    """
    assert isatom(new) and isatom(old) and islat(lat)

    return (() if isnull(lat)
            else cons(new, cons(old, multiinsertL(new, old, cdr(lat)))) if iseq(old, car(lat))
            else cons(car(lat), multiinsertL(new, old, cdr(lat))))

def multisubst(new, old, lat):
    assert isatom(new) and isatom(old) and islat(lat)

    return (() if isnull(lat)
            else cons(new if iseq(old, car(lat)) else car(lat),
                      multisubst(new, old, cdr(lat))))

def add1(atom):
    assert isatom(atom)

    return add(atom, 1)

def sub1(atom):
    assert isatom(atom)

    return max(sub(atom, 1), -1)

def iszero(atom):
    assert isatom(atom)

    return eq(atom, 0)

def _add(n, m):
    assert isatom(n) and isatom(m)

    return (n if iszero(m)
            else add1(_add(n, sub1(m))))

def _sub(n, m):
    assert isatom(n) and isatom(m)

    return (n if iszero(m)
            else sub1(_sub(n, sub1(m))))

def addtup(tup):
    """
    The First Commandment (first revision)
    When recurring on a list of atoms, lat, ask two questions about it:
    (null? lat) and else
    When recurring on a number, n, ask two questions about it:
    (zero? n) and else
    """
    return (0 if isnull(tup)
            else _add(car(tup), addtup(cdr(tup))))

def _mul(n, m):
    """
    The Fourth Commandment (first revision)
    Always change at least one argument while recurring.
    It must be changed to be closer to termination.
    The changing argument must be tested in the termination condition:
    when using cdr, test termination with null? and
    when using sub1, test termination with zero?

    The Fifth Commandment
    When building a value with +, always use 0 for the value of the
    terminating line, for adding 0 does not change the value of an
    addition.
    When building a value with x, always use 1 for the value of the
    terminating line, for multiplying 1 does not change the value
    of a multiplication.
    When building a value with cons, always consider () for the value
    of the terminating line.
    """
    assert isatom(n) and isatom(m)

    return (0 if iszero(m)
            else _add(n, _mul(n, sub1(m))))

def tupplus(tup1, tup2):
    return (tup2 if (isnull(tup1))
            else tup1 if (isnull(tup2))
            else cons(_add(car(tup1), car(tup2)),
                      tupplus(cdr(tup1), cdr(tup2))))

def _gt(n, m):
    assert isatom(n) and isatom(m)

    return (False if iszero(n)
            else True if iszero(m)
            else _gt(sub1(n), sub1(m)))

def _lt(n, m):
    assert isatom(n) and isatom(m)

    return (False if iszero(m)
            else True if iszero(n)
            else _lt(sub1(n), sub1(m)))

def _eq(n, m):
    assert isatom(n) and isatom(m)

    return (iszero(n) if iszero(m)
            else False if iszero(n)
            else _eq(sub1(n), sub1(m)))

def _eq2(n, m):
    assert isatom(n) and isatom(m)

    return (False if or_(_gt(n, m), _lt(n, m))
            else True)

def _pow(n, m):
    assert isatom(n) and isatom(m)

    return (1 if iszero(m)
            else _mul(n, _pow(n, sub1(m))))

def _div(n, m):
    assert isatom(n) and isatom(m)

    return (0 if _lt(n, m)
            else add1(_div(_sub(n, m), m)))

def length(lat):
    assert islat(lat)

    return (0 if isnull(lat)
            else add1(length(cdr(lat))))

def isundefined(atom):
    return atom == -1

def pick(n, lat):
    assert isatom(n) and islat(lat)

    return (-1 if isundefined(sub1(n))
            else car(lat) if iszero(sub1(n))
            else pick(sub1(n), cdr(lat)))

def rempick(n, lat):
    assert isatom(n) and islat(lat)

    return (lat if isundefined(sub1(n))
            else () if isnull(lat)
            else cdr(lat) if iszero(sub1(n))
            else cons(car(lat), rempick(sub1(n), cdr(lat))))

def isnumber(atom):
    return isinstance(atom, int)

def no_nums(lat):
    assert islat(lat)

    return (() if isnull(lat)
            else no_nums(cdr(lat)) if isnumber(car(lat))
            else cons(car(lat), no_nums(cdr(lat))))


def all_nums(lat):
    assert islat(lat)

    return (() if isnull(lat)
            else cons(car(lat), all_nums(cdr(lat))) if isnumber(car(lat))
            else all_nums(cdr(lat)))

def isegan(a1, a2):
    assert isatom(a1) and isatom(a2)

    return (_eq(a1, a2) if and_(isnumber(a1), isnumber(a2))
            else False if or_(isnumber(a1), isnumber(a2))
            else (iseq(a1, a2)))

def occur(atom, lat):
    assert isatom(atom) and islat(lat)

    return (0 if isnull(lat)
            else add1(occur(atom, cdr(lat))) if isegan(atom, car(lat))
            else occur(atom, cdr(lat)))

def isone(atom):
    assert isatom(atom)

    return isegan(atom, 1)

def rempick2(n, lat):
    assert isatom(n) and islat(lat)

    return (lat if isundefined(sub1(n))
            else () if isnull(lat)
            else cdr(lat) if isone(n)
            else cons(car(lat), rempick(sub1(n), cdr(lat))))


def rember_star(atom, _list):
    assert isatom(atom)

    return (() if isnull(_list)
            else (rember_star(atom, cdr(_list)) if isegan(atom, car(_list))
                  else cons(car(_list),
                            rember_star(atom,
                                        cdr(_list)))) if isatom(car(_list))
            else cons(rember_star(atom, car(_list)),
                      rember_star(atom, cdr(_list))))

def insertL_star(new, old, _list):
    assert isatom(new) and isatom(old)

    return (() if isnull(_list)
            else (cons(new, cons(old, insertL_star(new, old, cdr(_list)))) if isegan(old, car(_list))
                  else cons(car(_list),
                            insertL_star(new, old, cdr(_list)))) if isatom(car(_list))
            else cons(insertL_star(new, old, car(_list)),
                      insertL_star(new, old, cdr(_list))))

def insertR_star(new, old, _list):
    """
    The First Commandment
    When recurring on a list of atoms, lat, ask two questions about it:
    (null? lat) and else
    When recurring on a number, n, ask two questions about it:
    (zero? n) and else
    WHen recurring on a list of S-expressions, l, ask three
    questions about it: (null? l), (atom? l), and else

    The Fourth Commandment
    Always change at least one argument while recurring.
    When recurring on a list of atoms, lat, use (cdr lat).
    WHen recurring on a number, n, use (sub1 n).
    And when recurring on a list of S-expressions, l, use (car l)
    and (cdr l) if neither (null? l) nor (atom? (car l)) are true.
    It must be changed to be closer to termination. The changing
    argument must be tested in the termination condition:
    when using cdr, test termination with null? and
    when using sub1, test termination with zero?.
    """
    assert isatom(new) and isatom(old)

    return (() if isnull(_list)
            else (cons(old, cons(new, insertR_star(new, old, cdr(_list)))) if isegan(old, car(_list))
                  else cons(car(_list), insertR_star(new, old, cdr(_list)))) if isatom(car(_list))
            else cons(insertR_star(new, old, car(_list)),
                      insertR_star(new, old, cdr(_list))))

def occur_star(atom, _list):
    assert isatom(atom)

    return (0 if isnull(_list)
            else (add1(occur_star(atom, cdr(_list))) if isegan(atom, car(_list))
                  else occur_star(atom, cdr(_list))) if isatom(car(_list))
            else _add(occur_star(atom, car(_list)),
                      occur_star(atom, cdr(_list))))

def subst_star(new, old, _list):
    assert isatom(new) and isatom(old)

    return (() if isnull(_list)
            else (cons(new, subst_star(new, old, cdr(_list))) if isegan(old, car(_list))
                  else cons(car(_list), subst_star(new, old, cdr(_list)))) if isatom(car(_list))
            else cons(subst_star(new, old, car(_list)),
                      subst_star(new, old, cdr(_list))))

def member_star(atom, _list):
    assert isatom(atom)

    return (False if isnull(_list)
            else or_(isegan(atom, car(_list)),
                     member_star(atom, cdr(_list))) if isatom(car(_list))
            else or_(member_star(atom, car(_list)),
                     member_star(atom, cdr(_list))))

def leftmost(_list):
    return (car(_list) if isatom(car(_list))
            else leftmost(car(_list)))

def iseqlist(_l1, _l2):
    return (True if and_(isnull(_l1), isnull(_l2))
            else and_(isegan(car(_l1), car(_l2)),
                      iseqlist(cdr(_l1), cdr(_l2))) if and_(isatom(car(_l1)), isatom(car(_l2)))
            else False if or_(and_(isnull(_l1), isatom(car(_l2))),
                              and_(isnull(_l2), isatom(car(_l1))))
            else False if or_(isatom(car(_l1)), isatom(car(_l2)))
            else False if or_(isnull(_l1), isnull(_l2))
            else and_(iseqlist(car(_l1), car(_l2)),
                      iseqlist(cdr(_l1), cdr(_l2))))

def isequal(s1, s2):
    return (isegan(s1, s2) if and_(isatom(s1), isatom(s2))
            else False if or_(isatom(s1), isatom(s2))
            else iseqlist(s1, s2))

def iseqlist2(_l1, _l2):
    """
    The Sixth Commandment
    Simplify only after the function is correct.
    """
    return (True if and_(isnull(_l1), isnull(_l2))
            else False if or_(isnull(_l1), isnull(_l2))
            else and_(isequal(car(_l1), car(_l2)),
                      iseqlist(cdr(_l1), cdr(_l2))))

def rember2(s, _list):
    return (() if isnull(_list)
            else cdr(_list) if isequal(s, car(_list))
            else cons(car(_list), rember2(s, cdr(_list))))

def isnumbered(aexp):
    return (isnumber(aexp) if isatom(aexp)
            else and_(isnumbered(car(aexp)),
                      isnumbered(car(cdr(cdr(aexp))))))

def operator(nexp):
    return car(cdr(nexp))

def value(nexp):
    """
    The Seventh Commandment
    Recur on the subparts that are of the same nature:
    * On the sublists of a list.
    * On the subexpressions of an arithmetic expression.

    The Eighth Commandment
    Use help functions to abstract from representations.
    """
    return (nexp if isatom(nexp)
            else _add(value(car(nexp)), value(car(cdr(cdr(nexp))))) if iseq('+', operator(nexp))
            else _mul(value(car(nexp)), value(car(cdr(cdr(nexp))))) if iseq('*', operator(nexp))
            else _pow(value(car(nexp)), value(car(cdr(cdr(nexp))))))

def ismember2(atom, lat):
    assert isatom(atom) and islat(lat)

    return (False if isnull(lat)
            else or_(isequal(car(lat), atom),
                     ismember2(atom, cdr(lat))))

def isset(lat):
    return (True if isnull(lat)
            else False if ismember2(car(lat), cdr(lat))
            else isset(cdr(lat)))

def multirember2(atom, lat):
    assert isatom(atom) and islat(lat)

    return (() if isnull(lat)
            else multirember2(atom, cdr(lat)) if isequal(atom, car(lat))
            else cons(car(lat), multirember2(atom, cdr(lat))))

def makeset(lat):
    return (() if isnull(lat)
            else cons(car(lat), makeset(multirember2(car(lat), cdr(lat)))))

def issubset(set1, set2):
    return (True if isnull(set1)
            else and_(ismember2(car(set1), set2),
                      issubset(cdr(set1), set2)))

def iseqset(set1, set2):
    return and_(issubset(set1, set2),
                issubset(set2, set1))

def isintersect(set1, set2):
    return (False if isnull(set1)
            else or_(ismember2(car(set1), set2),
                     isintersect(cdr(set1), set2)))

def intersect(set1, set2):
    return (() if isnull(set1)
            else cons(car(set1), intersect(cdr(set1), set2)) if ismember2(car(set1), set2)
            else intersect(cdr(set1), set2))

def union(set1, set2):
    return (set2 if isnull(set1)
            else union(cdr(set1), set2) if ismember2(car(set1), set2)
            else cons(car(set1),
                      union(cdr(set1), set2)))

def difference(set1, set2):
    return (() if isnull(set1)
            else differene(cdr(set1), set2) if ismember2(car(set1), set2)
            else cons(car(set1), difference(cdr(set1), set2)))

def intersectall(l_set):
    return (car(l_set) if isnull(cdr(l_set))
            else intersect(car(l_set),
                           intersectall(cdr(l_set))))

def isapair(pair):
    return (False if and_(isatom(pair), isnull(pair))
            else False if isnull(cdr(pair))
            else True if isnull(cdr(cdr(pair)))
            else False)

def first(pair):
    return car(pair)

def second(pair):
    return car(cdr(pair))

def build(s1, s2):
    return cons(s1, cons(s2, ()))

#def isrel(rel):
#    return (True if isnull(rel)
#            else isrel(cdr(rel)) if isapair(car(rel))
#            else False)

def isfun(rel):
    return isset(firsts(rel))

def revrel(rel):
    return (() if isnull(rel)
            else cons(build(second(car(rel)), first(car(rel))),
                      revrel(cdr(rel))))

def revpair(pair):
    return build(second(pair), first(pair))

def revrel2(rel):
    return (() if isnull(rel)
            else cons(revpair(car(rel)),
                      revrel(cdr(rel))))

def seconds(_list):
    return (() if isnull(_list)
            else cons(car(cdr(car(_list))),
                      seconds(cdr(_list))))

def isfullfun(rel):
    return isset(seconds(rel))

def isone_to_one(rel):
    return isfun(revrel(rel))

def insertL2(new, old, lat):
    assert isatom(new) and isatom(old) and islat(lat)

    return (() if isnull(lat)
            else cons(new, lat) if isequal(car(lat), old)
            else cons(car(lat), insertL(new, old, cdr(lat))))

def rember_f(fun, s, _list):
    return (() if isnull(_list)
            else cdr(_list) if fun(s, car(_list))
            else cons(car(_list), rember_f(fun, s, cdr(_list))))

def iseq_c(a):
    return lambda x: iseq(x, a)

def rember_f2(fun):
    return (lambda s, _list:
            () if isnull(_list)
            else cdr(_list) if fun(s, car(_list))
            else cons(car(_list), rember_f2(fun)(s, cdr(_list))))

def insertL_f(fun):
    return (lambda new, old, lat:
            () if isnull(lat)
            else cons(new, lat) if fun(car(lat), old)
            else cons(car(lat), insertL_f(fun)(new, old, cdr(lat))))

def insertR_f(fun):
    return (lambda new, old, lat:
            () if isnull(lat)
            else cons(car(lat),
                      cons(new, cdr(lat)) if fun(old, car(lat))
                      else insertR_f(fun)(new, old, cdr(lat))))

def insert_g(seq):
    """
    The Ninth Commandment
    Abstract common patterns with a new function.
    """
    return (lambda new, old, _list:
            () if isnull(lat)
            else cons(car(lat), seq(new, old, cdr(_list))) if iseq(old, car(lat))
            else cons(car(_list), insert_g(seq)(new, old, _list)))

insertL_l = insert_g(lambda new, old, _list: cons(new, cons(old, _list)))
insertR_l = insert_g(lambda new, old, _list: cons(old, cons(new, _list)))

def atom_to_function(x):
    return (_add if iseq(x, '+')
            else _mul if iseq(x, '*')
            else _pow)

def value2(nexp):
    return (nexp if isatom(nexp)
            else atom_to_function(operator(nexp))(value2(car(nexp)),
                                                  value2(car(cdr(cdr(nexp))))))

def multirember_f(fun):
    return (lambda atom, lat:
            () if isnull(lat)
            else multirember2(atom, cdr(lat)) if fun(atom, car(lat))
            else cons(car(lat), multirember_f(fun)(atom, cdr(lat))))

def multirember_t(fun, lat):
    return (() if isnull(lat)
            else multirember_t(fun, cdr(lat)) if fun(car(lat))
            else cons(car(lat), multirember_t(fun, cdr(lat))))

def multirember_n_co(a, lat, col):
    """
    The Tenth Commandment
    Build functions to collect more than one value at a time.
    """
    return (col((), ()) if isnull(lat)
            else multirember_n_co(a,
                                  cdr(lat),
                                  lambda newlat, seen:
                                  col(newlat, cons(car(lat), seen))) if  iseq(a, car(lat))
            else multirember_n_co(a,
                                  cdr(lat),
                                  lambda newlat, seen:
                                  col(cons(car(lat), newlat),
                                      seen)))

def a_friend(x, y):
    return isnull(y)

def multiinsertLR(new, oldL, oldR, lat):
    assert isatom(new) and isatom(oldL) and isatom(oldR) and islat(lat)

    return (() if isnull(lat)
            else cons(new, cons(oldL, multiinsertLR(new, oldL, oldR, cdr(lat)))) if iseq(oldL, car(lat))
            else cons(oldR, cons(new, multiinsertLR(new, oldL, oldR, cdr(lat)))) if iseq(oldR, car(lat))
            else cons(car(lat),
                      multiinsertLR(new, oldL, oldR, cdr(lat))))

def multiinsertLR_n_co(new, oldL, oldR, lat, col):
    return (col((), 0, 0) if isnull(lat)
            else multiinsertLR_n_co(new, oldL, oldR, cdr(lat), lambda newlat, L, R: col(cons(new, cons(oldL, newlat)), add1(L), R)) if iseq(oldL, car(lat))
            else multiinsertLR_n_co(new, oldL, oldR, cdr(lat), lambda newlat, L, R: col(cons(oldR, cons(new, newlat)), L, add1(R))) if iseq(oldR, car(lat))
            else multiinsertLR_n_co(new, oldL, oldR, cdr(lat), lambda newlat, L, R: col(cons(car(lat), newlat), L, R)))

def iseven(n):
    return eq(0, mod(n, 2))

def evens_only_star(_list):
    return (() if isnull(_list)
            else (cons(car(_list), evens_only_star(cdr(_list))) if iseven(car(_list))
                  else evens_only_star(cdr(_list))) if isatom(car(_list))
            else cons(evens_only_star(car(_list)),
                      evens_only_star(cdr(_list))))

def evens_only_star_n_co(_list, col):
    return (col((), 1, 0) if isnull(_list)
            else (evens_only_star_n_co(cdr(_list), lambda newl, p, s: col(cons(car(_list), newl), _mul(car(_list), p), s)) if iseven(car(_list))
                  else evens_only_star_n_co(cdr(_list), lambda newl, p, s: col(newl, p, _add(car(_list), s)))) if isatom(car(_list))
            else evens_only_star_n_co(car(_list),
                                      lambda lcar, pcar, scar:
                                        evens_only_star_n_co(cdr(_list),
                                                             lambda lcdr, pcdr, scdr:
                                                                col(cons(lcar, lcdr),
                                                                    _mul(pcar, pcdr),
                                                                    _add(scar, scdr)))))

def looking(atom, lat):
    return keep_looking(atom, pick(1, lat), lat)

def keep_looking(atom, sorn, lat):
    return (keep_looking(atom, pick(sorn, lat), lat) if isnumber(sorn)
            else iseq(atom, sorn))

def shift(pair):
    return build(first(first(pair)),
                 build(second(first(pair)),
                       second(pair)))

def eternity(x):
    return eternity(x)

def _length(mk_length):
    assert callable(mk_length)

    return lambda l: (0 if isnull(l)
                      else add1(mk_length(cdr(l))))

def _length_for_1(mk_length):
    assert callable(mk_length)

    return lambda l: (0 if isnull(l)
                      else add1(mk_length(eternity)(cdr(l))))

def _length_many(mk_length):
    assert callable(mk_length)

    return lambda l: (0 if isnull(l)
                      else add1(mk_length(mk_length)(cdr(l))))

def _length_general(mk_length):
    assert callable(mk_length)

    def _(Length):
        return lambda l: (0 if isnull(l)
                          else add1(Length(cdr(l))))

    return _(lambda x: mk_length(mk_length)(x))

def _length_y(Length):
    assert callable(Length)

    return lambda l: (0 if isnull(l)
                      else add1(Length(cdr(l))))

def Y(le):
    def _(f):
        return le(lambda x: f(f)(x))

    return (lambda f: f(f))(_)

length_0 = (lambda mk_length: mk_length(eternity))(_length)
length_1 = (lambda mk_length: mk_length(mk_length(eternity)))(_length)

length_2 = (lambda mk_length: mk_length(mk_length(mk_length(eternity))))(_length)

_length_0 = (lambda mk_length: mk_length(mk_length))(_length)
_length_1 = (lambda mk_length: mk_length(mk_length))(_length_for_1)

length2 = (lambda mk_length: mk_length(mk_length))(_length_many)
length3 = (lambda mk_length: mk_length(mk_length))(_length_general)

length4 = Y(_length_y)

new_entry = build

def lookup_in_entry(name, entry, entry_f):
    return lookup_in_entry_help(name,
                                first(entry),
                                second(entry),
                                entry_f)

def lookup_in_entry_help(name, names, values, entry_f):
    return (entry_f(name) if isnull(names)
            else car(values) if iseq(name, car(names))
            else lookup_in_entry_help(name,
                                      cdr(names),
                                      cdr(values),
                                      entry_f))

extend_table = cons

def lookup_in_table(name, table, table_f):
    return (table_f(name) if isnull(table)
            else lookup_in_entry(name,
                                 car(table),
                                 lambda name:
                                    lookup_in_table(name,
                                                    cdr(table),
                                                    table_f)))

def expression_to_action(e):
    return (atom_to_function2(e) if isatom(e)
            else list_to_action(e))

def atom_to_function2(e):
    return ('*number' if isnumber(e)
            else Const if iseq(e, True)
            else Const if iseq(e, False)
            else Const if iseq(e, 'cons')
            else Const if iseq(e, 'car')
            else Const if iseq(e, 'cdr')
            else Const if iseq(e, 'null?')
            else Const if iseq(e, 'eq?')
            else Const if iseq(e, 'atom?')
            else Const if iseq(e, 'zero?')
            else Const if iseq(e, 'add1')
            else Const if iseq(e, 'sub1')
            else Const if iseq(e, 'number?')
            else Identifier)

def list_to_action(e):
    return (('*quote' if iseq(car(e), 'quote')
             else Lambda if iseq(car(e), 'lambda')
             else Cond if iseq(car(e), 'cond')
             else Application) if isatom(car(e))
            else Application)

def Value(e):
    return meaning(e, ())

def meaning(e, table):
    return expression_to_action(e, table)

def Const(e, table):
    return (e if isnumber(e)
            else True if iseq(e, True)
            else False if iseq(e, False)
            else build('primitive', e))

text_of = second

def Quote(e, table):
    return text_of(e, table)

def initial_table(name):
    return car(())

def Identifier(e, table):
    return lookup_in_table(e, table, initial_table)

def Lambda(e, table):
    return build('non-primitive', cons(table, cdr(e)))

table_of = first
formals_of = second
body_of = lambda x: car(cdr(cdr(x)))

question_of = first
answer_of = second

def evcon(lines, table):
    return (meaning(answer_of(car(lines)), table) if iselse(question_of(car(lines)))
            else meaning(answer_of(car(lines)), table) if meaning(question_of(car_lines), table)
            else evcon(cdr(lines), table))

def iselse(x):
    return (iseq(x, 'else') if isatom(x)
            else False)

cond_lines_of = cdr

def Cond(e, table):
    return evcon(cond_lines_of(e), table)

def evlis(args, table):
    return (() if isnull(args)
            else cons(meaning(car(args), table),
                      evlis(cdr(args), table)))

def isprimitive(l):
    return iseq('primitive', first(l))

def isprimitive(l):
    return iseq('non-primitive', first(l))

def iscatom(x):
    return (True if isatom(x)
            else False if isnull(x)
            else True if iseq(x, 'primitive')
            else True if iseq(x, 'non-primitive')
            else False)

def apply_primitive(name, vals):
    return (cons(first(vals), second(vals)) if iseq(name, 'cons')
            else car(first(vals)) if iseq(name, 'car')
            else cdr(first(vals)) if iseq(name, 'cdr')
            else isnull(first(vals)) if iseq(name, 'null?')
            else iseq(first(vals), second(vals)) if iseq(name, 'eq?')
            else iscatom(first(vals)) if iseq(name, 'atom?')
            else iszero(first(vals)) if iseq(name, 'zero?')
            else add1(first(vals)) if iseq(name, 'add1')
            else sub1(first(vals)) if iseq(name, 'sub1')
            else isnumber(first(vals)))

def apply_closure(closure, vals):
    return meaning(body_of(closure),
                   extend_table(new_entry(formals_of(closure),
                                          vals),
                                table_of(closure)))

def apply(fun, vals):
    return (apply_primitive(second(fun), vals) if isprimitive(fun)
            else apply_closure(second(fun), vals))

function_of = car
arguments_of = cdr

def Application(e, table):
    return apply(meaning(function_of(e), table),
                 evlis(arguments_of(e), table))
