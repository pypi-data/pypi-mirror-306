from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import pytest


from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import IntOption, StrOption, BoolOption, ChoiceOption, \
                     OptionDescription, Leadership, SymLinkOption, Config, submulti
try:
    from tiramisu_api import Config as JsonConfig
#    params = ['tiramisu', 'tiramisu-json']
    params = ['tiramisu']
except:
    params = ['tiramisu']

from .utils import TestHelpFormatter, to_dict


def get_config(json, with_mandatory=False, with_symlink=False, with_default_value=True):
    if with_default_value:
        default = ['192.168.0.1']
    else:
        default = []
    leader = StrOption('leader', "Leader var", default, multi=True)
    if with_symlink:
        link_leader = SymLinkOption('l', leader)
    follower = StrOption('follower', "Follower", multi=True)
    if with_mandatory:
        properties = ('mandatory',)
    else:
        properties = None
    follower_submulti = StrOption('follower_submulti', "Follower submulti", multi=submulti, properties=properties)
    follower_integer = IntOption('follower_integer', "Follower integer", multi=True)
    if with_symlink:
        link_follower = SymLinkOption('i', follower_integer)
    follower_boolean = BoolOption('follower_boolean', "Follower boolean", multi=True)
    follower_choice = ChoiceOption('follower_choice', "Follower choice", ('opt1', 'opt2'), multi=True)
    opt_list = [leader, follower, follower_submulti, follower_integer, follower_boolean, follower_choice]
    if with_symlink:
        opt_list.append(link_leader)
        opt_list.append(link_follower)
    if with_mandatory:
        opt_list.append(StrOption('follower_mandatory', "Follower mandatory", multi=True, properties=('mandatory',)))
    leadership = Leadership('leader', 'leader', opt_list)
    config = Config(OptionDescription('root', 'root', [leadership]))
    if json == 'tiramisu':
        return config
    jconfig = JsonConfig(config.option.dict())
    return jconfig


@pytest.fixture(params=params)
def json(request):
    return request.param


