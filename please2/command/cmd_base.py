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


def generic_match(cmd, string):
    params = cmd.parametrize(string)
    if params is None:
        return NoMatch()
    return cmd.run_match(params)
