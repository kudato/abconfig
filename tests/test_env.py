import os
import unittest
import unittest.mock

from abconfig.common import Dict
from abconfig.env import Env


class TestEnv(unittest.TestCase):
    def test_variable(self):
        with unittest.mock.patch.dict(os.environ, {'FOO': 'bar'}):            
            self.assertEqual(
                Dict(foo=str, load_env=True).bind(Env), {'foo': 'bar'})

    def test_with_prefix(self):
        with unittest.mock.patch.dict(os.environ, {'FOO_BAR': 'baz'}):            
            self.assertEqual(
                Dict(foo=dict(bar=str), load_env=True).bind(Env),
                {'foo':{'bar': 'baz'}}
            )

    def test_disabled(self):
        self.assertEqual(
            Dict(foo=1, load_env=False).bind(Env), {'foo': 1}
        )
