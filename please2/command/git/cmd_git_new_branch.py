import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, run_git_get_lines
from please2.util.args import get_positional_after


class CommandGitNewBranch(Command):

    def help(self):
        return self.key() + ' <branch-name> [@ <dir>]'

    def opt_keys(self):
        return set(['@'])


    def key(self):
        return 'git new branch'

    def run_match(self, args, params):
        name = get_positional_after(args.args, self.key().split()[-1])
        run_git_get_lines(args, params, ['branch', name])
        return Match('')


reg_cmd.register_command(CommandGitNewBranch())
