import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.tree_algo import recurse_filter_node_copy
from please2.util.chain import find_tree

class CommandFilter(Command):

    def key(self):
        return 'filter'

    def run_match(self, args, params):
        def filter_keep_node(node, key):
            return key in node.name()
        filter_key = args.args[len(self.key().split())]
        tree_k, tree_v = find_tree(params)
        result = {}
        if tree_k is not None:
            filtered_tree_root = recurse_filter_node_copy(tree_v, lambda node: filter_keep_node(node, filter_key))
            result = {
                tree_k+'-filtered': filtered_tree_root
            }
        return Match(result)


reg_cmd.register_command(CommandFilter())
