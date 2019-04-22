import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.reg_cmd import all_commands

class CommandHelp(Command):

    def key(self):
        return 'help'

    def run_match(self, params):
        result = sorted([x.help() for x in all_commands()])
        return Match(result)


reg_cmd.register_command(CommandHelp())
