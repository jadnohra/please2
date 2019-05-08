import platform
from copy import copy
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode


class CommandFlatten(Command):

    def key(self):
        return 'flatten'

    def run_match(self, args, params):
        def find_tree(params):
            for k,v in params.get('prev_result', {}).items():
                if isinstance(v, TreeNode):
                    return k, v
            return (None, None)
        def join(a, b):
            return a + '/' + b if len(a) else b
        def flatten_tree(node, path, flat_tree_root):
            node_path = join(path, node.name())
            if node.is_leaf():
                flat_node = copy(node)
                flat_node.set_name(node_path)
                if flat_node.has_label_layer():
                    layer = flat_node.label_layer()
                    layer.set_name(layer.name() + '-flat')
                flat_tree_root.add_child(flat_node)
            else:
                for child in node.children():
                    flatten_tree(child, node_path, flat_tree_root)
        tree_k, tree_v = find_tree(params)
        result = {}
        if tree_k is not None:
            flat_tree_root = TreeNode()
            flat_tree_root.set_name('')
            flatten_tree(tree_v, '', flat_tree_root)
            flat_tree_root.sort_children()
            result = {
                tree_k+'-flat': flat_tree_root
            }
        return Match(result)


reg_cmd.register_command(CommandFlatten())
