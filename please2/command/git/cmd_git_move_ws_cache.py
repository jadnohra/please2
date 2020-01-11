import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, get_ws_modifs, pprint_ws_modifs, \
                            git_add, git_commit
from please2.util.args import get_positional_after
from please2.util.input import resolve_smart_input

class CommandGitMoveWsCache(Command):

    def help(self):
        return self.key() + ' [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git move ws-cache'

    def run_match(self, args, params):
        modifs = get_ws_modifs(args, params, ws_cache=True, cache_local=False)
        if len(modifs) == 0:
            return Match(result = {'note': 'Everything is already in sync ;)'})
        pprint_ws_modifs(modifs)
        exitcode_ok = git_add(args, params) == 0
        if exitcode_ok:
            return Match('')
        else:
            return Match(result = {'error': 'Panic >:('})

reg_cmd.register_command(CommandGitMoveWsCache())
