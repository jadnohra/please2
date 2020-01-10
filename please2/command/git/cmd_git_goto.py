import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import git_reset, run_git_get_lines
from please2.util.args import get_positional_after


class CommandGitGoto(Command):

    def help(self):
        return self.key() + ' <key (commit-hash, tag, [last])> [kill local changes] [@ <dir>]'

    def opt_keys(self):
        return set(['@', 'kill local changes'])


    def key(self):
        return 'git goto'

    def run_match(self, args, params):
        name = get_positional_after(args.args, self.key().split()[-1])
        if name == '[last]':
            name = None
        hard = 'kill local changes' in ' '.join(args.args_low)
        git_reset(args, params, name, soft=(not hard))
        return Match('')


reg_cmd.register_command(CommandGitGoto())
