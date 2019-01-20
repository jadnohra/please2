import platform


class NoMatch:
    def did_match(self):
        return False


class Match:
    def __init__(self, result):
        self.result = result

    def did_match():
        return True

    def get_result(self):
        return self.result


def generic_match(cmd, string):
    params = cmd.parametrize(string)
    if params is None:
        return NoMatch()
    return cmd.run_match(params)


class CommandWhichOS:

    def match(self, string):
        return generic_match(self, string)

    def parametrize(self, string):
        if string.lower().startswith('which OS'.lower()):
            return {}
        return None

    def run_match(self, params):
        return Match({
            'OS': platform.system(),
            'release': platform.release()
            })
        # https://stackoverflow.com/questions/2756737/check-linux-distribution-name


test = CommandWhichOS()
print(test.match('which OS').get_result())
