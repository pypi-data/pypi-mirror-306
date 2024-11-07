int_long = IntOption('int', 'integer')
parser.add_arguments([BoolOption('v', 'increase output verbosity', default=False),
                      int_long,
                      SymLinkOption('i', int_long)])
