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

    def match_case_sensitive(self, other):
        return other.args == self.args[:len(other.args)]

    def match(self, other):
        return other.args_low == self.args_low[:len(other.args)]

def generic_match(cmd, args):
    params = cmd.parametrize(args)
    if params is None:
        return NoMatch()
    return cmd.run_match(params)

def generic_key_args(cmd):
    return Args(cmd.key().split())
