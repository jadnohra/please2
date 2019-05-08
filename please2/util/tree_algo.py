from copy import copy

def recurse_filter_node_copy(node, keep_node_func):
    filtered_children = [recurse_filter_node_copy(x, keep_node_func) for x in node.children()]
    filtered_children = [x for x in filtered_children if x is not None]
    keep_self = keep_node_func(node)
    if keep_self or filtered_children:
        filtered_node = copy(node)
        filtered_node.set_children(filtered_children)
        return filtered_node
    else:
        return None
