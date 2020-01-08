import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.args import get_positional_after
from please2.util.chain import find_tree_as_list
from please2.util.platform import display_any

class CommandDisplay(Command):

    def help(self):
        return self.key() + ' <file>'

    def opt_keys(self):
        return set()

    def key(self):
        return 'display'

    def run_match(self, args, params):
        filenames = find_tree_as_list(params)
        if filenames is None:
            filenames = [get_positional_after(args.args, self.key().split()[-1])]
        for filename in filenames:
            display_any(args, params, filename)
        return Match('')


reg_cmd.register_command(CommandDisplay())
