from os import getcwd
import subprocess

def run(args, params, run_args):
    trace = '[trace]' in args.args
    working_dir = params.get('@', getcwd())
    if trace:
        print(f' > {working_dir}$ {" ".join(run_args)}')
    subprocess.run(run_args, cwd=working_dir)

def run_get_stdout(args, params, run_args, shell=False, run_kwargs={}):
    trace = '[trace]' in args.args
    working_dir = params.get('@', getcwd())
    if trace:
        print(f' > {working_dir}$ {" ".join(run_args)}')
    result = subprocess.run(run_args, stdout=subprocess.PIPE, cwd=working_dir, **run_kwargs)
    result_stdout = result.stdout.decode('utf-8')
    return result_stdout.strip()

def run_get_lines(args, params, run_args):
    result_stdout = run_get_stdout(args, params, run_args)
    result_lines = [x.strip() for x in result_stdout.split('\n') if len(x.strip())]
    return result_lines
