import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
#from .cmd_git_util import get_ws_modifs, include_filter_ws_modifs
from please2.util.args import get_positional_after
from please2.util.run import run

class CommandGitLsDiffsWsRemote(Command):

    def help(self):
        return self.key() + ' [@ <dir>]'

    def references(self):
        return ['https://stackoverflow.com/questions/1800783/how-to-compare-a-local-git-branch-with-its-remote-branch']

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git diffs ws-remote'

    def run_match(self, args, params):
        # TODO: Fix this
        '''
        ws_modifs = get_ws_modifs(args, params, ws_cache=True, cache_local=False)
        untracked_ws_modifs = include_filter_ws_modifs(ws_modifs, include_tracked=False)
        print('\nNew files:')
        if len(untracked_ws_modifs) == 0:
            print(' N/A')
        else:
            #pprint_ws_modifs(untracked_ws_modifs, header=None)
            pass
        print('Existing files:')
        run(args, params, ['git', 'diff', '@{push}', '--compact-summary'])
        # Not perfect, untracked files are missing
        # TODO return trees instead of pprint, analyze results
        return Match('')
        '''

reg_cmd.register_command(CommandGitLsDiffsWsRemote())
