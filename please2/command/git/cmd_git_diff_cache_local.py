import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, get_ws_modifs, pprint_ws_modifs
from please2.util.args import get_positional_after

class CommandGitDiffWsCache(Command):

    def help(self):
        return self.key() + ' [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git diff cache-local'

    def run_match(self, args, params):
        modifs = get_ws_modifs(args, params, ws_cache=False, cache_local=True)
        if len(modifs) == 0:
            return Match(result = {'note': 'There are no modifications'})
        pprint_ws_modifs(modifs, ws_cache=False, cache_local=True)
        # TODO return trees instead of pprint
        return Match('')

reg_cmd.register_command(CommandGitDiffWsCache())
