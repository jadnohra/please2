import please2.all_commands  # noqa
import please2.reg_cmd as reg_cmd


def process(string):
    for cmd in reg_cmd.all_commands():
        out = cmd.match(string)
        if out.is_match():
            return out.get_result()
    return None


def main():
    test_result = process('which OS')
    print(test_result)
