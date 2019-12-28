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

def recurse_label_node_index(node, layer_name='index'):
    def label_node(node, index_container):
        layer = node.label_layer(layer_name)
        layer.set_value(index_container[0])
        index_container[0] = index_container[0] + 1
    def recurse_impl(node, index_container=[1]):
        label_node(node, index_container)
        for child in node.children():
            recurse_impl(child, index_container)
    recurse_impl(node)
