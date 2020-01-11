import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, get_ws_modifs_tree, \
                            git_add_modifs, git_commit_modifs, git_diff_layer_name
from please2.util.args import get_positional_after
from please2.util.input import resolve_smart_input
from please2.util.chain import find_tree, tree_to_list

class CommandGitMoveWsLocal(Command):

    def help(self):
        return self.key() + ' <commit-message> [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git move ws-local'

    def run_match(self, args, params):
        def is_node_ws_cache(node):
            return node.get_label_layer(git_diff_layer_name()).value()[0] not in ['_', 'D']
        def is_node_cache_local(node):
            return node.get_label_layer(git_diff_layer_name()).value()[1] != '_'

        tree_k, modifs_tree = find_tree(params)
        if tree_k is None:
            modifs_tree = get_ws_modifs_tree(args, params, ws_cache=True, cache_local=True)

        ws_cache_modifs = tree_to_list(modifs_tree, include_node_func=is_node_ws_cache)
        cache_local_modifs = tree_to_list(modifs_tree, include_node_func=is_node_cache_local)

        if len(ws_cache_modifs) + len(cache_local_modifs) == 0:
            return Match(result = {'note': 'Nothing to move'})

        if len(ws_cache_modifs):
            exitcode_ok = (git_add_modifs(args, params, ws_cache_modifs) == 0)
            if not exitcode_ok:
                return Match(result = {'error': 'Panic >:('})

        commit_msg = get_positional_after(args.args, self.key().split()[-1])
        if commit_msg is not None:
            if commit_msg in self.opt_keys() or commit_msg.startswith("["): # Hack to handle a lazy optional commit message (e.g when there are no modifications)
                commit_msg = None
        commit_msg = resolve_smart_input(commit_msg, prompt_str=' Commit message: ')

        cumulated_local_modifs = ws_cache_modifs + cache_local_modifs

        exitcode_ok = (git_commit_modifs(args, params, cumulated_local_modifs, commit_msg=commit_msg) == 0)
        if exitcode_ok:
            return Match('')
        else:
            return Match(result = {'error': 'Panic >:('})

reg_cmd.register_command(CommandGitMoveWsLocal())
