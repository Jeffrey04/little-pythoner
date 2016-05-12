import unittest
import schemer
from operator import *

class PreprocessorTest(unittest.TestCase):
    def test_isatom(self):
        test_cases = (('atom', True),
                      ('turkey', True),
                      ('1492', True),
                      ('u', True),
                      ('*abc$', True),
                      (14, True),
                      (-3, False),
                      (3.14159, False))

        for atom, expected in test_cases:
            result = schemer.isatom(atom)
            self.assertEqual(result, expected)

    def test_islat(self):
        test_cases = ((('Jack', 'Sprat', 'could', 'eat', 'no', 'chicken', 'fat'), True),
                      ((('Jack', ), 'Sprat', 'could', 'eat', 'no', 'chicken', 'fat'), False),
                      (('Jack', ('Sprat', 'could'), 'eat', 'no', 'chicken', 'fat'), False),
                      ((), True),
                      (((('tomato', 'sauce'),), (('bean', ), 'sauce'), ('and', (('flying', ), ), 'sauce')),
                       False))

        for atom, expected in test_cases:
            result = schemer.islat(atom)
            self.assertEqual(result, expected)

    def test_ismember(self):
        test_cases = (('poached', ('fried', 'eggs', 'and', 'scrambled', 'eggs'), False),
                      ('meat', ('mashed', 'potatoes', 'and', 'meat', 'gravy'), True),
                      ('liver', ('bagels', 'and', 'lox'), False))

        for atom, lat, expected in test_cases:
            result = schemer.ismember(atom, lat)
            self.assertEqual(result, expected)

    def test_rember(self):
        test_cases = (('mint',
                       ('lamb', 'chops', 'and', 'mint', 'jelly'),
                       ('lamb', 'chops', 'and', 'jelly')),
                      ('mint',
                       ('lamb', 'chops', 'and', 'mint', 'flavored', 'mint', 'jelly'),
                       ('lamb', 'chops', 'and', 'flavored', 'mint', 'jelly')),
                      ('toast',
                       ('bacon', 'lettuce', 'and', 'tomato'),
                       ('bacon', 'lettuce', 'and', 'tomato')),
                      ('cup',
                       ('coffee', 'cup', 'tea', 'cup', 'and', 'hick', 'cup'),
                       ('coffee', 'tea', 'cup', 'and', 'hick', 'cup')),
                      ('and',
                       ('bacon', 'lettuce', 'and', 'tomato'),
                       ('bacon', 'lettuce', 'tomato')),
                      ('sauce',
                       ('soy', 'sauce', 'and', 'tomato', 'sauce'),
                       ('soy', 'and', 'tomato', 'sauce')))

        for atom, lat, expected in test_cases:
            result = schemer.rember(atom, lat)
            self.assertEqual(result, expected)

    def test_firsts(self):
        test_cases = (((('apple', 'peach', 'pumpkin'),
                        ('plum', 'pear', 'cherry'),
                        ('grape', 'raisin', 'pea'),
                        ('bean', 'carrot', 'eggplant')),
                       ('apple', 'plum', 'grape', 'bean')),
                      ((('a', 'b'),
                        ('c', 'd'),
                        ('e', 'f')),
                       ('a', 'c', 'e')),
                      ((), ()),
                      ((('five', 'plums'),
                        ('four', ),
                        ('eleven', 'green', 'oranges')),
                       ('five', 'four', 'eleven')),
                      (((('five', 'plums'), 'four'),
                        ('eleven', 'green', 'oranges'),
                        (('no', ), 'more')),
                       (('five', 'plums'), 'eleven', ('no', ))))

        for lat, expected in test_cases:
            result = schemer.firsts(lat)
            self.assertEqual(result, expected)

    def test_insertR(self):
        test_cases = (('topping',
                       'fudge',
                       ('ice', 'cream', 'with', 'fudge', 'for', 'dessert'),
                       ('ice', 'cream', 'with', 'fudge', 'topping', 'for', 'dessert')),
                      ('jalapeno',
                       'and',
                       ('tacos', 'tamales', 'and', 'salsa'),
                       ('tacos', 'tamales', 'and', 'jalapeno', 'salsa')),
                      ('e',
                       'd',
                       ('a', 'b', 'c', 'd', 'f', 'g', 'h'),
                       ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')))

        for new, old, lat, expected in test_cases:
            result = schemer.insertR(new, old, lat)
            self.assertEqual(result, expected)

    def test_insertL(self):
        test_cases = (('topping',
                       'fudge',
                       ('ice', 'cream', 'with', 'fudge', 'for', 'dessert'),
                       ('ice', 'cream', 'with', 'topping', 'fudge', 'for', 'dessert')),
                      ('jalapeno',
                       'and',
                       ('tacos', 'tamales', 'and', 'salsa'),
                       ('tacos', 'tamales', 'jalapeno', 'and', 'salsa')),
                      ('e',
                       'd',
                       ('a', 'b', 'c', 'd', 'f', 'g', 'h'),
                       ('a', 'b', 'c', 'e', 'd', 'f', 'g', 'h')))

        for new, old, lat, expected in test_cases:
            result = schemer.insertL(new, old, lat)
            self.assertEqual(result, expected)

    def test_subst(self):
        test_cases = (('topping',
                       'fudge',
                       ('ice', 'cream', 'with', 'fudge', 'for', 'dessert'),
                       ('ice', 'cream', 'with', 'topping', 'for', 'dessert')),
                      ('jalapeno',
                       'and',
                       ('tacos', 'tamales', 'and', 'salsa'),
                       ('tacos', 'tamales', 'jalapeno', 'salsa')),
                      ('e',
                       'd',
                       ('a', 'b', 'c', 'd', 'f', 'g', 'h'),
                       ('a', 'b', 'c', 'e', 'f', 'g', 'h')))

        for new, old, lat, expected in test_cases:
            result = schemer.subst(new, old, lat)
            self.assertEqual(result, expected)

    def test_subst2(self):
        test_cases = (('vanilla',
                       'chocolate',
                       'banana',
                       ('banana', 'ice', 'cream', 'with', 'chocolate', 'topping'),
                       ('vanilla', 'ice', 'cream', 'with', 'chocolate', 'topping')), )

        for new, o1, o2, lat, expected in test_cases:
            result = schemer.subst2(new, o1, o2, lat)
            self.assertEqual(result, expected)

    def test_multirember(self):
        test_cases = (('cup',
                       ('coffee', 'cup', 'tea', 'cup', 'and', 'hick', 'cup'),
                       ('coffee', 'tea', 'and', 'hick')),)

        for atom, lat, expected in test_cases:
            result = schemer.multirember(atom, lat)
            self.assertEqual(result, expected)

    def test_multiinsertR(self):
        test_cases = (('fried',
                       'fish',
                       ('chips', 'and', 'fish', 'or', 'fish', 'and', 'fried'),
                       ('chips', 'and', 'fish', 'fried', 'or', 'fish', 'fried', 'and', 'fried')),)

        for new, old, lat, expected in test_cases:
            result = schemer.multiinsertR(new, old, lat)
            self.assertEqual(result, expected)

    def test_multiinsertL(self):
        test_cases = (('fried',
                       'fish',
                       ('chips', 'and', 'fish', 'or', 'fish', 'and', 'fried'),
                       ('chips', 'and', 'fried', 'fish', 'or', 'fried', 'fish', 'and', 'fried')),)

        for new, old, lat, expected in test_cases:
            result = schemer.multiinsertL(new, old, lat)
            self.assertEqual(result, expected)

    def test_subst(self):
        test_cases = (('fried',
                       'fish',
                       ('chips', 'and', 'fish', 'or', 'fish', 'and', 'fried'),
                       ('chips', 'and', 'fried', 'or', 'fried', 'and', 'fried')),)

        for new, old, lat, expected in test_cases:
            result = schemer.multisubst(new, old, lat)
            self.assertEqual(result, expected)

    def test_add1(self):
        test_cases = ((67, 68),)

        for atom, expected in test_cases:
            result = schemer.add1(atom)
            self.assertEqual(result, expected)

    def test_sub1(self):
        test_cases = ((5, 4),
                      (0, -1))

        for atom, expected in test_cases:
            result = schemer.sub1(atom)
            self.assertEqual(result, expected)

    def test_iszero(self):
        test_cases = ((0, True),
                      (1492, False))

        for atom, expected in test_cases:
            result = schemer.iszero(atom)
            self.assertEqual(result, expected)

    def test_add(self):
        test_cases = ((46, 12, 58),)

        for n, m, expected in test_cases:
            result = schemer._add(n, m)
            self.assertEqual(result, expected)

    def test_sub(self):
        test_cases = ((14, 3, 11),
                      (17, 9, 8),
                      (18, 25, -1))

        for n, m, expected in test_cases:
            result = schemer._sub(n, m)
            self.assertEqual(result, expected)

    def test_addtup(self):
        test_cases = (((3, 5, 2, 8), 18),
                      ((15, 6, 7, 12, 3), 43))

        for tup, expected in test_cases:
            result = schemer.addtup(tup)
            self.assertEqual(result, expected)

    def test_mul(self):
        test_cases = ((5, 3, 15),
                      (13, 4, 52),
                      (12, 3, 36))

        for n, m, expected in test_cases:
            result = schemer._mul(n, m)
            self.assertEqual(result, expected)

    def test_tupplus(self):
        test_cases = (((3, 6, 9, 11, 4),
                       (8, 5, 2, 0, 7),
                       (11, 11, 11, 11, 11)),
                      ((2, 3),
                       (4, 6),
                       (6, 9)),
                      ((3, 7),
                       (4, 6),
                       (7, 13)),
                      ((3, 7),
                       (4, 6, 8, 1),
                       (7, 13, 8, 1)),
                      ((3, 7, 8, 1),
                       (4, 6),
                       (7, 13, 8, 1)))

        for tup1, tup2, expected in test_cases:
            result = schemer.tupplus(tup1, tup2)
            self.assertEqual(result, expected)

    def test_gt(self):
        test_cases = ((12, 133, False),
                      (120, 11, True),
                      (3, 3, False))

        for n, m, expected in test_cases:
            result = schemer._gt(n, m)
            self.assertEqual(result, expected)

    def test_lt(self):
        test_cases = ((4, 6, True),
                      (8, 3, False),
                      (6, 6, False))

        for n, m, expected in test_cases:
            result = schemer._lt(n, m)
            self.assertEqual(result, expected)

    def test_eq(self):
        test_cases = ((3, 3, True),
                      (8, 3, False),
                      (6, 6, True))

        for n, m, expected in test_cases:
            result = schemer._eq(n, m)
            self.assertEqual(result, expected)

    def test_eq2(self):
        test_cases = ((3, 3, True),
                      (8, 3, False),
                      (6, 6, True))

        for n, m, expected in test_cases:
            result = schemer._eq2(n, m)
            self.assertEqual(result, expected)

    def test_pow(self):
        test_cases = ((1, 1, 1),
                      (2, 3, 8),
                      (5, 3, 125))

        for n, m, expected in test_cases:
            result = schemer._pow(n, m)
            self.assertEqual(result, expected)

    def test_div(self):
        test_cases = ((15, 4, 3),)

        for n, m, expected in test_cases:
            result = schemer._div(n, m)
            self.assertEqual(result, expected)

    def test_length(self):
        test_cases = ((('hotdogs', 'with', 'mustard', 'sauerkraurt', 'and', 'pickles'), 6),
                      (('ham', 'and', 'cheese', 'on', 'rye'), 5))

        for lat, expected in test_cases:
            result = schemer.length(lat)
            self.assertEqual(result, expected)

    def test_pick(self):
        test_cases = ((4,
                       ('lassagna', 'spaghetti', 'ravioli', 'macaroni', 'meatball'),
                       'macaroni'),
                      (0,
                       ('a', ),
                       -1))

        for n, lat, expected in test_cases:
            result = schemer.pick(n, lat)
            self.assertEqual(result, expected)

    def test_rempick(self):
        test_cases = ((3,
                       ('hotdogs', 'with', 'hot', 'mustard'),
                       ('hotdogs', 'with', 'mustard')),)

        for n, lat, expected in test_cases:
            result = schemer.rempick(n, lat)
            self.assertEqual(result, expected)

    def test_rempick2(self):
        test_cases = ((3,
                       ('hotdogs', 'with', 'hot', 'mustard'),
                       ('hotdogs', 'with', 'mustard')),
                      (3,
                       ('lemon', 'meringue', 'salty', 'pie'),
                       ('lemon', 'meringue', 'pie')))

        for n, lat, expected in test_cases:
            result = schemer.rempick2(n, lat)
            self.assertEqual(result, expected)

    def test_no_nums(self):
        test_cases = (((5, 'pears', 6, 'prunes', 9, 'dates'),
                       ('pears', 'prunes', 'dates')),)

        for lat, expected in test_cases:
            result = schemer.no_nums(lat)
            self.assertEqual(result, expected)

    def test_all_nums(self):
        test_cases = (((5, 'pears', 6, 'prunes', 9, 'dates'),
                       (5, 6, 9)),)

        for lat, expected in test_cases:
            result = schemer.all_nums(lat)
            self.assertEqual(result, expected)

    def test_isegan(self):
        test_cases = ((1, 1, True),
                      (1, 2, False),
                      ('one', 'one', True),
                      ('one', 'two', False),
                      (1, 'one', False))

        for a1, a2, expected in test_cases:
            result = schemer.isegan(a1, a2)
            self.assertEqual(result, expected)

    def test_occur(self):
        test_cases = (('a',
                       ('a', 'a', 'b'),
                       2),
                      ('c',
                       ('a', 'a', 'b'),
                       0))

        for atom, lat, expected in test_cases:
            result = schemer.occur(atom, lat)
            self.assertEqual(result, expected)

    def test_isone(self):
        test_cases = ((1, True),
                      ('one', False),
                      (2, False))

        for atom, expected in test_cases:
            result = schemer.isone(atom)
            self.assertEqual(result, expected)

    def test_rember_star(self):
        test_cases = (('cup',
                       (('coffee', ), 'cup', (('tea', ), 'cup'), ('and', ('hick', ), 'cup')),
                       (('coffee', ), (('tea', ), ), ('and', ('hick', )))),
                      ('sauce',
                       ((('tomato', 'sauce'),), (('bean', ), 'sauce'), ('and', (('flying', ), ), 'sauce')),
                       ((('tomato',),), (('bean',), ), ('and', (('flying', ),)))))

        for atom, _list, expected in test_cases:
            result = schemer.rember_star(atom, _list)
            self.assertEqual(result, expected)

    def test_insertL_star(self):
        test_cases = (('roast',
                       'chuck',
                       ((('how', 'much', ('wood', ), ), ),
                        'cound',
                        (('a', ('wood', ), 'chuck')),
                        ((('chuck', ), ), ),
                        ('if', ('a', ), ('woodchuck', ), ),
                        'could', 'chuck', 'wood'),
                       ((('how', 'much', ('wood', ), ), ),
                        'cound',
                        (('a', ('wood', ), 'roast', 'chuck')),
                        ((('roast', 'chuck', ), ), ),
                        ('if', ('a', ), ('woodchuck', ), ),
                        'could', 'roast', 'chuck', 'wood')),)

        for new, old, _list, expected in test_cases:
            result = schemer.insertL_star(new, old, _list)
            self.assertEqual(result, expected)

    def test_insertR_star(self):
        test_cases = (('roast',
                       'chuck',
                       ((('how', 'much', ('wood', ), ), ),
                        'cound',
                        (('a', ('wood', ), 'chuck')),
                        ((('chuck', ), ), ),
                        ('if', ('a', ), ('woodchuck', ), ),
                        'could', 'chuck', 'wood'),
                       ((('how', 'much', ('wood', ), ), ),
                        'cound',
                        (('a', ('wood', ), 'chuck', 'roast')),
                        ((('chuck', 'roast', ), ), ),
                        ('if', ('a', ), ('woodchuck', ), ),
                        'could', 'chuck', 'roast', 'wood')),)

        for new, old, _list, expected in test_cases:
            result = schemer.insertR_star(new, old, _list)
            self.assertEqual(result, expected)

    def test_occur_star(self):
        test_cases = (('banana',
                       (('banana', ),
                         ('split', ((('banana', 'ice'), ), ),
                          ('cream', ('banana', )),
                          'sherbet'),
                         ('banana', ),
                         ('bread'),
                         ('banana', 'brandy')),
                       5), )

        for atom, _list, expected in test_cases:
            result = schemer.occur_star(atom, _list)
            self.assertEqual(result, expected)

    def test_subst_star(self):
        test_cases = (('orange',
                       'banana',
                       (('banana', ),
                         ('split', ((('banana', 'ice'), ), ),
                          ('cream', ('banana', )),
                          'sherbet'),
                         ('banana', ),
                         ('bread'),
                         ('banana', 'brandy')),
                       (('orange', ),
                         ('split', ((('orange', 'ice'), ), ),
                          ('cream', ('orange', )),
                          'sherbet'),
                         ('orange', ),
                         ('bread'),
                         ('orange', 'brandy'))), )

        for new, old, _list, expected in test_cases:
            result = schemer.subst_star(new, old, _list)
            self.assertEqual(result, expected)

    def test_member_star(self):
        test_cases = (('chips',
                       (('potato', ), ('chips', (('with', ), 'fish'), ('chips', ))),
                       True), )

        for atom, _list, expected in test_cases:
            result = schemer.member_star(atom, _list)
            self.assertEqual(result, expected)

    def test_leftmost(self):
        test_cases = (((('potato', ), ('chips', (('with', ), 'fish'), ('chips', ))),
                       'potato'),
                      (((('hot', ), ('tuna', ('and', ))), 'cheese'),
                       'hot'))

        for _list, expected in test_cases:
            result = schemer.leftmost(_list)
            self.assertEqual(result, expected)

    def test_iseqlist(self):
        test_cases = ((('strawberry', 'ice', 'cream'),
                       ('strawberry', 'ice', 'cream'),
                       True),
                      (('strawberry', 'ice', 'cream'),
                       ('strawberry', 'cream', 'ice'),
                       False),
                      (('banana', (('split', ), )),
                       (('banana', ), ('split', )),
                       False),
                      (('beef', (('sausage', ), ), ('and', ('soda', ))),
                       ('beef', (('salami', ), ), ('and', ('soda', ))),
                       False),
                      (('beef', (('sausage', ), ), ('and', ('soda', ))),
                       ('beef', (('sausage', ), ), ('and', ('soda', ))),
                       True))

        for _l1, _l2, expected in test_cases:
            result = schemer.iseqlist(_l1, _l2)
            self.assertEqual(result, expected)

    def test_equal(self):
        test_cases = ((('strawberry', 'ice', 'cream'),
                       ('strawberry', 'ice', 'cream'),
                       True),
                      (('strawberry', 'ice', 'cream'),
                       ('strawberry', 'cream', 'ice'),
                       False),
                      (('banana', (('split', ), )),
                       (('banana', ), ('split', )),
                       False),
                      (('beef', (('sausage', ), ), ('and', ('soda', ))),
                       ('beef', (('salami', ), ), ('and', ('soda', ))),
                       False),
                      (('beef', (('sausage', ), ), ('and', ('soda', ))),
                       ('beef', (('sausage', ), ), ('and', ('soda', ))),
                       True),
                      ('a', 'a', True),
                      (1, 2, False))

        for _s1, _s2, expected in test_cases:
            result = schemer.isequal(_s1, _s2)
            self.assertEqual(result, expected)

    def test_iseqlist2(self):
        test_cases = ((('strawberry', 'ice', 'cream'),
                       ('strawberry', 'ice', 'cream'),
                       True),
                      (('strawberry', 'ice', 'cream'),
                       ('strawberry', 'cream', 'ice'),
                       False),
                      (('banana', (('split', ), )),
                       (('banana', ), ('split', )),
                       False),
                      (('beef', (('sausage', ), ), ('and', ('soda', ))),
                       ('beef', (('salami', ), ), ('and', ('soda', ))),
                       False),
                      (('beef', (('sausage', ), ), ('and', ('soda', ))),
                       ('beef', (('sausage', ), ), ('and', ('soda', ))),
                       True))

        for _l1, _l2, expected in test_cases:
            result = schemer.iseqlist2(_l1, _l2)
            self.assertEqual(result, expected)

    def test_rember2(self):
        test_cases = (('mint',
                       ('lamb', 'chops', 'and', 'mint', 'jelly'),
                       ('lamb', 'chops', 'and', 'jelly')),
                      ('mint',
                       ('lamb', 'chops', 'and', 'mint', 'flavored', 'mint', 'jelly'),
                       ('lamb', 'chops', 'and', 'flavored', 'mint', 'jelly')),
                      ('toast',
                       ('bacon', 'lettuce', 'and', 'tomato'),
                       ('bacon', 'lettuce', 'and', 'tomato')),
                      ('cup',
                       ('coffee', 'cup', 'tea', 'cup', 'and', 'hick', 'cup'),
                       ('coffee', 'tea', 'cup', 'and', 'hick', 'cup')),
                      ('and',
                       ('bacon', 'lettuce', 'and', 'tomato'),
                       ('bacon', 'lettuce', 'tomato')),
                      ('sauce',
                       ('soy', 'sauce', 'and', 'tomato', 'sauce'),
                       ('soy', 'and', 'tomato', 'sauce')))

        for atom, lat, expected in test_cases:
            result = schemer.rember2(atom, lat)
            self.assertEqual(result, expected)

    def test_isnumbered(self):
        test_cases = ((1, True),
                      ((3, '+', (4, '^', 5)), True),
                      ((2, '*', 'sausage'), False))

        for aexp, expected in test_cases:
            result = schemer.isnumbered(aexp)
            self.assertEqual(result, expected)

    def test_value(self):
        test_cases = ((13, 13),
                      ((1, '+', 3), 4),
                      ((1, '+', (3, '^', 4)), 82))

        for nexp, expected in test_cases:
            result = schemer.value(nexp)
            self.assertEqual(result, expected)

    def test_isset(self):
        test_cases = ((('apple', 'peaches', 'apple', 'plum'), False),
                      (('apples', 'peaches', 'pears', 'plums'), True),
                      ((), True),
                      (('apple', 3, 'pear', 4, 9, 'apple', 3, 4), False))

        for lat, expected in test_cases:
            result = schemer.isset(lat)
            self.assertEqual(result, expected)

    def test_makeset(self):
        test_cases = ((('apple', 'peach', 'pear', 'peach', 'plum', 'apple', 'lemon', 'peach'),
                       ('apple', 'peach', 'pear', 'plum', 'lemon')), )

        for lat, expected in test_cases:
            result = schemer.makeset(lat)
            self.assertEqual(result, expected)

    def test_issubset(self):
        test_cases = (((5, 'chicken', 'wings'),
                       (5, 'hamburgers', 2, 'pieces', 'fried', 'chicken', 'and', 'light', 'duckling', 'wings'),
                       True),
                      ((4, 'pounds', 'of', 'horseradish'),
                       ('four', 'pounds', 'chicken', 'and', 5, 'ounces', 'horseradish'),
                       False))

        for set1, set2, expected in test_cases:
            result = schemer.issubset(set1, set2)
            self.assertEqual(result, expected)

    def test_iseqset(self):
        test_cases = (((6, 'large', 'chickens', 'with', 'wings'),
                       (6, 'chickens', 'with', 'large', 'wings'),
                       True), )

        for set1, set2, expected in test_cases:
            result = schemer.iseqset(set1, set2)
            self.assertEqual(result, expected)

    def test_isintersect(self):
        test_cases = ((('stewed', 'tomatoes', 'and', 'macaroni'),
                       ('macaroni', 'and', 'cheese'),
                       True), )

        for set1, set2, expected in test_cases:
            result = schemer.isintersect(set1, set2)
            self.assertEqual(result, expected)

    def test_intersect(self):
        test_cases = ((('stewed', 'tomatoes', 'and', 'macaroni'),
                       ('macaroni', 'and', 'cheese'),
                       ('and', 'macaroni')), )

        for set1, set2, expected in test_cases:
            result = schemer.intersect(set1, set2)
            self.assertEqual(result, expected)

    def test_union(self):
        test_cases = ((('stewed', 'tomatoes', 'and', 'macaroni', 'casserole'),
                       ('macaroni', 'and', 'cheese'),
                       ('stewed', 'tomatoes', 'casserole', 'macaroni', 'and', 'cheese')), )

        for set1, set2, expected in test_cases:
            result = schemer.union(set1, set2)
            self.assertEqual(result, expected)

    def test_intersectall(self):
        test_cases = (((('a', 'b', 'c'), ('c', 'a', 'd', 'e'), ('e', 'f', 'g', 'h', 'a', 'b')),
                       ('a', )),
                      (((6, 'pears', 'and'),
                        (3, 'peaches', 'and', 6, 'peppers'),
                        (8, 'pears', 'and', 6, 'plums'),
                        ('and', 6, 'prunes', 'with', 'some', 'apples')),
                       (6, 'and')), )

        for l_set, expected in test_cases:
            result = schemer.intersectall(l_set)
            self.assertEqual(result, expected)

    def test_ispair(self):
        test_cases = ((('pear', 'pear'), True),
                      ((3, 7), True),
                      (((2, ), ('pair', )), True),
                      (('full', ('house', )), True))

        for pair, expected in test_cases:
            result = schemer.isapair(pair)
            self.assertEqual(result, expected)

    #def test_isrel(self):
    #    test_cases = ((('apples', 'peaches', 'pumpkin', 'pie'), False),
    #                  ((('apples', 'peaches'), ('pumpkin', 'pie'), ('apples', 'peaches')), False),
    #                  ((('apples', 'peaches'), ('pumpkin', 'pie')), True),
    #                  (((4, 3), (4, 2), (7, 6), (6, 2), (3, 4)), True))

    #    for rel, expected in test_cases:
    #        result = schemer.isrel(rel)
    #        self.assertEqual(result, expected)

    def test_isfun(self):
        test_cases = ((((4, 3), (4, 2), (7, 6), (6, 2), (3, 4)), False),
                      (((8, 3), (4, 2), (7, 6), (6, 2), (3, 4)), True),
                      ((('d', 4), ('b', 0), ('b', 9), ('e', 5), ('g', 4)), False))

        for rel, expected in test_cases:
            result = schemer.isfun(rel)
            self.assertEqual(result, expected)

    def test_revrel(self):
        test_cases = ((((8, 'a'), ('pumpkin', 'pie'), ('got', 'sick')),
                       (('a', 8), ('pie', 'pumpkin'), ('sick', 'got'))), )

        for rel, expected in test_cases:
            result = schemer.revrel(rel)
            self.assertEqual(result, expected)

    def test_revrel2(self):
        test_cases = ((((8, 'a'), ('pumpkin', 'pie'), ('got', 'sick')),
                       (('a', 8), ('pie', 'pumpkin'), ('sick', 'got'))), )

        for rel, expected in test_cases:
            result = schemer.revrel2(rel)
            self.assertEqual(result, expected)

    def test_isfullfun(self):
        test_cases = ((((8, 3), (4, 2), (7, 6), (6, 2), (3, 4)), False),
                      (((8, 3), (4, 8), (7, 6), (6, 2), (3, 4)), True),
                      ((('grape', 'raisin'), ('plum', 'prune'), ('stewed', 'prune')), False),
                      ((('grape', 'raisin'), ('plum', 'prune'), ('stewed', 'grape')), True))

        for rel, expected in test_cases:
            result = schemer.isfullfun(rel)
            self.assertEqual(result, expected)

    def test_isone_to_one(self):
        test_cases = ((((8, 3), (4, 2), (7, 6), (6, 2), (3, 4)), False),
                      (((8, 3), (4, 8), (7, 6), (6, 2), (3, 4)), True),
                      ((('grape', 'raisin'), ('plum', 'prune'), ('stewed', 'prune')), False),
                      ((('grape', 'raisin'), ('plum', 'prune'), ('stewed', 'grape')), True),
                      ((('chocolate', 'chip'), ('doughy', 'cookie')), True))

        for rel, expected in test_cases:
            result = schemer.isone_to_one(rel)
            self.assertEqual(result, expected)

    def test_insertL2(self):
        test_cases = (('topping',
                       'fudge',
                       ('ice', 'cream', 'with', 'fudge', 'for', 'dessert'),
                       ('ice', 'cream', 'with', 'topping', 'fudge', 'for', 'dessert')),
                      ('jalapeno',
                       'and',
                       ('tacos', 'tamales', 'and', 'salsa'),
                       ('tacos', 'tamales', 'jalapeno', 'and', 'salsa')),
                      ('e',
                       'd',
                       ('a', 'b', 'c', 'd', 'f', 'g', 'h'),
                       ('a', 'b', 'c', 'e', 'd', 'f', 'g', 'h')))

        for new, old, lat, expected in test_cases:
            result = schemer.insertL2(new, old, lat)
            self.assertEqual(result, expected)

    def test_rember_f(self):
        test_cases = ((eq, 5, (6, 2, 5, 3), (6, 2, 3)),
                      (schemer.iseq, 'jelly', ('jelly', 'beans', 'are', 'good'), ('beans', 'are', 'good')))

        for fun, s, _list, expected in test_cases:
            result = schemer.rember_f(fun, s, _list)
            self.assertEqual(result, expected)

    def test_rember_f2(self):
        test_cases = ((eq, 5, (6, 2, 5, 3), (6, 2, 3)),
                      (schemer.iseq, 'jelly', ('jelly', 'beans', 'are', 'good'), ('beans', 'are', 'good')),
                      (schemer.iseq, 'tuna', ('shrimp', 'salad', 'and', 'tuna', 'salad'), ('shrimp', 'salad', 'and', 'salad')))

        for fun, s, _list, expected in test_cases:
            result = schemer.rember_f2(fun)(s, _list)
            self.assertEqual(result, expected)

    def test_insertL_f(self):
        test_cases = ((schemer.iseq,
                       'topping',
                       'fudge',
                       ('ice', 'cream', 'with', 'fudge', 'for', 'dessert'),
                       ('ice', 'cream', 'with', 'topping', 'fudge', 'for', 'dessert')),
                      (schemer.iseq,
                       'jalapeno',
                       'and',
                       ('tacos', 'tamales', 'and', 'salsa'),
                       ('tacos', 'tamales', 'jalapeno', 'and', 'salsa')),
                      (schemer.iseq,
                       'e',
                       'd',
                       ('a', 'b', 'c', 'd', 'f', 'g', 'h'),
                       ('a', 'b', 'c', 'e', 'd', 'f', 'g', 'h')))

        for fun, new, old, lat, expected in test_cases:
            result = schemer.insertL_f(fun)(new, old, lat)
            self.assertEqual(result, expected)

    def test_insertR_f(self):
        test_cases = ((schemer.iseq,
                       'topping',
                       'fudge',
                       ('ice', 'cream', 'with', 'fudge', 'for', 'dessert'),
                       ('ice', 'cream', 'with', 'fudge', 'topping', 'for', 'dessert')),
                      (schemer.iseq,
                       'jalapeno',
                       'and',
                       ('tacos', 'tamales', 'and', 'salsa'),
                       ('tacos', 'tamales', 'and', 'jalapeno', 'salsa')),
                      (schemer.iseq,
                       'e',
                       'd',
                       ('a', 'b', 'c', 'd', 'f', 'g', 'h'),
                       ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')))

        for fun, new, old, lat, expected in test_cases:
            result = schemer.insertR_f(fun)(new, old, lat)
            self.assertEqual(result, expected)

    def test_value2(self):
        test_cases = ((13, 13),
                      ((1, '+', 3), 4),
                      ((1, '+', (3, '^', 4)), 82))

        for nexp, expected in test_cases:
            result = schemer.value2(nexp)
            self.assertEqual(result, expected)

    def test_multirember_f(self):
        test_cases = ((schemer.iseq,
                       'cup',
                       ('coffee', 'cup', 'tea', 'cup', 'and', 'hick', 'cup'),
                       ('coffee', 'tea', 'and', 'hick')),
                      (schemer.iseq,
                       'tuna',
                       ('shrimp', 'salad', 'tuna', 'salad', 'and', 'tuna'),
                       ('shrimp', 'salad', 'salad', 'and')))

        for fun, atom, lat, expected in test_cases:
            result = schemer.multirember_f(fun)(atom, lat)
            self.assertEqual(result, expected)

    def test_multirember_t(self):
        test_cases = ((schemer.iseq_c('tuna'),
                       ('shrimp', 'salad', 'tuna', 'salad', 'and', 'tuna'),
                       ('shrimp', 'salad', 'salad', 'and')),)

        for fun, lat, expected in test_cases:
            result = schemer.multirember_t(fun, lat)
            self.assertEqual(result, expected)

    def test_multirember_n_co(self):
        test_cases = (('tuna',
                       (),
                       schemer.a_friend,
                       True),
                      ('tuna',
                       ('tuna',),
                       schemer.a_friend,
                       False))

        for a, lat, col, expected in test_cases:
            result = schemer.multirember_n_co(a, lat, col)
            self.assertEqual(result, expected)

    def test_evens_only_star(self):
        test_cases = ((((9, 1, 2, 8), 3, 10, ((9, 9), 7, 6), 2),
                       ((2, 8), 10, ((), 6), 2)), )

        for _list, expected in test_cases:
            result = schemer.evens_only_star(_list)
            self.assertEqual(result, expected)

    def test_evens_only_star(self):
        import sys
        sys.setrecursionlimit(2000)
        the_last_friend = lambda newl, product, _sum: schemer.cons(_sum, schemer.cons(product, newl))

        test_cases = ((((9, 1, 2, 8), 3, 10, ((9, 9), 7, 6), 2),
                       (38, 1920, (2, 8), 10, ((), 6), 2)),)

        for _list, expected in test_cases:
            result = schemer.evens_only_star_n_co(_list, the_last_friend)
            self.assertEqual(result, expected)

    def test_looking(self):
        test_cases = (('caviar',
                       (6, 2, 4, 'caviar', 5, 7, 3),
                       True),
                      ('caviar',
                       (6, 2, 'grits', 'caviar', 5, 7, 3),
                       False))

        for atom, lat, expected in test_cases:
            result = schemer.looking(atom, lat)
            self.assertEqual(result, expected)

    def test_shift(self):
        test_cases = (((('a', 'b'), 'c'),
                       ('a', ('b', 'c'))),
                      ((('a', 'b'), ('c', 'd')),
                       ('a', ('b', ('c', 'd')))))

        for pair, expected in test_cases:
            result = schemer.shift(pair)
            self.assertEqual(result, expected)

    def test_lengths(self):
        test_cases = ((schemer.length_0,
                       (),
                       0),
                      (schemer.length_1,
                       (1,),
                       1),
                      (schemer.length_2,
                       (1, 2),
                       2),
                      (schemer._length_0,
                       (),
                       0),
                      (schemer._length_1,
                       (1,),
                       1))

        for fun, l, expected in test_cases:
            result = fun(l)
            self.assertEqual(result, expected)

    def test_length2(self):
        test_cases = ((('hotdogs', 'with', 'mustard', 'sauerkraurt', 'and', 'pickles'), 6),
                      (('ham', 'and', 'cheese', 'on', 'rye'), 5))

        for lat, expected in test_cases:
            result = schemer.length2(lat)
            self.assertEqual(result, expected)

    def test_length3(self):
        test_cases = ((('hotdogs', 'with', 'mustard', 'sauerkraurt', 'and', 'pickles'), 6),
                      (('ham', 'and', 'cheese', 'on', 'rye'), 5))

        for lat, expected in test_cases:
            result = schemer.length3(lat)
            self.assertEqual(result, expected)

    def test_length4(self):
        test_cases = ((('hotdogs', 'with', 'mustard', 'sauerkraurt', 'and', 'pickles'), 6),
                      (('ham', 'and', 'cheese', 'on', 'rye'), 5))

        for lat, expected in test_cases:
            result = schemer.length4(lat)
            self.assertEqual(result, expected)

    def test_lookup_in_table(self):
        test_cases = (('entree',
                       ((('entree', 'dessert'), ('spaghetti', 'spumoni')), (('appetizer', 'entree', 'beverage'),('food', 'tastes', 'good'))),
                       lambda name: None,
                       'spaghetti'), )

        for name, table, table_f, expected in test_cases:
            result = schemer.lookup_in_table(name, table, table_f)
            self.assertEqual(result, expected)
