from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import pytest


from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import IntOption, StrOption, BoolOption, ChoiceOption, \
                     SymLinkOption, OptionDescription, Config, calc_value, \
                     Calculation, ParamValue, ParamOption, Params
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
                                properties=('mandatory',
                                            'positional'))
    booloption = BoolOption('verbosity',
                            'increase output verbosity',
                            default=default_verbosity)
    short_booloption = SymLinkOption('v', booloption)
    str_ = StrOption('str',
                     'string option',
                     properties=('mandatory',
                                 Calculation(calc_value,
                                             Params(ParamValue('disabled'),
                                                    kwargs={'condition': ParamOption(choiceoption),
                                                            'reverse_condition': ParamValue(True),
                                                            'expected': ParamValue('str')})),
                                 ),
                     )
    list_ = StrOption('list',
                      'list string option',
                      multi=True,
                      properties=('mandatory',
                                  Calculation(calc_value,
                                              Params(ParamValue('disabled'),
                                                     kwargs={'condition': ParamOption(choiceoption),
                                                             'reverse_condition': ParamValue(True),
                                                             'expected': ParamValue('list')})),
                                  ),
                      )
    int_ = IntOption('int',
                     'int option',
                      properties=('mandatory',
                                  Calculation(calc_value,
                                              Params(ParamValue('disabled'),
                                                     kwargs={'condition': ParamOption(choiceoption),
                                                             'reverse_condition': ParamValue(True),
                                                             'expected': ParamValue('int')})),
                                  ),
                     )

    root = OptionDescription('root',
                             'root',
                             [choiceoption,
                             booloption,
                             short_booloption,
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
    output = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}

positional arguments:
  {str,list,int,none}  choice the sub argument

options:
  -h, --help           show this help message and exit
  -v, --verbosity      increase output verbosity (default: False)
  -nv, --no-verbosity
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_readme_help_tree(json):
    output = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}

options:
  -h, --help            show this help message and exit

root:
  {str,list,int,none}   choice the sub argument
  -v, --root.verbosity  increase output verbosity (default: False)
  -nv, --root.no-verbosity
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_readme_help_tree_flatten(json):
    output = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}

options:
  -h, --help           show this help message and exit

root:
  {str,list,int,none}  choice the sub argument
  -v, --verbosity      increase output verbosity (default: False)
  -nv, --no-verbosity
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', fullpath=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()
    assert f.getvalue() == output


def test_readme_help_modif_positional(json):
    output = """usage: prog.py "str" [-h] [-v] [-nv] --str STR {str,list,int,none}

positional arguments:
  {str,list,int,none}  choice the sub argument

options:
  -h, --help           show this help message and exit
  -v, --verbosity      increase output verbosity (default: False)
  -nv, --no-verbosity
  --str STR            string option
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        try:
            parser.parse_args(['str', '--help'])
        except SystemExit as err:
            assert str(err) == "0"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_help_modif_positional_remove(json):
    output = """usage: prog.py "str" [-h] [-v] [-nv] --str STR

options:
  -h, --help           show this help message and exit
  -v, --verbosity      increase output verbosity (default: False)
  -nv, --no-verbosity
  --str STR            string option
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        try:
            parser.parse_args(['str', '--help'])
        except SystemExit as err:
            assert str(err) == "0"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_help_modif(json):
    output = """usage: prog.py "str" --str "toto" [-h] [-v] [-nv] --str STR {str,list,int,none}

positional arguments:
  {str,list,int,none}  choice the sub argument

options:
  -h, --help           show this help message and exit
  -v, --verbosity      increase output verbosity (default: False)
  -nv, --no-verbosity
  --str STR            string option
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        try:
            parser.parse_args(['str', '--str', 'toto', '--help'])
        except SystemExit as err:
            assert str(err) == "0"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_help_modif_remove(json):
    output = """usage: prog.py "str" --str "toto" [-h] [-v] [-nv]

options:
  -h, --help           show this help message and exit
  -v, --verbosity      increase output verbosity (default: False)
  -nv, --no-verbosity
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        try:
            parser.parse_args(['str', '--str', 'toto', '--help'])
        except SystemExit as err:
            assert str(err) == "0"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_help_modif_short(json):
    output = """usage: prog.py "str" -v [-h] [-v] [-nv] --str STR {str,list,int,none}

positional arguments:
  {str,list,int,none}  choice the sub argument

options:
  -h, --help           show this help message and exit
  -v, --verbosity      increase output verbosity (default: False)
  -nv, --no-verbosity
  --str STR            string option
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        try:
            parser.parse_args(['str', '-v', '--help'])
        except SystemExit as err:
            assert str(err) == "0"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_help_modif_short_remove(json):
	# FIXME -v -nv ?? pas de description
    output = """usage: prog.py "str" -v [-h] [-nv] --str STR

