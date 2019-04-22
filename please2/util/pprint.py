from .tree import TreeNode

def pprint_tree_node(tree):
    def pprint_name(node):
        name = str(node.name())
        if node.has_attr('pprint-highlight'):
            return name + ' <----- ' + str(node.get_attr('pprint-highlight', '?'))
        elif node.has_label('pprint-highlight'):
            return name + ' <-----'
        else:
            return name
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
