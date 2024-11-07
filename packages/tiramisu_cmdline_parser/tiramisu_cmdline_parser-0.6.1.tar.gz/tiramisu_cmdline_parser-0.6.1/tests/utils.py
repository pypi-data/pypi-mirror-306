from argparse import ArgumentDefaultsHelpFormatter
from tiramisu_cmdline_parser.api import TiramisuHelpFormatter


def _leadership_to_dict(dico, ret):
    leader, *followers = list(dico)
    ret[leader.path()] = dico[leader]
    for follower in followers:
        follower_path = follower.path()
        ret.setdefault(follower_path, []).append(dico[follower])


def _to_dict(dico, ret):
    for key, value in dico.items():
        if key.isoptiondescription():
            if key.isleadership():
                _leadership_to_dict(value, ret)
            else:
                _to_dict(value, ret)
        else:
            ret[key.path()] = value


def to_dict(dico):
    ret = {}
    _to_dict(dico, ret)
    return ret


class TestHelpFormatter(TiramisuHelpFormatter, ArgumentDefaultsHelpFormatter):
    def __init__(self,
                 *args,
                 **kwargs,
                 ):
        return super().__init__(*args, **kwargs, width=5000)
