import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import generic_match, generic_key_args, generic_parametrize, Match


class CommandWhichOS:

    def key(self):
        return 'which OS'

    def match(self, str_args, str_args_low):
        return generic_match(self, str_args, str_args_low)

    def parametrize(self, str_args, str_args_low):
        return generic_parametrize(generic_key_args(self),
                                    str_args, str_args_low)

    def run_match(self, params):
        result = {
            'OS': platform.system(),
            'release': platform.release()
            }
        if result['OS'].lower() == 'linux':
            result['distro'] = platform.linux_distribution()
        return Match(result)


reg_cmd.register_command(CommandWhichOS())
