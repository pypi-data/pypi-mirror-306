from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import pytest


from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import IntOption, StrOption, BoolOption, ChoiceOption, \
                     SymLinkOption, OptionDescription, Config
try:
    from tiramisu_api import Config as JsonConfig
    #params = ['tiramisu', 'tiramisu-json']
    params = ['tiramisu']
except:
    params = ['tiramisu']
from .utils import TestHelpFormatter


def get_config(json, has_tree=False, default_verbosity=False, add_long=False, add_store_false=False, empty_optiondescription=False):
    choiceoption = ChoiceOption('cmd',
                                'choice the sub argument',
                                ('str', 'list', 'int', 'none'),
                                properties=('mandatory',
                                            'positional'))
    booloption = BoolOption('verbosity',
                            'increase output verbosity',
                            default=default_verbosity)
    short_booloption = SymLinkOption('v', booloption)

    od0 = OptionDescription('od0',
                            'Sub-Tree 1',
                            [choiceoption,
                            booloption,
                            short_booloption,
                            ])
    if empty_optiondescription:
        descr = None
    else:
        descr = 'First OptionDescription'
    od1 = OptionDescription('od1',
                            descr,
                            [od0])
    before = StrOption('before',
                       'Before',
                       properties=('mandatory',))
    after = StrOption('after',
                      'After',
                      properties=('mandatory',))
    str_ = StrOption('str',
                     'string option 2',
                     properties=('mandatory',))
    subtree = OptionDescription('subtree',
                                'Sub-Tree 2',
                                [str_])
    od2 = OptionDescription('od2',
                            None,
                            [before, subtree, after])
    root = OptionDescription('root',
                             'root',
                             [od1, od2])
    config = Config(root)
    config.property.read_write()
    if json == 'tiramisu':
        return config
    jconfig = JsonConfig(config.option.dict())
    return jconfig


@pytest.fixture(params=params)
def json(request):
    return request.param


def test_optiondescription_help(json):
    output = """usage: prog.py [-h] [-v] [-nv] --od2.subtree.str STR --od2.before BEFORE --od2.after AFTER {str,list,int,none}

options:
  -h, --help            show this help message and exit

od1:
  First OptionDescription

od1.od0:
  Sub-Tree 1

  {str,list,int,none}   choice the sub argument
  -v, --od1.od0.verbosity
                        increase output verbosity (default: False)
  -nv, --od1.od0.no-verbosity

od2:
  --od2.before BEFORE   Before
  --od2.after AFTER     After

od2.subtree:
  Sub-Tree 2

  --od2.subtree.str STR
                        string option 2
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_optiondescription_help_remove_empty_od(json):
    output = """usage: prog.py [-h] [-v] [-nv] --od2.subtree.str STR --od2.before BEFORE --od2.after AFTER {str,list,int,none}

options:
  -h, --help            show this help message and exit

od1.od0:
  Sub-Tree 1

  {str,list,int,none}   choice the sub argument
  -v, --od1.od0.verbosity
                        increase output verbosity (default: False)
  -nv, --od1.od0.no-verbosity

od2:
  --od2.before BEFORE   Before
  --od2.after AFTER     After

od2.subtree:
  Sub-Tree 2

  --od2.subtree.str STR
                        string option 2
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', remove_empty_od=True, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_optiondescription_help_remove_empty_description_od(json):
    output = """usage: prog.py [-h] [-v] [-nv] --od2.subtree.str STR --od2.before BEFORE --od2.after AFTER {str,list,int,none}

options:
  -h, --help            show this help message and exit

od1.od0:
  Sub-Tree 1

  {str,list,int,none}   choice the sub argument
  -v, --od1.od0.verbosity
                        increase output verbosity (default: False)
  -nv, --od1.od0.no-verbosity

od2:
  --od2.before BEFORE   Before
  --od2.after AFTER     After

od2.subtree:
  Sub-Tree 2

  --od2.subtree.str STR
                        string option 2
"""
    parser = TiramisuCmdlineParser(get_config(json, empty_optiondescription=True), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_optiondescription_help_subtree(json):
    output = """usage: prog.py [-h] --od2.subtree.str STR --od2.before BEFORE --od2.after AFTER

options:
  -h, --help            show this help message and exit
  --od2.before BEFORE   Before
  --od2.after AFTER     After

od2.subtree:
  Sub-Tree 2

  --od2.subtree.str STR
                        string option 2
"""
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py', root='od2', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output
