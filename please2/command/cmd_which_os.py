import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match


class CommandWhichOS(Command):

    def key(self):
        return 'which OS'

    def run_match(self, args, params):
        result = {
            'OS': platform.system(),
            'release': platform.release()
            }
        if result['OS'].lower() == 'linux':
            result['distro'] = platform.linux_distribution()
        return Match(result)


reg_cmd.register_command(CommandWhichOS())
