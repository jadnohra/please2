from os import getcwd
import subprocess

def _preprocess_run(args, params, run_args, run_kwargs={}):
    def _process_kwargs(params, run_kwargs):
        if 'cwd' not in run_kwargs:
            working_dir = params.get('@', getcwd())
            run_kwargs  = dict({'cwd': working_dir}, **run_kwargs)
        return run_kwargs
    trace = '[trace]' in args.args
    run_kwargs = _process_kwargs(params, run_kwargs)
    if trace:
        run_args_str = run_args if isinstance(run_args, str) else " ".join(run_args)
        print(f' TRACE: (cd {run_kwargs["cwd"]}; {run_args_str})')
    return run_kwargs

def run(args, params, run_args, run_kwargs={}, asnc=False):
    _preprocess_run(args, params, run_args, run_kwargs)
    if asnc:
        subprocess.Popen(run_args, **run_kwargs)
        return None
    else:
        result = subprocess.run(run_args, **run_kwargs)
        return result.returncode

def run_get_exitcode_stdout(args, params, run_args, run_kwargs={}, strip=True):
    _preprocess_run(args, params, run_args, run_kwargs)
    result = subprocess.run(run_args, stdout=subprocess.PIPE, **run_kwargs)
    result_stdout = result.stdout.decode('utf-8')
    return result.returncode, result_stdout.strip() if strip else result_stdout

def run_get_stdout(args, params, run_args, run_kwargs={}, strip=True):
    return run_get_exitcode_stdout(args, params, run_args, run_kwargs=run_kwargs, strip=strip)[1]

def run_get_exitcode_lines(args, params, run_args, run_kwargs={}, strip=True):
    exitcode, result_stdout = run_get_exitcode_stdout(args, params, run_args, run_kwargs=run_kwargs, strip=strip)
    result_lines = result_stdout.split('\n')
    if strip:
        result_lines = [x for x in result_lines if len(x.strip())]
    return exitcode, result_lines

def run_get_lines(args, params, run_args, run_kwargs={}, strip=True):
    return run_get_exitcode_lines(args, params, run_args, run_kwargs=run_kwargs, strip=strip)[1]
