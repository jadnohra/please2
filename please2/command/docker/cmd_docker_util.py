from please2.util.run import run_get_stdout, run_get_lines

def run_docker_get_stdout(args, params, git_args):
    run_args = ['docker']+git_args
    return run_get_stdout(args, params, run_args)

def run_docker_get_lines(args, params, git_args):
    run_args = ['docker']+git_args
    return run_get_lines(args, params, run_args)

def make_error_result(args, params):
    result = {
        'error': 'Panic ;(',
    }
    return result

def get_all_containers(args, params):
    result_lines = run_docker_get_lines(args, params, ['ps', '-aq'])
    return [x.strip() for x in result_lines if len(x.strip())]

def get_all_images(args, params):
    result_lines = run_docker_get_lines(args, params, ['images', '-q'])
    return [x.strip() for x in result_lines if len(x.strip())]
