from os import listdir
from os.path import isfile, isdir, join, basename
from functools import reduce
from .tree import TreeNode

def dir_tree(root_dir, dirs_only=False, dir_filter_func=lambda x: True,
        file_filter_func=lambda x: True):
    layer_key = 'dir_tree'
    def recurse(dir, dirname):
        node = TreeNode()
        node.set_name(dirname)
        layer = node.label_layer(layer_key).set_value('d')
        fs_nodes = listdir(dir)
        for node_name in fs_nodes:
                node_path = join(dir, node_name)
                if isfile(node_path):
                    if file_filter_func(node_name):
                        fnode = TreeNode()
                        fnode.set_name(node_name)
                        layer = fnode.label_layer(layer_key)
                        layer.set_label('f')
                        node.add_child(fnode)
                elif isdir(node_path):
                    if dir_filter_func(node_name):
                        node.add_child(recurse(node_path, node_name))
        return node
    root_tree = recurse(root_dir, '.')
    root_tree.label_layer('root').set_value(root_dir)
    return root_tree
