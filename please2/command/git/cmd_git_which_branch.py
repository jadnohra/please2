import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import which_branch, make_error_result


class CommandGitWhichBranch(Command):

    def help(self):
        return self.key() + ' [@ <dir>] [trace]'

    def opt_keys(self):
        return set(['@', 'trace'])


    def key(self):
        return 'git which branch'

    def run_match(self, args, params):
        found_branch = which_branch(args, params)
        if found_branch:
            result = {
                'branch': found_branch,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandGitWhichBranch())
