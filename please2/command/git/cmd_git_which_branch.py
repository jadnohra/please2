import subprocess
import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, run_git_get_lines


class CommandGitWhichBranch(Command):

    def help(self):
        return self.key() + ' [@ <dir>] [trace]'

    def opt_keys(self):
        return set(['@', 'trace'])


    def key(self):
        return 'git which branch'

    def run_match(self, args, params):
        result_lines = run_git_get_lines(args, params, ['branch'])
        found_branch = None
        for line in result_lines:
            if line.startswith('* '):
                found_branch = line.split()[1]
                break
        if found_branch:
            result = {
                'branch': found_branch,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandGitWhichBranch())
