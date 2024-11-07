str_long = StrOption('foo', 'foo help')
str_short = SymLinkOption('f', str_long)
parser.add_arguments([str_long, str_short])
