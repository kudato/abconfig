import unittest

from abconfig import GetAttrs
from abconfig.common import Dict
from abconfig.utils import Close

test_data = dict(
    test1=1,
    test2=1,
    test3=Dict(
        a=1,
        b=1
    )
)


class TestClass(Dict):
    test1 = 1
    test2 = 1
    test3 = Dict(
        a=1,
        b=1
    )


class TestGetAttrs(unittest.TestCase):
    def test_read_attrs(self):
        self.assertEqual(GetAttrs(TestClass()),test_data)


class TestClose(unittest.TestCase):
    def test_finalize(self):
        data = test_data
        self.assertEqual(Close(Dict(data)), test_data)
