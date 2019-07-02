import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run_get_lines
from please2.util.args import get_positional_after

class CommandExtract(Command):

    def help(self):
        return self.key() + ' <file> [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'extract'

    def run_match(self, args, params):
        file = get_positional_after(args.args, self.key())
        if file.endswith('.rar'):
            run_get_lines(args, params, ['unrar', 'e', file])
            return Match('')
        else:
            return Match(result = {
                'error': "Apologies, I don't know how to extract this file type",
            })


reg_cmd.register_command(CommandExtract())
