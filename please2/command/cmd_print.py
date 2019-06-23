import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run_get_lines
from please2.util.args import get_positional_after

class CommandPrint(Command):

    def help(self):
        return self.key() + ' <file> [two-sided]'

    def opt_keys(self):
        return set(['two-sided'])

    def key(self):
        return 'print'

    def run_match(self, args, params):
        two_sided = 'two-sided' in args.args
        file = get_positional_after(args.args, self.key())
        opt_args = ['-o', 'sides=two-sided-long-edge'] if two_sided else []
        run_get_lines(args, params, ['lp', file] + opt_args)
        return Match('')


reg_cmd.register_command(CommandPrint())
