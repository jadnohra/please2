
def parametrize_common(args):
    params = {}
    for i,arg in enumerate(args):
        if arg == '@' and i+1<len(args):
            params['@'] = args[i+1]
    return params
