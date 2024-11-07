from io import StringIO
import pytest
from contextlib import redirect_stderr


from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import IntOption, StrOption, BoolOption, ChoiceOption, \
                     SymLinkOption, OptionDescription, Config
try:
    from tiramisu_api import Config as JsonConfig
    params = ['tiramisu']
    #params = ['tiramisu', 'tiramisu-json']
except:
    params = ['tiramisu']

from .utils import to_dict


@pytest.fixture(params=params)
def json(request):
    return request.param


def test_short(json):
    def get_config():
        list_ = StrOption('list',
                          'list string option')
        slist_ = SymLinkOption('l', list_)
        root = OptionDescription('root',
                                 'root',
                                 [list_,
                                  slist_,
                                  ])
        config = Config(root)
        config.property.read_write()
        if json != 'tiramisu':
            config = JsonConfig(config.option.dict())
        return config
    #
    output = {'list': None, 'l': None}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args([])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': 'a', 'l': 'a'}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--list', 'a'])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': 'a', 'l': 'a'}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['-l', 'a'])
    assert to_dict(config.value.get()) == output
    #
    assert config.option('list').value.get() == config.option('l').value.get()
    assert config.option('list').owner.get() == config.option('l').owner.get()
    assert config.option('list').owner.isdefault() == config.option('l').owner.isdefault()


def test_short_mandatory(json):
    def get_config():
        list_ = StrOption('list',
                          'list string option',
                          properties=('mandatory',))
        slist_ = SymLinkOption('l', list_)
        root = OptionDescription('root',
                                 'root',
                                 [list_,
                                  slist_,
                                  ])
        config = Config(root)
        config.property.read_write()
        if json != 'tiramisu':
            config = JsonConfig(config.option.dict())
        return config
    #
    output = """usage: prog.py [-h] -l LIST
prog.py: error: the following arguments are required: --list
"""
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args([])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output
    #
    output = {'list': 'a', 'l': 'a'}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--list', 'a'])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': 'a', 'l': 'a'}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['-l', 'a'])
    assert to_dict(config.value.get()) == output


def test_short_multi(json):
    def get_config():
        list_ = StrOption('list',
                          'list string option',
                          multi=True)
        slist_ = SymLinkOption('l', list_)
        root = OptionDescription('root',
                                 'root',
                                 [list_,
                                  slist_,
                                  ])
        config = Config(root)
        config.property.read_write()
        if json != 'tiramisu':
            config = JsonConfig(config.option.dict())
        return config
    #
    output = {'list': [], 'l': []}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args([])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': ['a'], 'l': ['a']}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--list', 'a'])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': ['a', 'b'], 'l': ['a', 'b']}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--list', 'a', 'b'])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': ['a'], 'l': ['a']}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['-l', 'a'])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': ['a', 'b'], 'l': ['a', 'b']}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['-l', 'a', 'b'])
    assert to_dict(config.value.get()) == output


def test_short_multi_mandatory(json):
    def get_config():
        list_ = StrOption('list',
                          'list string option',
                          multi=True,
                          properties=('mandatory',))
        slist_ = SymLinkOption('l', list_)
        root = OptionDescription('root',
                                 'root',
                                 [list_,
                                  slist_,
                                  ])
        config = Config(root)
        config.property.read_write()
        if json != 'tiramisu':
            config = JsonConfig(config.option.dict())
        return config
    #
    output = """usage: prog.py [-h] -l LIST [LIST ...]
prog.py: error: the following arguments are required: --list
"""
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    f = StringIO()
    with redirect_stderr(f):
        try:
            parser.parse_args([])
        except SystemExit as err:
            assert str(err) == "2"
        else:
            raise Exception('must raises')
    assert f.getvalue() == output
    #
    output = {'list': ['a'], 'l': ['a']}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--list', 'a'])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': ['a', 'b'], 'l': ['a', 'b']}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['--list', 'a', 'b'])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': ['a'], 'l': ['a']}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['-l', 'a'])
    assert to_dict(config.value.get()) == output
    #
    output = {'list': ['a', 'b'], 'l': ['a', 'b']}
    config = get_config()
    parser = TiramisuCmdlineParser(config, 'prog.py')
    parser.parse_args(['-l', 'a', 'b'])
    assert to_dict(config.value.get()) == output
