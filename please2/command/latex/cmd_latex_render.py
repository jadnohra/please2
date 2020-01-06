import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run_get_lines
from please2.util.args import get_positional_after

class CommandLatexRender(Command):

    def help(self):
        return self.key() + ' <latex-code>'

    def opt_keys(self):
        return set()

    def key(self):
        return 'latex render'

    def run_match(self, args, params):
        latex_code = get_positional_after(args.args, self.key().split()[-1])
        print(latex_code)
        return Match('')


reg_cmd.register_command(CommandLatexRender())
