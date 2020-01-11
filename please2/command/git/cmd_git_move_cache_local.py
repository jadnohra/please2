import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, get_ws_modifs_tree, git_commit_modifs
from please2.util.args import get_positional_after
from please2.util.input import resolve_smart_input
from please2.util.chain import find_tree_as_list, tree_to_list

class CommandGitMoveCacheLocal(Command):

    def help(self):
        return self.key() + ' ["commit-message"] [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git move cache-local'

    def run_match(self, args, params):
        modifs = find_tree_as_list(params)
        if modifs is None:
            modifs_tree = get_ws_modifs_tree(args, params, ws_cache=False, cache_local=True)
            modifs = tree_to_list(modifs_tree)
        if len(modifs) == 0:
            return Match(result = {'note': 'Nothing to move'})
        commit_msg = get_positional_after(args.args, self.key().split()[-1])
        if commit_msg is not None:
            if commit_msg in self.opt_keys() or commit_msg.startswith("["): # Hack to handle a lazy optional commit message (e.g when there are no modifications)
                commit_msg = None
        commit_msg = resolve_smart_input(commit_msg, prompt_str=' Commit message: ')
        exitcode_ok = (git_commit_modifs(args, params, modifs, commit_msg=commit_msg) == 0)
        if exitcode_ok:
            return Match('')
        else:
            return Match(result = {'error': 'Panic >:('})

reg_cmd.register_command(CommandGitMoveCacheLocal())
