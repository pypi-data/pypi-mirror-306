from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import pytest


from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import IntOption, StrOption, BoolOption, ChoiceOption, \
                     OptionDescription, Config
try:
    from tiramisu_api import Config as JsonConfig
    #params = ['tiramisu', 'tiramisu-json']
    params = ['tiramisu']
except:
    params = ['tiramisu']
from .utils import TestHelpFormatter, to_dict


def get_config(json, has_tree=False, default_verbosity=False, add_long=False, add_store_false=False):
    choiceoption = ChoiceOption('cmd',
                                'choice the sub argument',
                                ('str', 'list', 'int', 'none'),
                                properties=('mandatory',))
    booloption = BoolOption('verbosity',
                            'increase output verbosity',
                            default=default_verbosity,
                            )
    str_ = StrOption('str',
                     'string option',
                     default='default'
                     )
    list_ = StrOption('list',
                      'list string option',
                      multi=True,
                      default=['default'],
                      )
    int_ = IntOption('int',
                     'int option',
                     default=10,
                     )

    root = OptionDescription('root',
                             'root',
                             [choiceoption,
                             booloption,
                             str_,
                             list_,
                             int_
                             ])
    if has_tree:
        root = OptionDescription('root',
                                 'root',
                                 [root])
    config = Config(root)
    config.property.read_write()
    if add_store_false:
        config.option('verbosity').property.add('storefalse')
    if add_long:
        config.option('verbosity').property.add('longargument')
    if json == 'tiramisu':
        return config
    jconfig = JsonConfig(config.option.dict())
    return jconfig


@pytest.fixture(params=params)
def json(request):
    return request.param


def test_readme_help(json):
    output = """usage: prog.py [-h] --cmd {str,list,int,none} [--verbosity] [--no-verbosity] [--str [STR]] [--list [LIST ...]] [--int [INT]]

options:
  -h, --help            show this help message and exit
  --cmd {str,list,int,none}
                        choice the sub argument
  --verbosity           increase output verbosity (default: False)
  --no-verbosity
  --str [STR]           string option (default: default)
  --list [LIST ...]     list string option (default: default)
  --int [INT]           int option (default: 10)
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_readme_help2(json):
    output = """usage: prog.py [-h] --cmd {str,list,int,none} [--verbosity] [--no-verbosity] [--str [STR]] [--list [LIST ...]] [--int [INT]]

options:
  -h, --help            show this help message and exit
  --cmd {str,list,int,none}
                        choice the sub argument
  --verbosity           increase output verbosity (default: True)
  --no-verbosity
  --str [STR]           string option (default: default)
  --list [LIST ...]     list string option (default: default)
  --int [INT]           int option (default: 10)
"""
    parser = TiramisuCmdlineParser(get_config(json, default_verbosity=True), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output
