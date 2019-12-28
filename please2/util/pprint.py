from .tree import TreeNode

def pprint_tree_node(tree, key=None, index_label_key=None):
    def pprint_name(node):
        postfix = ''
        if node.has_label_layer(key):
            lbl_join = ', '.join(node.label_layer(key).labels())
            postfix = ' <----- ' + lbl_join
        node_name = node.name()
        if isinstance(node_name, tuple):
            node_name = "{}: {}".format(node_name[0], node_name[1])
        return str(node_name) + postfix
    def recurse(node, depth=0, index_label_key=None):
        if index_label_key is not None and node.has_label_layer(index_label_key):
            print("{}.".format(node.label_value(index_label_key)), end = '')
        print(' '*depth*2, pprint_name(node))
        for child in node.children():
            recurse(child, depth+1, index_label_key=index_label_key)
    recurse(tree, index_label_key=index_label_key)

def pprint_any(obj, key=None):
    if isinstance(obj, TreeNode):
        pprint_tree_node(obj, key)
    else:
        print(obj)