def test_leadership_help(json):
    output = """usage: prog.py [-h] [--leader.leader [LEADER ...]] [--leader.pop-leader INDEX] [--leader.follower INDEX [FOLLOWER]] --leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...] [--leader.follower_integer INDEX [FOLLOWER_INTEGER]] [--leader.follower_boolean INDEX] [--leader.no-follower_boolean INDEX] [--leader.follower_choice INDEX [{opt1,opt2}]] --leader.follower_mandatory INDEX FOLLOWER_MANDATORY

options:
  -h, --help            show this help message and exit

leader:
  --leader.leader [LEADER ...]
                        Leader var
  --leader.pop-leader INDEX
  --leader.follower INDEX [FOLLOWER]
                        Follower
  --leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...]
                        Follower submulti
  --leader.follower_integer INDEX [FOLLOWER_INTEGER]
                        Follower integer
  --leader.follower_boolean INDEX
                        Follower boolean
  --leader.no-follower_boolean INDEX
  --leader.follower_choice INDEX [{opt1,opt2}]
                        Follower choice
  --leader.follower_mandatory INDEX FOLLOWER_MANDATORY
                        Follower mandatory
"""
    parser = TiramisuCmdlineParser(get_config(json, with_mandatory=True), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_leadership_help_no_pop(json):
    output = """usage: prog.py [-h] [--leader.leader [LEADER ...]] [--leader.follower INDEX [FOLLOWER]] --leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...] [--leader.follower_integer INDEX [FOLLOWER_INTEGER]] [--leader.follower_boolean INDEX] [--leader.follower_choice INDEX [{opt1,opt2}]] --leader.follower_mandatory INDEX FOLLOWER_MANDATORY

options:
  -h, --help            show this help message and exit

leader:
  --leader.leader [LEADER ...]
                        Leader var
  --leader.follower INDEX [FOLLOWER]
                        Follower
  --leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...]
                        Follower submulti
  --leader.follower_integer INDEX [FOLLOWER_INTEGER]
                        Follower integer
  --leader.follower_boolean INDEX
                        Follower boolean
  --leader.follower_choice INDEX [{opt1,opt2}]
                        Follower choice
  --leader.follower_mandatory INDEX FOLLOWER_MANDATORY
                        Follower mandatory
"""
    parser = TiramisuCmdlineParser(get_config(json, with_mandatory=True), 'prog.py', add_extra_options=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_leadership_help_short_no_default(json):
    output = """usage: prog.py [-h] [-l [LEADER ...]]

options:
  -h, --help            show this help message and exit

leader:
  -l [LEADER ...], --leader.leader [LEADER ...]
                        Leader var
"""
    parser = TiramisuCmdlineParser(get_config(json, with_mandatory=True, with_symlink=True, with_default_value=False), 'prog.py', add_extra_options=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_leadership_help_short(json):
    output = """usage: prog.py [-h] [-l [LEADER ...]] [--leader.follower INDEX [FOLLOWER]] --leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...] [-i INDEX [FOLLOWER_INTEGER]] [--leader.follower_boolean INDEX] [--leader.follower_choice INDEX [{opt1,opt2}]] --leader.follower_mandatory INDEX FOLLOWER_MANDATORY

options:
  -h, --help            show this help message and exit

leader:
  -l [LEADER ...], --leader.leader [LEADER ...]
                        Leader var
  --leader.follower INDEX [FOLLOWER]
                        Follower
  --leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...]
                        Follower submulti
  -i INDEX [FOLLOWER_INTEGER], --leader.follower_integer INDEX [FOLLOWER_INTEGER]
                        Follower integer
  --leader.follower_boolean INDEX
                        Follower boolean
  --leader.follower_choice INDEX [{opt1,opt2}]
                        Follower choice
  --leader.follower_mandatory INDEX FOLLOWER_MANDATORY
                        Follower mandatory
"""
    parser = TiramisuCmdlineParser(get_config(json, with_mandatory=True, with_symlink=True), 'prog.py', add_extra_options=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_leadership_modif_leader(json):
    output = {'leader.leader': ['192.168.1.1'],
              'leader.follower': [None],
              'leader.follower_boolean': [None],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [[]]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.leader', '192.168.1.1'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower(json):
    output = {'leader.leader': ['192.168.0.1'],
              'leader.follower': ['255.255.255.0'],
              'leader.follower_boolean': [None],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [[]]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.follower', '0', '255.255.255.0'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower_not_submulti(json):
    output = """usage: prog.py [-h] [--leader.leader [LEADER ...]] [--leader.pop-leader INDEX] [--leader.follower INDEX [FOLLOWER]] [--leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...]] [--leader.follower_integer INDEX [FOLLOWER_INTEGER]] [--leader.follower_boolean INDEX] [--leader.no-follower_boolean INDEX] [--leader.follower_choice INDEX [{opt1,opt2}]]
prog.py: error: unrecognized arguments: 255.255.255.0
"""

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--leader.follower', '0', '255.255.255.0', '255.255.255.0'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_leadership_modif_follower_submulti(json):
    output = {'leader.leader': ['192.168.0.1'],
              'leader.follower': [None],
              'leader.follower_boolean': [None],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [['255.255.255.0']]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.follower_submulti', '0', '255.255.255.0'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower_submulti_multi(json):
    output = {'leader.leader': ['192.168.0.1'],
              'leader.follower': [None],
              'leader.follower_boolean': [None],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [['255.255.255.0', '255.255.255.128']]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.follower_submulti', '0', '255.255.255.0', '255.255.255.128'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower_bool_true(json):
    output = {'leader.leader': ['192.168.0.1'],
              'leader.follower': [None],
              'leader.follower_boolean': [True],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [[]]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.follower_boolean', '0'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower_bool_false(json):
    output = {'leader.leader': ['192.168.0.1'],
              'leader.follower': [None],
              'leader.follower_boolean': [False],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [[]]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.no-follower_boolean', '0'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower_bool_true_fullname(json):
    output = {'leader.leader': ['192.168.0.1'],
              'leader.follower': [None],
              'leader.follower_boolean': [True],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [[]]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['--follower_boolean', '0'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower_bool_false_fullname(json):
    output = {'leader.leader': ['192.168.0.1'],
              'leader.follower': [None],
              'leader.follower_boolean': [False],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [[]]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['--no-follower_boolean', '0'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower_choice(json):
    output = {'leader.leader': ['192.168.0.1'],
              'leader.follower': [None],
              'leader.follower_boolean': [None],
              'leader.follower_choice': ['opt1'],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [[]]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.follower_choice', '0', 'opt1'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_follower_choice_unknown(json):
    output = """usage: prog.py [-h] [--leader.leader [LEADER ...]] [--leader.pop-leader INDEX] [--leader.follower INDEX [FOLLOWER]] [--leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...]] [--leader.follower_integer INDEX [FOLLOWER_INTEGER]] [--leader.follower_boolean INDEX] [--leader.no-follower_boolean INDEX] [--leader.follower_choice INDEX [{opt1,opt2}]]
prog.py: error: argument --leader.follower_choice: invalid choice: 'opt_unknown' (choose from 'opt1', 'opt2')
"""
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--leader.follower_choice', '0', 'opt_unknown'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_leadership_modif_follower_not_number(json):
    output = """usage: prog.py [-h] [--leader.leader [LEADER ...]] [--leader.pop-leader INDEX] [--leader.follower INDEX [FOLLOWER]] [--leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...]] [--leader.follower_integer INDEX [FOLLOWER_INTEGER]] [--leader.follower_boolean INDEX] [--leader.no-follower_boolean INDEX] [--leader.follower_choice INDEX [{opt1,opt2}]]
prog.py: error: index must be a number, not a
"""

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--leader.follower', 'a', '255.255.255.0'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_leadership_modif_multi(json):
    output = {'leader.leader': ['192.168.1.1', '10.253.10.1', '192.168.253.1'],
              'leader.follower': ['255.255.255.128', None, '255.255.255.0'],
              'leader.follower_boolean': [None, None, None],
              'leader.follower_choice': [None, None, None],
              'leader.follower_integer': [None, None, None],
              'leader.follower_submulti': [[], [], []]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.leader', '192.168.1.1', '10.253.10.1', '192.168.253.1',
                       '--leader.follower', '0', '255.255.255.128',
                       '--leader.follower', '2', '255.255.255.0'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_multi_reduce(json):
    output = {'leader.leader': ['192.168.1.1', '192.168.253.1'],
              'leader.follower': ['255.255.255.128', '255.255.255.0'],
              'leader.follower_boolean': [None,  None],
              'leader.follower_choice': [None, None],
              'leader.follower_integer': [None, None],
              'leader.follower_submulti': [[], []]}

    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.leader', '192.168.1.1', '10.253.10.1', '192.168.253.1',
                       '--leader.follower', '0', '255.255.255.128',
                       '--leader.follower', '2', '255.255.255.0',
                       '--leader.pop-leader', '1'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_mandatory(json):
    output = {'leader.leader': ['192.168.1.1'],
              'leader.follower': [None],
              'leader.follower_mandatory': ['255.255.255.128'],
              'leader.follower_boolean': [None],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [['255.255.255.128']]}
    output2 = """usage: prog.py --leader.leader "192.168.1.1" [-h] [--leader.leader [LEADER ...]] [--leader.pop-leader INDEX] [--leader.follower INDEX [FOLLOWER]] --leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...] [--leader.follower_integer INDEX [FOLLOWER_INTEGER]] [--leader.follower_boolean INDEX] [--leader.no-follower_boolean INDEX] [--leader.follower_choice INDEX [{opt1,opt2}]] --leader.follower_mandatory INDEX FOLLOWER_MANDATORY
prog.py: error: the following arguments are required: --leader.follower_submulti"""

    config = get_config(json, with_mandatory=True)
    parser = TiramisuCmdlineParser(config, 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--leader.leader', '192.168.1.1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output2 + ', --leader.follower_mandatory\n'
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--leader.leader', '192.168.1.1',
                               '--leader.follower_mandatory', '0', '255.255.255.128'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output2 + '\n'
    parser.parse_args(['--leader.leader', '192.168.1.1',
                       '--leader.follower_submulti', '0', '255.255.255.128',
                       '--leader.follower_mandatory', '0', '255.255.255.128'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_mandatory_remove(json):
    output = {'leader.leader': ['192.168.1.1'],
              'leader.follower': [None],
              'leader.follower_mandatory': ['255.255.255.128'],
              'leader.follower_boolean': [None],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [['255.255.255.128']]}
    output2 = """usage: prog.py --leader.leader "192.168.1.1" [-h] [--leader.pop-leader INDEX] [--leader.follower INDEX [FOLLOWER]] --leader.follower_submulti INDEX [FOLLOWER_SUBMULTI ...] [--leader.follower_integer INDEX [FOLLOWER_INTEGER]] [--leader.follower_boolean INDEX] [--leader.no-follower_boolean INDEX] [--leader.follower_choice INDEX [{opt1,opt2}]] --leader.follower_mandatory INDEX FOLLOWER_MANDATORY
prog.py: error: the following arguments are required: --leader.follower_submulti"""

    config = get_config(json, with_mandatory=True)
    parser = TiramisuCmdlineParser(config, 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--leader.leader', '192.168.1.1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output2 + ', --leader.follower_mandatory\n'
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--leader.leader', '192.168.1.1',
                               '--leader.follower_mandatory', '0', '255.255.255.128'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output2 + '\n'
    parser.parse_args(['--leader.leader', '192.168.1.1',
                       '--leader.follower_submulti', '0', '255.255.255.128',
                       '--leader.follower_mandatory', '0', '255.255.255.128'])
    assert to_dict(config.value.get()) == output


def test_leadership_modif_mandatory_unvalidate(json):
    output = {'leader.leader': ['192.168.1.1'],
              'leader.follower': [None],
              'leader.follower_mandatory': [None],
              'leader.follower_boolean': [None],
              'leader.follower_choice': [None],
              'leader.follower_integer': [None],
              'leader.follower_submulti': [[]]}
    config = get_config(json, with_mandatory=True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--leader.leader', '192.168.1.1'], valid_mandatory=False)
    assert to_dict(config.value.get()) == output
