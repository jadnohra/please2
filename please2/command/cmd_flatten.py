import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode


class CommandFlatten(Command):

    def key(self):
        return 'flatten'

    def run_match(self, params):
        print(params['prev_result'])
        if isinstance(params['prev_result'], TreeNode):
            print('GOT IT')
        result = {
            }
        return Match(result)


reg_cmd.register_command(CommandFlatten())
