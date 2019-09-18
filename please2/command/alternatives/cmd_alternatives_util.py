import json
from please2.util.run import run_get_stdout, run_get_lines

def run_alternatives_get_stdout(args, params, alt_args):
    run_args = ['update-alternatives']+alt_args
    return run_get_stdout(args, params, run_args)

def run_alternatives_get_lines(args, params, alt_args):
    run_args = ['update-alternatives']+alt_args
    return run_get_lines(args, params, run_args)

def make_error_result(args, params):
    result = {
        'error': 'Panic ;(',
    }
    return result

def get_all_alternatives(args, params):
    result_lines = run_alternatives_get_lines(args, params, ['--get-selections'])
    return [x.strip() for x in result_lines if len(x.strip())]
