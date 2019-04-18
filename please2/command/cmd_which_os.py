import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import generic_match, generic_key_args, Match


class CommandWhichOS:

    def key(self):
        return 'which OS'

    def match(self, args):
        return generic_match(self, args)

    def parametrize(self, args):
        return {} if args.match(generic_key_args(self)) else None

    def run_match(self, params):
        result = {
            'OS': platform.system(),
            'release': platform.release()
            }
        if result['OS'].lower() == 'linux':
            result['distro'] = platform.linux_distribution()
        return Match(result)


reg_cmd.register_command(CommandWhichOS())
