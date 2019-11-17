import unittest

from abconfig.common import Item, Dict


class TestItem(unittest.TestCase):
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
        values = [list, [1,2,3]]
        for x in values:
            self.assertEqual(Item(x) + [4,5,6], [4,5,6])
            self.assertEqual(Item(x) + (4,5,6), [4,5,6])
            self.assertEqual(Item(x) + {4,5,6}, [4,5,6])
            # convert errors
            self.assertRaises(TypeError, lambda: Item(x) + 1)
            self.assertRaises(TypeError, lambda: Item(x) + 1.0)
            self.assertRaises(TypeError, lambda: Item(x) + 'a')
            self.assertRaises(TypeError, lambda: Item(x) + True)

    def test_tuple(self):
        values = [tuple, (1,2,3)]
        for x in values:
            self.assertEqual(Item(x) + [4,5,6], (4,5,6))
            self.assertEqual(Item(x) + (4,5,6), (4,5,6))
            self.assertEqual(Item(x) + {4,5,6}, (4,5,6))
            # convert errors
            self.assertRaises(TypeError, lambda: Item(x) + 1)
            self.assertRaises(TypeError, lambda: Item(x) + 1.0)
            self.assertRaises(TypeError, lambda: Item(x) + 'a')
            self.assertRaises(TypeError, lambda: Item(x) + True)

    def test_set(self):
        values = [set, {1,2,3}]
        for x in values:
            self.assertEqual(Item(x) + [4,5,6], {4,5,6})
            self.assertEqual(Item(x) + (4,5,6), {4,5,6})
            self.assertEqual(Item(x) + {4,5,6}, {4,5,6})
            # convert errors
            self.assertRaises(TypeError, lambda: Item(x) + 1)
            self.assertRaises(TypeError, lambda: Item(x) + 1.0)
            self.assertRaises(TypeError, lambda: Item(x) + 'a')
            self.assertRaises(TypeError, lambda: Item(x) + True)


class TestDict(unittest.TestCase):
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
            Dict(data=1)._fmap(lambda k,v: (k, v + 1)),
            Dict(data=2)
        )

    def test_bind(self):
        self.assertEqual(
            Dict(data=1)._bind(lambda x: dict(new_data=x['data'])),
            Dict(new_data=1)
        )