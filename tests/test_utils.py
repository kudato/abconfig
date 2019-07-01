import unittest

from abconfig.utils import Attrs, Finalize
from abconfig.common import Dict


test_data = dict(
    test1=1,
    test2=int,
    test3=Dict(
        a=1,
        b=list
    )
)


class TestClass(Dict):
    test1 = 1
    test2 = int
    test3 = test_data['test3']


class TestAttrs(unittest.TestCase):
    def test_read_attrs(self):
        self.assertEqual(Attrs(TestClass()), test_data)


class TestFinalize(unittest.TestCase):
    def test_finalize(self):
        data = test_data
        data['test2'] = None
        data['test3']['b'] = None
        self.assertEqual(Finalize(Dict(data)), data)
