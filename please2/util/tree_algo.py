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

def flatten_tree(node, flat_tree_root, node_path='',
                join_func=(lambda a,b: a + '/' + b if len(a) else b)):
    node_path = join_func(node_path, node.name())
    if node.is_leaf():
        flat_node = copy(node)
        flat_node.set_name(node_path)
        #if flat_node.has_label_layer():
        #    layer = flat_node.label_layer()
        #    layer.set_name(layer.name() + '-flat')
        flat_tree_root.add_child(flat_node)
    else:
        for child in node.children():
            flatten_tree(child, flat_tree_root, node_path)
