from .tree import TreeNode

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
