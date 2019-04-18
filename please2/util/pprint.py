from .tree import TreeNode

def pprint_tree_node(tree):
    def pprint_name(node):
        name = node.name()
        return name + ' <-----' if node.has_label('highlight') else name
    def recurse(node, depth=0):
        print(' '*depth*2, pprint_name(node))
        for child in node.children():
            recurse(child, depth+1)
    recurse(tree)

def pprint_any(obj):
    if isinstance(obj, TreeNode):
        pprint_tree_node(obj)
    else:
        print(obj)
