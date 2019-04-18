import sys
import please2.all_commands  # noqa
import please2.reg_cmd as reg_cmd
from please2.command.cmd_base import Args


def process(args):
    for cmd in reg_cmd.all_commands():
        out = cmd.match(args)
        if out.is_match():
            return out.get_result();
    return "Apologies, I don't know this command"


def main():
    args = Args(sys.argv[1:])
    test_result = process(args)
    print(test_result)
