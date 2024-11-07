from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import pytest


from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import ChoiceOption, OptionDescription, Config
try:
    from tiramisu_api import Config as JsonConfig
    #params = ['tiramisu', 'tiramisu-json']
    params = ['tiramisu']
except:
    params = ['tiramisu']

from .utils import TestHelpFormatter, to_dict


def get_config(json):
    positional = ChoiceOption('positional',
                              'choice the sub argument',
                              ('str', 'list', 'int', 'none'),
                              properties=('positional', 'mandatory'))
    positional_int = ChoiceOption('positional_int',
                              'choice the sub argument',
                              (1, 2, 3),
                              properties=('positional', 'mandatory'))
    str_ = ChoiceOption('str',
                        'choice the sub argument',
                        ('str1', 'str2', 'str3', None))
    int_ = ChoiceOption('int',
                        'choice the sub argument',
                        (1, 2, 3))
    int_multi = ChoiceOption('int_multi',
                             'choice the sub argument',
                             (1, 2, 3),
                             multi=True)
    od = OptionDescription('od',
                           'od',
                           [positional, positional_int, str_, int_, int_multi])
    config = Config(od)
    config.property.read_write()
    if json == 'tiramisu':
        return config
    jconfig = JsonConfig(config.option.get())
    return jconfig


@pytest.fixture(params=params)
def json(request):
    return request.param


def test_choice_positional(json):
    output1 = '''usage: prog.py "str" "1" [-h] [--str {str1,str2,str3}] [--int {1,2,3}] [--int_multi [{1,2,3} ...]] {str,list,int,none} {1,2,3}
prog.py: error: argument positional: invalid choice: 'error' (choose from 'str', 'list', 'int', 'none')
'''
    output2 = '''usage: prog.py "str" "1" [-h] [--str {str1,str2,str3}] [--int {1,2,3}] [--int_multi [{1,2,3} ...]] {str,list,int,none} {1,2,3}
prog.py: error: argument positional_int: invalid choice: '4' (choose from '1', '2', '3')
'''
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', formatter_class=TestHelpFormatter)
    parser.parse_args(['str', '1'])
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': None,
                                   'int': None,
                                   'int_multi': []}
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['error', '1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output1

    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str', '4'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output2


def test_choice_str(json):
    output = """usage: prog.py "str" "1" --str "str3" [-h] [--str {str1,str2,str3}] [--int {1,2,3}] [--int_multi [{1,2,3} ...]] {str,list,int,none} {1,2,3}
prog.py: error: argument --str: invalid choice: 'error' (choose from 'str1', 'str2', 'str3')
"""
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', formatter_class=TestHelpFormatter)
    parser.parse_args(['str', '1', '--str', 'str1'])
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': 'str1',
                                   'int': None,
                                   'int_multi': []}
    parser.parse_args(['str', '1', '--str', 'str2'])
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': 'str2',
                                   'int': None,
                                   'int_multi': []}
    parser.parse_args(['str', '1', '--str', 'str3'])
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': 'str3',
                                   'int': None,
                                   'int_multi': []}
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str', '1', '--str', 'error'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': 'str3',
                                   'int': None,
                                   'int_multi': []}


def test_choice_int(json):
    output = """usage: prog.py "str" "1" --int "1" [-h] [--str {str1,str2,str3}] [--int {1,2,3}] [--int_multi [{1,2,3} ...]] {str,list,int,none} {1,2,3}
prog.py: error: argument --int: invalid choice: '4' (choose from '1', '2', '3')
"""
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', formatter_class=TestHelpFormatter)
    parser.parse_args(['str', '1', '--int', '1'])
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': None,
                                   'int': 1,
                                   'int_multi': []}
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str', '1', '--int', '4'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': None,
                                   'int': 1,
                                   'int_multi': []}


def test_choice_int_multi(json):
    output = """usage: prog.py "str" "1" --int_multi "1" "2" [-h] [--str {str1,str2,str3}] [--int {1,2,3}] [--int_multi [{1,2,3} ...]] {str,list,int,none} {1,2,3}
prog.py: error: argument --int_multi: invalid choice: '4' (choose from '1', '2', '3')
"""
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', formatter_class=TestHelpFormatter)
    parser.parse_args(['str', '1', '--int_multi', '1', '2'])
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': None,
                                   'int': None,
                                   'int_multi': [1, 2]}
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str', '1', '--int_multi', '4'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': None,
                                   'int': None,
                                   'int_multi': [1, 2]}
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str', '1', '--int_multi', '1', '4'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output
    assert to_dict(config.value.get()) == {'positional': 'str',
                                   'positional_int': 1,
                                   'str': None,
                                   'int': None,
                                   'int_multi': [1, 2]}
