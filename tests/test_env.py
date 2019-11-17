import os
import unittest
import unittest.mock

from abconfig.common import Dict
from abconfig.env import Env


class TestEnv(unittest.TestCase):
    def test_variable(self):
        with unittest.mock.patch.dict(os.environ, {'FOO': 'bar'}):
            self.assertEqual(
                Dict(foo=str, __env__=True)._bind(Env), {'foo': 'bar'})

    def test_with_prefix(self):
        with unittest.mock.patch.dict(os.environ, {'FOO_BAR': 'baz'}):
            self.assertEqual(
                Dict(foo=dict(bar=str), __env__=True)._bind(Env),
                {'foo':{'bar': 'baz'}}
            )

    def test_disabled(self):
        self.assertEqual(
            Dict(foo=1, __env__=False)._bind(Env), {'foo': 1}
        )
