import os
from .tree import TreeNode
from .tree_algo import flatten_tree

def get_prev_result(params, dflt={}):
    prev_result = params.get('prev_result', dflt)
    if prev_result is None:
        prev_result = dflt
    return prev_result

def find_tree(params):
    for k,v in get_prev_result(params).items():
        if isinstance(v, TreeNode):
            return k, v
    return (None, None)

def tree_to_list(tree, include_node_func=(lambda node: True)):
    if tree is None:
        return []
    path_root = tree.label_layer('root').value()
    if path_root is None:
        path_root = ''
    flat_tree = TreeNode('')
    flatten_tree(tree, flat_tree)
    items = [os.path.join(path_root, child.name()) for child in flat_tree.children() if include_node_func(child)]
    items = [x for x in items if len(x.strip())]
    return items

def find_tree_as_list(params):
    tree_k, tree_v = find_tree(params)
    if tree_k:
        return tree_to_list(tree_v)
    return None
