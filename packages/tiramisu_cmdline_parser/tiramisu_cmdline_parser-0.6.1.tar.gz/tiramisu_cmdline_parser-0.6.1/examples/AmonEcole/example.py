#!/usr/bin/env python3
"""AmonEcole example
"""

from examples.AmonEcole import amonecole
from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import default_storage


def display_name(option, dyn_name):
    return "--" + option.impl_getpath()


def main():
    """AmonEcole
    """
    default_storage.setting(engine='sqlite3', name='amonecole_cmdline_parser')
    config = amonecole.get_config(display_name=display_name)
    config.property.read_write()
    config.property.pop('expert')
    config.property.pop('normal')
    config.property.add('expert')
    config.property.add('normal')
    config.permissive.add('expert')
    config.permissive.add('normal')
    parser = TiramisuCmdlineParser(config, root='creole')
    #parser.parse_args(valid_mandatory=False)
    parser.parse_args()


if __name__ == "__main__":
    main()