options:
  -h, --help           show this help message and exit
  -nv, --no-verbosity  increase output verbosity (default: False)
  --str STR            string option
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        try:
            parser.parse_args(['str', '-v', '--help'])
        except SystemExit as err:
            assert str(err) == "0"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_help_modif_short_no1(json):
    output = """usage: prog.py "str" -v [-h] [-v] [-nv] --str STR {str,list,int,none}

positional arguments:
  {str,list,int,none}  choice the sub argument

options:
  -h, --help           show this help message and exit
  -v, --verbosity      increase output verbosity (default: False)
  -nv, --no-verbosity
  --str STR            string option
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        try:
            parser.parse_args(['str', '-nv', '--help'])
        except SystemExit as err:
            assert str(err) == "0"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_help_modif_short_no_remove(json):
    output = """usage: prog.py "str" -v [-h] [-v] --str STR

options:
  -h, --help       show this help message and exit
  -v, --verbosity  increase output verbosity (default: False)
  --str STR        string option
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stdout(f):
        try:
            parser.parse_args(['str', '-nv', '--help'])
        except SystemExit as err:
            assert str(err) == "0"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_positional_mandatory(json):
    output = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: the following arguments are required: cmd
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args([])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_positional_mandatory_tree(json):
    output = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: the following arguments are required: root.cmd
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args([])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_positional_mandatory_tree_flatten(json):
    output = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: the following arguments are required: cmd
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', fullpath=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args([])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_mandatory(json):
    output = """usage: prog.py "str" [-h] [-v] [-nv] --str STR {str,list,int,none}
prog.py: error: the following arguments are required: --str
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_mandatory_remove(json):
    output = """usage: prog.py "str" [-h] [-v] [-nv] --str STR
prog.py: error: the following arguments are required: --str
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_mandatory_tree(json):
    output = """usage: prog.py "str" [-h] [-v] [-nv] --root.str STR {str,list,int,none}
prog.py: error: the following arguments are required: --root.str
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_mandatory_tree_remove(json):
    output = """usage: prog.py "str" [-h] [-v] [-nv] --root.str STR
prog.py: error: the following arguments are required: --root.str
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_mandatory_tree_flatten(json):
    output = """usage: prog.py "str" [-h] [-v] [-nv] --str STR {str,list,int,none}
prog.py: error: the following arguments are required: --str
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', fullpath=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_mandatory_tree_flatten_remove(json):
    output = """usage: prog.py "str" [-h] [-v] [-nv] --str STR
prog.py: error: the following arguments are required: --str
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', fullpath=False, display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['str'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_cross(json):
    output = """usage: prog.py "none" [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: unrecognized arguments: --int
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['none', '--int', '1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_cross_remove(json):
    output = """usage: prog.py "none" [-h] [-v] [-nv]
