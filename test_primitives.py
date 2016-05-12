import unittest
import primitives
from operator import *

class PrimitivesTest(unittest.TestCase):
    def test_isatom(self):
        test_cases = (('atom', True),
                      ('turkey', True),
                      ('1492', True),
                      ('u', True),
                      ('*abc$', True),
                      ('Harry', True),
                      (('Harry', 'had', 'a', 'heap', 'of', 'apples'), False))

        for atom, expected in test_cases:
            result = primitives.isatom(atom)
            self.assertEqual(result, expected)


    def test_car(self):
        test_cases = ((('a', 'b', 'c'), 'a'),
                      ((('a', 'b', 'c'), 'x', 'y', 'z'), ('a', 'b', 'c')), 
                      (((('hotdogs', ),), ('and', ), ('pickle', ), 'relish'), (('hotdogs', ),)),
                      (((('hotdogs', ), ), ('and', )), (('hotdogs', ), )),
                      ('hotdog', None),
                      ((), None))

        for l, expected in test_cases:
            result = primitives.car(l)
            self.assertEqual(result, expected)


    def test_cdr(self):
        test_cases = ((('a', 'b', 'c'), ('b', 'c')),
                      ((('a', 'b', 'c'), 'x', 'y', 'z'), ('x', 'y', 'z')),
                      (('hamburgers', ), ()),
                      ('hotdogs', None),
                      ((), None))

        for l, expected in test_cases:
            result = primitives.cdr(l)
            self.assertEqual(result, expected)


    def test_cons(self):
        test_cases = (('peanut',
                       ('butter', 'and', 'jelly'),
                       ('peanut', 'butter', 'and', 'jelly')),
                      (('banana', 'and'),
                       ('peanut', 'butter', 'and', 'jelly'),
                       (('banana', 'and'), 'peanut', 'butter', 'and', 'jelly')),
                      ((('help', ), 'this'),
                       ('is', 'very', 'hard', 'to', 'learn'),
                       ((('help', ), 'this'), 'is', 'very', 'hard', 'to', 'learn')),
                      (('a', 'b', 'c'),
                       'b',
                       None),
                      ('a', 'b', None))

        for s, l, expected in test_cases:
            result = primitives.cons(s, l)
            self.assertEqual(result, expected)


    def test_isnull(self):
        test_cases = (((), True),
                      (('a', 'b', 'c'), False),
                      ('spaghetti', None))

        for l, expected in test_cases:
            result = primitives.isnull(l)
            self.assertEqual(result, expected)


    def test_iseq(self):
        test_cases = (('Harry', 'Harry', True),
                      ('margarine', 'butter', False),
                      ((), ('strawberry', ), None))

        for alpha, beta, expected in test_cases:
            result = primitives.iseq(alpha, beta)
            self.assertEqual(result, expected)
