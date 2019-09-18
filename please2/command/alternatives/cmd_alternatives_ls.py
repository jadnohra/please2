import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_alternatives_util import get_all_alternatives

class CommandAlternativesLs(Command):

    def help(self):
        return self.key()

    def opt_keys(self):
        return set()


    def key(self):
        return 'alternatives ls'

    def layer_name(self):
        return 'alternatives'


    def run_match(self, args, params):
        def create_branch_node(name):
            node = TreeNode()
            node.set_name(name)
            return node
        found_alts = get_all_alternatives(args, params)
        root_node = create_branch_node('.')
        if len(found_alts):
            for alt in found_alts:
                fields = alt.split()
                if fields[1] != 'auto':
                    root_node.add_child(TreeNode( (fields[0], fields[2]) ))
            result = { self.layer_name(): root_node}
        else:
            result = { 'info' : 'It seems there are not alternatives' }
        return Match(result)


reg_cmd.register_command(CommandAlternativesLs())
