import sys
import please2.all_commands  # noqa
import please2.reg_cmd as reg_cmd


def process(str_args, str_args_low):
    for cmd in reg_cmd.all_commands():
        out = cmd.match(str_args, str_args_low)
        if out.is_match():
            return out.get_result();
    return None


def main():
    str_args = sys.argv[1:]
    str_args_low = [x.lower() for x in str_args]
    test_result = process(str_args, str_args_low)
    print(test_result)
