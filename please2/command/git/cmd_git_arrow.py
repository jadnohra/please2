import subprocess
import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import which_branch, make_error_result, run_git_get_lines


class CommandGitArrow(Command):

    def help(self):
        return self.key() + ' (staging|remote)/source-branch (staging|remote)/target-branch'

    def opt_keys(self):
        return set(['@', 'trace'])

    def key(self):
        return 'git ='
        
    def run_match(self, args, params):
        def find_src_target(args, params):
            cands = [x for x in args.args if any(x.startswith(y) for y in ['staging/', 'remote/'])]
            if len(cands) != 2:
                return None
            return cands
        curr_branch = which_branch(args, params)
        if curr_branch is not None:
            src_target = find_src_target(args, params)
            if src_target is not None:
                result = {}
            else:
                result = {
                    'error': 'I could not extract the source and target paramters',
                }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandGitArrow())
