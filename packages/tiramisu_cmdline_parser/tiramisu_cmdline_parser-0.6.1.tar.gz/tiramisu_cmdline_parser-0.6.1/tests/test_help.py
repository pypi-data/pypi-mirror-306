from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import pytest
from argparse import RawDescriptionHelpFormatter


from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import IntOption, StrOption, BoolOption, ChoiceOption, \
                     OptionDescription, Config
try:
    from tiramisu_api import Config as JsonConfig
    #params = ['tiramisu', 'tiramisu-json']
    params = ['tiramisu']
except:
    params = ['tiramisu']
from .utils import TestHelpFormatter



def get_config(json):
    choiceoption = ChoiceOption('cmd',
                                'choice the sub argument',
                                ('str', 'list', 'int', 'none'),
                                properties=('mandatory',
                                            'positional'))
    od = OptionDescription('od',
                           'od',
                           [choiceoption])
    root = OptionDescription('root',
                             'root',
                             [od])
    config = Config(root)
    config.property.read_write()
    if json == 'tiramisu':
        return config
    jconfig = JsonConfig(config.option.dict())
    return jconfig


@pytest.fixture(params=params)
def json(request):
    return request.param


def test_help(json):
    output = """usage: prog.py [-h] {str,list,int,none}

options:
  -h, --help           show this help message and exit

od:
  {str,list,int,none}  choice the sub argument
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_help_epilog(json):
    output = """usage: prog.py [-h] {str,list,int,none}

options:
  -h, --help           show this help message and exit

od:
  {str,list,int,none}  choice the sub argument

two line
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', epilog="\ntwo\nline", formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_help_epilog_raw(json):
    output = """usage: prog.py [-h] {str,list,int,none}

options:
  -h, --help           show this help message and exit

od:
  {str,list,int,none}  choice the sub argument

two
line
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', epilog="\ntwo\nline", formatter_class=RawDescriptionHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output
