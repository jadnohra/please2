import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode


class CommandFlatten(Command):

    def key(self):
        return 'flatten'

    def run_match(self, params):
        def find_tree(params):
            for k,v in params.get('prev_result', {}).items():
                if isinstance(v, TreeNode):
                    return k, v
            return (None, None)
        def join(a, b):
            return a + '/' + b
        def flatten_tree(node, path, flat):
            node_path = join(path, node.name())
            if node.is_leaf():
                flat.append(node_path)
            else:
                for child in node.children():
                    flatten_tree(child, node_path, flat)
        tree_k, tree_v = find_tree(params)
        result = {}
        if tree_k is not None:
            flat_tree = []
            flatten_tree(tree_v, '', flat_tree)
            result = {
                tree_k+'-flat': flat_tree
            }
        return Match(result)


reg_cmd.register_command(CommandFlatten())
