
def parametrize_common(args, opt_keys):
    opt_keys = set(opt_keys)
    params = {}
    for i,arg in enumerate(args):
        if arg in opt_keys and i+1<len(args):
            params[arg] = args[i+1]
    return params

def get_positional_at(args, index):
    return args[index]
    
def get_positional_after(args, key):
    return get_positional_at(args, args.index(key)+1)