prog.py: error: unrecognized arguments: --int
"""
    parser = TiramisuCmdlineParser(get_config(json), 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['none', '--int', '1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_cross_tree(json):
    output = """usage: prog.py "none" [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: unrecognized arguments: --root.int
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['none', '--root.int', '1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_cross_tree_remove(json):
    output = """usage: prog.py "none" [-h] [-v] [-nv]
prog.py: error: unrecognized arguments: --root.int
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['none', '--root.int', '1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_cross_tree_flatten(json):
    output = """usage: prog.py "none" [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: unrecognized arguments: --int
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', fullpath=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['none', '--int', '1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_cross_tree_flatten_remove(json):
    output = """usage: prog.py "none" [-h] [-v] [-nv]
prog.py: error: unrecognized arguments: --int
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', fullpath=False, display_modified_value=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['none', '--int', '1'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_unknown(json):
    output = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: argument root.cmd: invalid choice: 'unknown' (choose from 'str', 'list', 'int', 'none')
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', fullpath=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['unknown'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output


def test_readme_int(json):
    output = {'cmd': 'int',
              'int': 3,
              'verbosity': False,
              'v': False}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--int', '3'])
    assert to_dict(config.value.get()) == output


def test_readme_int_tree(json):
    output = {'root.cmd': 'int',
              'root.int': 3,
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--root.int', '3'])
    assert to_dict(config.value.get()) == output


def test_readme_int_tree_flatten(json):
    output = {'root.cmd': 'int',
              'root.int': 3,
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['int', '--int', '3'])
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity(json):
    output = {'cmd': 'int',
              'int': 3,
              'verbosity': True,
              'v': True}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--int', '3', '--verbosity'])
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity_tree(json):
    output = {'root.cmd': 'int',
              'root.int': 3,
              'root.verbosity': True,
              'root.v': True}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--root.int', '3', '--root.verbosity'])
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity_tree_flatten(json):
    output = {'root.cmd': 'int',
              'root.int': 3,
              'root.verbosity': True,
              'root.v': True}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['int', '--int', '3', '--verbosity'])
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity_short(json):
    output = {'cmd': 'int',
              'int': 3,
              'verbosity': True,
              'v': True}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--int', '3', '-v'])
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity_short_store_false(json):
    output = {'cmd': 'int',
              'int': 3,
              'verbosity': None,
              'v': True}
    config = get_config(json, default_verbosity=None, add_store_false=True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--int', '3', '-v'])
    output = {'cmd': 'int',
              'int': 3,
              'verbosity': False,
              'v': False}
    assert to_dict(config.value.get()) == output
    parser.parse_args(['int', '--int', '3', '-nv'])
    output = {'cmd': 'int',
              'int': 3,
              'verbosity': True,
              'v': True}
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity_short_no(json):
    output = {'cmd': 'int',
              'int': 3,
              'verbosity': False,
              'v': False}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--int', '3', '-nv'])
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity_short_tree(json):
    output = {'root.cmd': 'int',
              'root.int': 3,
              'root.verbosity': True,
              'root.v': True}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--root.int', '3', '-v'])
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity_short_tree_flatten(json):
    output = {'root.cmd': 'int',
              'root.int': 3,
              'root.verbosity': True,
              'root.v': True}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['int', '--int', '3', '-v'])
    assert to_dict(config.value.get()) == output


def test_readme_int_verbosity_short_and_not(json):
    output = {'cmd': 'int',
              'int': 3,
              'verbosity': False,
              'v': False}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['int', '--int', '3', '-v', '-nv'])
    assert to_dict(config.value.get()) == output


def test_readme_str(json):
    output = {'cmd': 'str',
              'str': 'value',
              'verbosity': False,
              'v': False}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['str', '--str', 'value'])
    assert to_dict(config.value.get()) == output


def test_readme_str_tree(json):
    output = {'root.cmd': 'str',
              'root.str': 'value',
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['str', '--root.str', 'value'])
    assert to_dict(config.value.get()) == output


def test_readme_str_tree_flatten(json):
    output = {'root.cmd': 'str',
              'root.str': 'value',
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['str', '--str', 'value'])
    assert to_dict(config.value.get()) == output


def test_readme_str_int(json):
    output = {'cmd': 'str',
              'str': '3',
              'verbosity': False,
              'v': False}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['str', '--str', '3'])
    assert to_dict(config.value.get()) == output


def test_readme_str_int_tree(json):
    output = {'root.cmd': 'str',
              'root.str': '3',
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['str', '--root.str', '3'])
    assert to_dict(config.value.get()) == output


def test_readme_str_int_tree_flatten(json):
    output = {'root.cmd': 'str',
              'root.str': '3',
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['str', '--str', '3'])
    assert to_dict(config.value.get()) == output


def test_readme_list_single(json):
    output = {'cmd': 'list',
              'list': ['a'],
              'verbosity': False,
              'v': False}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['list', '--list', 'a'])
    assert to_dict(config.value.get()) == output


def test_readme_list(json):
    output = {'cmd': 'list',
              'list': ['a', 'b', 'c'],
              'verbosity': False,
              'v': False}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['list', '--list', 'a', 'b', 'c'])
    assert to_dict(config.value.get()) == output


def test_readme_list_tree(json):
    output = {'root.cmd': 'list',
              'root.list': ['a', 'b', 'c'],
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['list', '--root.list', 'a', 'b', 'c'])
    assert to_dict(config.value.get()) == output


def test_readme_list_tree_flatten(json):
    output = {'root.cmd': 'list',
              'root.list': ['a', 'b', 'c'],
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['list', '--list', 'a', 'b', 'c'])
    assert to_dict(config.value.get()) == output


def test_readme_list_uniq(json):
    output = {'cmd': 'list',
              'list': ['a'],
              'verbosity': False,
              'v': False}
    config = get_config(json)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['list', '--list', 'a'])
    assert to_dict(config.value.get()) == output


def test_readme_list_uniq_tree(json):
    output = {'root.cmd': 'list',
              'root.list': ['a'],
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['list', '--root.list', 'a'])
    assert to_dict(config.value.get()) == output


def test_readme_list_uniq_tree_flatten(json):
    output = {'root.cmd': 'list',
              'root.list': ['a'],
              'root.verbosity': False,
              'root.v': False}
    config = get_config(json, True)
    parser = TiramisuCmdlineParser(config, 'prog.py', fullpath=False)
    parser.parse_args(['list', '--list', 'a'])
    assert to_dict(config.value.get()) == output


def test_readme_longargument(json):
    output = {'cmd': 'list',
              'list': ['a'],
              'verbosity': True,
              'v': True}
    config = get_config(json, add_long=True)
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['list', '--list', 'a', '--v'])
    assert to_dict(config.value.get()) == output


def test_readme_unknown_key(json):
    output1 = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: unrecognized arguments: --unknown
"""
    output2 = """usage: prog.py [-h] [-v] [-nv] {str,list,int,none}
prog.py: error: unrecognized arguments: --root.unknown
"""
    parser = TiramisuCmdlineParser(get_config(json, True), 'prog.py', fullpath=False, formatter_class=TestHelpFormatter)
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--unknown'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output1

    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args(['--root.unknown'])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output2
