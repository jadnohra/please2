import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from please2.util.args import get_positional_after
from please2.util.run import run

class CommandAlternativesChoose(Command):

    def help(self):
        return self.key() + ' <key>'

    def opt_keys(self):
        return set()

    def key(self):
        return 'alternatives choose'

    def run_match(self, args, params):
        key = get_positional_after(args.args, self.key().split()[-1])
        run(args, params, ['sudo', 'update-alternatives', '--config', key])
        return Match('')


reg_cmd.register_command(CommandAlternativesChoose())
