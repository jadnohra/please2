import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, get_ws_modifs_tree, git_add_modifs
from please2.util.args import get_positional_after
from please2.util.input import resolve_smart_input
from please2.util.chain import find_tree_as_list, tree_to_list

class CommandGitMoveWsCache(Command):

    def help(self):
        return self.key() + ' [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git ws-cache'

    def run_match(self, args, params):
        modifs = find_tree_as_list(params)
        if modifs is None:
            modifs_tree = get_ws_modifs_tree(args, params, ws_cache=True, cache_local=False)
            modifs = tree_to_list(modifs_tree)
        if len(modifs) == 0:
            return Match(result = {'note': 'Nothing to move'})
        exitcode_ok = (git_add_modifs(args, params, modifs) == 0)
        if exitcode_ok:
            return Match('')
        else:
            return Match(result = {'error': 'Panic >:('})

reg_cmd.register_command(CommandGitMoveWsCache())
