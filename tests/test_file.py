import os
import json
import yaml
import toml
import unittest

from unittest.mock import mock_open, patch
from abconfig.file import Json, Yaml, Toml, Ini, File
from abconfig.common import Dict

ini_source = dict(
    __file__='test_file.ini',
    __file_required__=bool,
    test1=int,
    test2=str
)

ini_data = dict(
    __file__='test_file.ini',
    __file_required__=True,
    test1=1,
    test2='qwe'
)

ini_raw = '''
[data]
__file__ = test_file.ini
__file_required__ = 1
test1 = 1
test2 = qwe
'''

source = dict(
    __file__='test_file',
    test=int,
    test2=dict(
        test3=str
    )
)

data = dict(
    __file__='test_file',
    test=1,
    test2=dict(
        test3='a'
    )
)

class TestFile(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(data))
    def test_json(self, m):
        self.assertEqual(Dict(source).bind(Json), data)
        m.assert_called_with(data['__file__'], 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=yaml.dump(data))
    def test_yaml(self, m):
        self.assertEqual(Dict(source).bind(Yaml), data)
        m.assert_called_with(data['__file__'], 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=toml.dumps(data))
    def test_toml(self, m):
        self.assertEqual(Dict(source).bind(Toml), data)
        m.assert_called_with(data['__file__'], 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='wrong')
    def test_wrong_file(self, m):
        self.assertEqual(
            Dict(test=1, __file__=data['__file__']).bind(Json),
            dict(test=1, __file__=data['__file__'])
        )
        m.assert_called_with(data['__file__'], 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([1,2,3]))
    def test_wrong_file_format(self, m):
        self.assertEqual(
            Dict(test=1, __file__=data['__file__']).bind(Json),
            dict(test=1, __file__=data['__file__'])
        )
        m.assert_called_with(data['__file__'], 'r')

    def test_disabled(self):
        self.assertEqual(
            Dict(test=1,).bind(Json),
            dict(test=1)
        )

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(data))
    def test_detect_format_json(self, m):
        self.assertEqual(
            Dict(test=1, __file__=data['__file__']).bind(File),
            dict(test=1, __file__=data['__file__'])
        )
        m.assert_called_with(data['__file__'], 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=yaml.dump(data))
    def test_detect_format_yaml(self, m):
        self.assertEqual(
            Dict(test=1, __file__=data['__file__']).bind(File),
            dict(test=1, __file__=data['__file__'])
        )
        m.assert_called_with(data['__file__'], 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=toml.dumps(data))
    def test_detect_format_toml(self, m):
        self.assertEqual(
            Dict(test=1, __file__=data['__file__']).bind(File),
            dict(test=1, __file__=data['__file__'])
        )
        m.assert_called_with(data['__file__'], 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'test': data}))
    def test_with_prefix(self, m):
        self.assertEqual(
            Dict(
                test=1,
                __file__=data['__file__'],
                __prefix__='test'
            ).bind(File),
            dict(
                test=1,
                __file__=data['__file__'],
                __prefix__='test'
            )
        )
        m.assert_called_with(data['__file__'], 'r')
