import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, get_ws_modifs, pprint_ws_modifs, \
                            git_add, git_commit
from please2.util.args import get_positional_after
from please2.util.input import resolve_smart_input

class CommandGitMoveCacheLocal(Command):

    def help(self):
        return self.key() + ' <commit-message> [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git move cache-local'

    def run_match(self, args, params):
        commit_msg = get_positional_after(args.args, self.key().split()[-1])
        modifs = get_ws_modifs(args, params, ws_cache=False, cache_local=True)
        if len(modifs) == 0:
            return Match(result = {'note': 'Everything is already in sync ;)'})
        pprint_ws_modifs(modifs)
        commit_msg = resolve_smart_input(commit_msg, prompt_str=' Commit message: ')
        exitcode_ok = exitcode_ok and git_commit(args, params, commit_msg=commit_msg) == 0
        if exitcode_ok:
            return Match('')
        else:
            return Match(result = {'error': 'Panic >:('})

reg_cmd.register_command(CommandGitMoveCacheLocal())
