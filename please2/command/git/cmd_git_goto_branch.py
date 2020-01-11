import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import checkout_branch, run_git_get_lines
from please2.util.args import get_positional_after


class CommandGitGotoBranch(Command):

    def help(self):
        return self.key() + ' <branch-name> [@ <dir>]'

    def opt_keys(self):
        return set(['@'])


    def key(self):
        return 'git goto branch'

    def run_match(self, args, params):
        name = get_positional_after(args.args, self.key().split()[-1])
        checkout_branch(args, params, name)
        return Match('')


reg_cmd.register_command(CommandGitGotoBranch())
