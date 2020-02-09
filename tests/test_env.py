import os
import unittest
import unittest.mock

from abconfig.common import Dict
from abconfig.env import Environment


class TestEnv(unittest.TestCase):
    def test_variable(self):
        with unittest.mock.patch.dict(os.environ, {'FOO': 'bar'}):
            self.assertEqual(
                Dict(foo=str, __env__=True).bind(Environment), {'foo': 'bar', '__env__': True})

    def test_with_prefix(self):
        with unittest.mock.patch.dict(os.environ, {'FOO_BAR': 'baz'}):
            self.assertEqual(
                Dict(foo=dict(bar=str), __env__=True).bind(Environment),
                {'foo':{'bar': 'baz'}, '__env__': True}
            )

    def test_disabled(self):
        self.assertEqual(
            Dict(foo=1, __env__=False).bind(Environment), {'foo': 1, '__env__': False}
        )

    def test_list_value(self):
        with unittest.mock.patch.dict(os.environ, {'FOO': '1,2,3,4,5'}):
            self.assertEqual(
                Dict(foo=[int], __env__=True).bind(Environment), {'foo': [1,2,3,4,5], '__env__': True})
