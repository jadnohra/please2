import sys
import please2.all_commands  # noqa
import please2.reg_cmd as reg_cmd
from please2.command.cmd_base import Args, NoMatch, Match
from please2.util.pprint import pprint_any
import pprint

def process(args):
    for cmd in reg_cmd.all_commands():
        out = cmd.match(args)
        if out.is_match():
            return out.get_result();
    return "Apologies, I don't know this command"

def pprint_match(result):
    if isinstance(result, dict) and len(result) == 1:
        for v in result.values():
            pprint_any(v)
        return
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)


def main():
    args = Args(sys.argv[1:])
    test_result = process(args)
    pprint_match(test_result)
