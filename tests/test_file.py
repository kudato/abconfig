import os
import json
import yaml
import toml
import unittest

from unittest.mock import mock_open, patch
from abconfig.file import Json, Yaml, Toml
from abconfig.common import Dict


source = dict(
    __file__='test_file',
    test1=int,
    test2=dict(
        test3=str
    )
)

data = dict(
    __file__='test_file',
    test1=1,
    test2=dict(
        test3='a'
    )
)


class TestFile(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(data))
    def test_json(self, m):
        self.assertEqual(Dict(source).bind(Json), data)
        m.assert_called_with('test_file', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=yaml.dump(data))
    def test_yaml(self, m):
        self.assertEqual(Dict(source).bind(Yaml), data)
        m.assert_called_with('test_file', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=toml.dumps(data))
    def test_toml(self, m):
        self.assertEqual(Dict(source).bind(Toml), data)
        m.assert_called_with('test_file', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='wrong')
    def test_wrong_file(self, m):
        self.assertEqual(
            Dict(test=1, __file__='test_file').bind(Json),
            dict(test=1, __file__='test_file')
        )
        m.assert_called_with('test_file', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([1,2,3]))
    def test_wrong_file_format(self, m):
        self.assertEqual(
            Dict(test=1, __file__='test_file').bind(Json),
            dict(test=1, __file__='test_file')
        )
        m.assert_called_with('test_file', 'r')

    def test_disabled(self):
        self.assertEqual(
            Dict(test=1,).bind(Json),
            dict(test=1)
        )
