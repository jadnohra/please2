from .tree import TreeNode

def pprint_tree_node(tree, key=None):
    def pprint_name(node):
        postfix = ''
        if node.is_label_layer(key):
            lbl_join = ', '.join(node.labels())
            postfix = ' <----- ' + lbl_join
        return str(node.name()) + postfix
    def recurse(node, depth=0):
        print(' '*depth*2, pprint_name(node))
        for child in node.children():
            recurse(child, depth+1)
    recurse(tree)

def pprint_any(obj, key=None):
    if isinstance(obj, TreeNode):
        pprint_tree_node(obj, key)
    else:
        print(obj)
