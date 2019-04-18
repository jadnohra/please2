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


def generic_match(cmd, str_args, str_args_low):
    params = cmd.parametrize(str_args, str_args_low)
    if params is None:
        return NoMatch()
    return cmd.run_match(params)

def generic_key_args(cmd):
    return cmd.key().lower().split()

def generic_parametrize(key_args, str_args, str_args_low):
    if key_args == str_args_low[:len(key_args)]:
        return {}
    return None
