import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, get_ws_modifs_tree, git_diff_layer_name
from please2.util.args import get_positional_after

class CommandGitLsDiffsWsCache(Command):

    def help(self):
        return self.key() + ' [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git ls diffs ws-cache'

    def layer_name(self):
        return git_diff_layer_name()

    def run_match(self, args, params):
        root = get_ws_modifs_tree(args, params, ws_cache=True, cache_local=False)
        return Match({self.layer_name():root})

reg_cmd.register_command(CommandGitLsDiffsWsCache())
