import platform
from copy import copy
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.tree_algo import flatten_tree
from please2.util.chain import find_tree


class CommandFlatten(Command):

    def key(self):
        return 'flatten'

    def run_match(self, args, params):
        tree_k, tree_v = find_tree(params)
        result = {}
        if tree_k is not None:
            flat_tree_root = TreeNode()
            flat_tree_root.set_name('')
            flatten_tree(tree_v, flat_tree_root)
            flat_tree_root.sort_children()
            result = {
                tree_k+'-flat': flat_tree_root
            }
        return Match(result)


reg_cmd.register_command(CommandFlatten())
