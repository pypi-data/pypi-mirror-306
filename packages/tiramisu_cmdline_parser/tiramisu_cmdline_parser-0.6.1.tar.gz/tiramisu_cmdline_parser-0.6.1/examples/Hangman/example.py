#!/usr/bin/env python3
"""Hangman example
"""


from random import choice
import unicodedata
import re
from os import unlink
from os.path import isfile
from tiramisu import RegexpOption, OptionDescription, Config, IntOption, UnicodeOption, BoolOption, ParamOption, Params, default_storage
from tiramisu_cmdline_parser import TiramisuCmdlineParser


LANG = 'fr_FR'
DICT_FILE = '/usr/share/myspell/{}.dic'.format(LANG)
WORD_REGEXP = re.compile(r'^[a-z]{7,12}$')
PROPOSALS_LEN = 27
NB_PROPOSALS = 6


def remove_accent(word):
    """remove all accent"""
    word = unicodedata.normalize('NFD', word)
    return word.encode('ascii', 'ignore').decode()


def get_random_word():
    """get line randomly in myspell file
    """
    with open(DICT_FILE, 'r') as file_content:
        word = choice(file_content.readlines()).strip()
        if word.endswith('/S.'):
            word = word[:-3]
        if word.endswith('/X.'):
            word = word[:-3]
        if word.endswith('/F.'):
            word = word[:-3]
        if word.endswith('/a0p+') or word.endswith('/d0p+') or word.endswith('/a3p+'):
            word = word[:-5]
        if not WORD_REGEXP.search(remove_accent(word)):
            return get_random_word()
        return word


def display_uncomplete_word(word, *proposals):
    """display response with proposals
    """
    if display_proposals_left(display_misses(word, *proposals)) == 0:
        return word
    display = ['-'] * len(word)
    for idx, char in enumerate(remove_accent(word)):
        if char in proposals:
            display[idx] = word[idx]
    return ''.join(display)


def display_misses(word, *proposals):
    """display all proposals
    """
    ret = list(set(proposals) - set(list(remove_accent(word))))
    if None in ret:
        ret.remove(None)
    ret.sort()
    return ' '.join(ret)


def validate_misses(misses):
    if display_proposals_left(misses) == 0:
        raise ValueError('No more guest possible')


def display_proposals_left(misses):
    if not misses:
        return NB_PROPOSALS
    return max(NB_PROPOSALS - len(misses.split(' ')), 0)


def display_proposal(word, *proposals):
    if display_uncomplete_word(word, *proposals) == word:
        return False
    return display_proposals_left(display_misses(word, *proposals)) != 0


class ProposalOption(RegexpOption):
    __slots__ = tuple()
    _regexp = re.compile(r'^[a-z]$')
    _display_name = 'proposal'


def main():
    options = []
    proposal = None
    word = UnicodeOption('word',
                         'Word',
                         properties=('hidden', 'force_store_value'),
                         callback=get_random_word)
    proposals = [ParamOption(word)]
    for idx in range(PROPOSALS_LEN):
        requires = [{'option': 'self',
                     'expected': None,
                     'action': 'hidden',
                     'inverse': True}]
        if proposal is not None:
            display = BoolOption('display{}'.format(idx),
                                 'Display {}'.format(idx),
                                 properties=('hidden',),
                                 callback=display_proposal,
                                 callback_params=Params(tuple(proposals)))
            options.append(display)
            requires.append({'option': proposal,
                             'expected': None,
                             'action': 'disabled'})
            requires.append({'option': display,
                             'expected': False,
                             'action': 'disabled'})

        proposal = ProposalOption('guess{}'.format(idx),
                                  'Guess {}'.format(idx),
                                  requires=requires,
                                  properties=('positional', 'mandatory'))
        #FIXME maximum recursion ...
        #if proposals:
        #    proposal.impl_add_consistency('not_equal', proposals[0])

        proposals.append(ParamOption(proposal, True))
        options.append(proposal)
    #
    proposal_word = UnicodeOption('proposal_word',
                                  'Word',
                                  properties=('frozen',),
                                  callback=display_uncomplete_word,
                                  callback_params=Params(tuple(proposals)))
    misses = UnicodeOption('misses',
                           'Misses',
                           properties=('frozen',),
                           callback=display_misses,
                           callback_params=Params(tuple(proposals)),
                           validator=validate_misses)
    proposals_left = IntOption('proposals_left',
                               'Proposals left',
                               properties=('frozen',),
                               callback=display_proposals_left,
                               callback_params=Params(ParamOption(misses)))
    #descr = OptionDescription('proposals',
    #                          'Suggesting letters',
    #                          options)
    default_storage.setting(engine='sqlite3', name='hangman_cmdline_parser')
    config = Config(OptionDescription('root', 'root', [word, proposal_word, misses, proposals_left] + options), persistent=True, session_id='hangman')
    config.property.read_write()
    try:
        parser = TiramisuCmdlineParser(config)
        parser.parse_args(valid_mandatory=False)
    except ValueError:
        # if no more suggestion
        pass
    filename = '/tmp/tiramisu.db'
    lost = False
    for name in ['proposal_word', 'misses', 'proposals_left']:
        option = config.option(name)
        try:
            value = option.value.get()
            print('{}: {}'.format(option.option.doc(), value))
        except ValueError as err:
            lost = True
            err.prefix = ''
            print(option.option.doc(), str(err))
            if isfile(filename):
                unlink(filename)
    if not lost and \
            config.option('proposal_word').value.get() == config.forcepermissive.option('word').value.get():
        print('You win')
        if isfile(filename):
            unlink(filename)

if __name__ == "__main__":
    main()
