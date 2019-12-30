import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.tree_algo import recurse_filter_node_copy, \
                                    recurse_label_node_index
from please2.util.pprint import pprint_tree_node
from please2.util.input import input_indices
from please2.util.chain import find_tree

class CommandFilterSelect(Command):

    def key(self):
        return 'select'

    def layer_name(self):
        return 'select'

    def run_match(self, args, params):
        def filter_keep_node(node, sel_indices):
            return node.label_layer(self.layer_name()).value() in sel_indices
        tree_k, tree_v = find_tree(params)
        result = {}
        if tree_k is not None:
            recurse_label_node_index(tree_v, layer_name=self.layer_name())
            pprint_tree_node(tree_v, key=tree_k, index_label_key=self.layer_name())
            sel_indices = input_indices('Select: ')
            filtered_tree_root = recurse_filter_node_copy(tree_v, lambda node: filter_keep_node(node, sel_indices))
            if filtered_tree_root is None:
                filtered_tree_root = TreeNode('')
            result = {
                tree_k+'-filtered': filtered_tree_root
            }
        return Match(result)


reg_cmd.register_command(CommandFilterSelect())
