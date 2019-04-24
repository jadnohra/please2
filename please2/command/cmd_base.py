import please2.util.args as arg_util

class NoMatch:
    def is_match(self):
        return False

class Match:
    def __init__(self, result):
        self.result = result

    def is_match(self):
        return True

    def get_result(self):
        return self.result

class Args:
    def __init__(self, raw_args):
        self.args = raw_args
        self.args_low = [x.lower() for x in self.args]

    def asym_match_case_sensitive(self, other):
        # Note that this is an asymmetric match: the reference length is taken from others.args
        return other.args == self.args[:len(other.args)]

    def asym_match(self, other):
        # Note that this is an asymmetric match: the reference length is taken from others.args
        return other.args_low == self.args_low[:len(other.args)]

class Command:
    def help(self):
        return self.key()

    def opt_keys(self):
        return set(['@'])

    def match(self, args, prev_result):
        params = self.parametrize(args)
        if params is None:
            return NoMatch()
        params['prev_result'] = prev_result
        return self.run_match(params)

    def key_split(self):
        return Args(self.key().split())

    def parametrize(self, args):
        key_args = self.key_split()
        if args.asym_match(key_args):
            params = {}
            key_len = len(key_args.args)
            if  key_len < len(args.args):
                params = arg_util.parametrize_common(args.args[key_len:], self.opt_keys())
            return params
        return None
