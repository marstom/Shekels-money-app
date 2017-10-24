from unittest import mock

import pytest

from shekels.cli import gen_arg_parser


@pytest.fixture
def arg_parser():
    return gen_arg_parser()


class TestGenArgParser:
    def test_parse_list_action(self, arg_parser):
        arguments = arg_parser.parse_args(['list'])
        assert arguments.action == 'list'

    def test_parse_add_action(self, arg_parser):
        arguments = arg_parser.parse_args(['add', '--name', 'test', '--price', '12'])

        assert arguments.action == 'add'
        assert arguments.name == 'test'
        assert arguments.price == 12

    @mock.patch('sys.stderr', mock.MagicMock())
    def test_add_wrong_param(self, arg_parser):
        with mock.patch('sys.exit', mock.MagicMock()) as m:
            arg_parser.parse_args(['add'])

        m.assert_any_call(2)
