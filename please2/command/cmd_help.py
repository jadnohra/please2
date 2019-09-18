import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.reg_cmd import all_commands
from please2.util.args import get_positional_after

class CommandHelp(Command):

    def help(self):
        return self.key() + ' <key>'

    def key(self):
        return 'help'

    def run_match(self, args, params):
        key = get_positional_after(args.args, self.key())
        help_list = [x.help() for x in all_commands()]
        if key is not None:
            help_list = [x for x in help_list if key in x]
        result = sorted(help_list)
        return Match(result)


reg_cmd.register_command(CommandHelp())
