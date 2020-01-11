
def parametrize_common(args, opt_keys):
    opt_keys = set(opt_keys)
    params = {}
    for i,arg in enumerate(args):
        if arg in opt_keys and i+1<len(args):
            params[arg] = args[i+1]
    return params

def get_positional_at(args, index):
    return args[index] if index < len(args) else None

def get_positional_after(args, key):
    return get_positional_at(args, args.index(key)+1)

def get_positionals_after(args, key):
    if key in args:
        return args[args.index(key)+1:]
    else:
        return None
