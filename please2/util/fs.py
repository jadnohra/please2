from os import listdir
from os.path import isfile, join, basename
from functools import reduce
from .tree import TreeNode

def dir_tree(root_dir, dirs_only=False, dir_filter_func=lambda x: True,
        file_filter_func=lambda x: True):
    def recurse(dir, dirname):
        node = TreeNode()
        node.set_name(dirname)
        node.set_label('d')
        fs_nodes = listdir(dir)
        for node_name in fs_nodes:
                node_path = join(dir, node_name)
                if isfile(node_path):
                    if file_filter_func(node_name):
                        fnode = TreeNode()
                        fnode.set_name(node_name)
                        fnode.set_label('f')
                        node.add_child(fnode)
                else:
                    if dir_filter_func(node_name):
                        node.add_child(recurse(node_path, node_name))
        return node
    root_tree = recurse(root_dir, basename(root_dir))
    root_tree.set_attr('root', root_dir)
    return root_tree
