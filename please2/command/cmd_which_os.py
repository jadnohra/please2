import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import generic_match, Match


class CommandWhichOS:

    def match(self, string):
        return generic_match(self, string)

    def parametrize(self, string):
        if string.lower().startswith('which OS'.lower()):
            return {}
        return None

    def run_match(self, params):
        result = {
            'OS': platform.system(),
            'release': platform.release()
            }
        if result['OS'].lower() == 'linux':
            result['distro'] = platform.linux_distribution()
        return Match(result)


reg_cmd.register_command(CommandWhichOS())
