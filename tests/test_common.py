from unittest import TestCase

from abconfig import ABConfig
from abconfig.common import Item, Dict, Type


class TestType(TestCase):
    all_types = Type.__types__[0] + Type.__types__[1]
    all_items = (1,1.5,'1',True,[1,2,3],(1,2,3),{1,2,3},frozenset([1,2,3]))

    def test_is_type(self):
        for t,i in zip(self.all_types * 2, self.all_items + self.all_types):
            self.assertEqual(t, Type.is_type(i))

    def test_is_list(self):
        for i in self.all_items[4:]:
            self.assertEqual(True, Type.is_list(i))
        for i in self.all_items[:4]:
            self.assertEqual(False, Type.is_list(i))

    def test_is_dict(self):
        et = {'test': 123}
        dicts = [i(et) for i in Dict.__supported_classes__]

        for i in dicts:
            self.assertEqual(Dict.is_dict(i), True)

        for i in TestType.all_items:
            self.assertEqual(Dict.is_dict(i), False)


class TestItem(TestCase):
    def test_mempty(self):
        for sub_set in Item.__types__:
            for x in sub_set:
                self.assertEqual(
                    Item(Item.__mempty__) + x,
                    Item(x) + Item.__mempty__
                )

    def test_associativity(self):
        for sub_set in Item.__types__:
            for t in sub_set:
                self.assertEqual(
                    Item(Item(1) + 2) + 3,
                    Item(1) + (Item(2) + 3)
                )

    def test_int(self):
        values = [int, 3]
        for x in values:
            self.assertEqual(Item(x) + 1, 1)
            self.assertEqual(Item(x) + 1.0, 1)
            self.assertEqual(Item(x) + '1', 1)
            self.assertEqual(Item(x) + True, 1)
            self.assertEqual(Item(x) + False, 0)
            # convert errors
            self.assertRaises(ValueError, lambda: Item(x) + 'a')
            self.assertRaises(TypeError, lambda: Item(x) + [1,2])
            self.assertRaises(TypeError, lambda: Item(x) + (1,2))
            self.assertRaises(TypeError, lambda: Item(x) + {1,2})

    def test_float(self):
        values = [float, 1.0]
        for x in values:
            self.assertEqual(Item(x) + 1.0, 1.0)
            self.assertEqual(Item(x) + 1, 1.0)
            self.assertEqual(Item(x) + '1', 1.0)
            self.assertEqual(Item(x) + True, 1.0)
            self.assertEqual(Item(x) + False, 0.0)
            # convert errors
            self.assertRaises(ValueError, lambda: Item(x) + 'a')
            self.assertRaises(TypeError, lambda: Item(x) + [1,2])
            self.assertRaises(TypeError, lambda: Item(x) + (1,2))
            self.assertRaises(TypeError, lambda: Item(x) + {1,2})

    def test_str(self):
        values = [str, '1']
        for x in values:
            self.assertEqual(Item(x) + 'a', 'a')
            self.assertEqual(Item(x) + 1, '1')
            self.assertEqual(Item(x) + 1.0, '1.0')
            self.assertEqual(Item(x) + True, 'True')
            self.assertEqual(Item(x) + False, 'False')
            # convert errors
            self.assertRaises(TypeError, lambda: Item(x) + [1,2])
            self.assertRaises(TypeError, lambda: Item(x) + (1,2))
            self.assertRaises(TypeError, lambda: Item(x) + {1,2})

    def test_bool(self):
        values = [bool, True, False]
        for x in values:
            self.assertEqual(Item(x) + True, True)
            self.assertEqual(Item(x) + 'True', True)
            self.assertEqual(Item(x) + 1, True)
            self.assertEqual(Item(x) + 1.0, True)
            self.assertEqual(Item(x) + False, False)
            # convert errors
            self.assertRaises(TypeError, lambda: Item(x) + [1,2])
            self.assertRaises(TypeError, lambda: Item(x) + (1,2))
            self.assertRaises(TypeError, lambda: Item(x) + {1,2})

    def test_list(self):
        values = [[1,2,3],]
        for x in values:
            self.assertEqual(Item(x) + [4,5,6], [4,5,6])
            self.assertEqual(Item(x) + (4,5,6), [4,5,6])
            self.assertEqual(Item(x) + {4,5,6}, [4,5,6])
            # convert errors
            self.assertRaises(TypeError, lambda: Item(x) + 1)
            self.assertRaises(TypeError, lambda: Item(x) + 1.0)
            self.assertRaises(ValueError, lambda: Item(x) + 'a')
            self.assertRaises(TypeError, lambda: Item(x) + True)

    def test_tuple(self):
        values = [(1,2,3),]
        for x in values:
            self.assertEqual(Item(x) + [4,5,6], (4,5,6))
            self.assertEqual(Item(x) + (4,5,6), (4,5,6))
            self.assertEqual(Item(x) + {4,5,6}, (4,5,6))
            # convert errors
            self.assertRaises(TypeError, lambda: Item(x) + 1)
            self.assertRaises(TypeError, lambda: Item(x) + 1.0)
            self.assertRaises(ValueError, lambda: Item(x) + 'a')
            self.assertRaises(TypeError, lambda: Item(x) + True)

    def test_set(self):
        values = [{1,2,3},]
        for x in values:
            self.assertEqual(Item(x) + [4,5,6], {4,5,6})
            self.assertEqual(Item(x) + (4,5,6), {4,5,6})
            self.assertEqual(Item(x) + {4,5,6}, {4,5,6})
            # convert errors
            self.assertRaises(TypeError, lambda: Item(x) + 1)
            self.assertRaises(TypeError, lambda: Item(x) + 1.0)
            self.assertRaises(ValueError, lambda: Item(x) + 'a')
            self.assertRaises(TypeError, lambda: Item(x) + True)

    def test_type_by_index(self):
        test_i = Item(TestType.all_items)
        for index,t in enumerate(TestType.all_types):
            self.assertEqual(t, test_i._type_by_index(index))
        self.assertEqual(int, test_i._type_by_index(999))


class TestDict(TestCase):
    def test_mempty(self):
        self.assertEqual(
            Dict(Dict.__mempty__) + dict(data=2),
            Dict(data=2) + Dict.__mempty__, dict(data=2)
        )

    def test_associativity(self):
        self.assertEqual(
            Dict(Dict(data=1) + dict(data=2)) + dict(data=3),
            Dict(data=1) + (Dict(dict(data=2)) + dict(data=3))
        )

    def test_fmap(self):
        self.assertEqual(
            Dict(data=1).fmap(lambda k,v: (k, v + 1)),
            Dict(data=2)
        )

    def test_bind(self):
        self.assertEqual(
            Dict(data=1).bind(lambda x: dict(new_data=x['data'])),
            Dict(new_data=1)
        )


class SmokeTestsTarget(ABConfig):
    a = 1
    b = '2'
    c = 'string'
    d = {
        'a': 0,
        'b': 42
    }


class SmokeTests(TestCase):
    test_data = {
        'a': 1,
        'b': '2',
        'c': 'string',
        'd': {
            'a': 0,
            'b': 42
        }
    }

    def test_getattrs(self):
        self.assertDictEqual(dict(SmokeTestsTarget()),self.test_data)

