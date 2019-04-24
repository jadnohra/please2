import sys
import please2.all_commands  # noqa
import please2.reg_cmd as reg_cmd
from please2.command.cmd_base import Args, NoMatch, Match
from please2.util.pprint import pprint_any
import pprint


def process(args, prev_result=None):
    for cmd in reg_cmd.all_commands():
        out = cmd.match(args, prev_result)
        if out.is_match():
            return out.get_result()
    return "Apologies, I don't know this command"


def pprint_match(result):
    if isinstance(result, dict) and len(result) == 1:
        for v in result.values():
            pprint_any(v)
        return
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)


def split_into_cmd_chains(argv, chain_sep='---'):
    split_indices = [i for i in range(len(argv)) if argv[i] == '---']
    chains = []
    split_start = 0
    for split_i in split_indices:
        chains.append(argv[split_start: split_i])
        split_start = split_i + 1
    if split_start < len(argv):
        chains.append(argv[split_start:])
    return chains


def main():
    chains = split_into_cmd_chains(sys.argv[1:])
    last_result = None
    for chain in chains:
        args = Args(chain)
        last_result = process(args, last_result)
        pprint_match(last_result)
