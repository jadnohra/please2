import platform
from copy import copy
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode


class CommandCount(Command):

    def key(self):
        return 'count'

    def run_match(self, params):
        # TODO
        return None


reg_cmd.register_command(CommandCount())
