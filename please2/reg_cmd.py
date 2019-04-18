_g_cmd_reg = set()


def register_command(cmd):
    global _g_cmd_reg
    _g_cmd_reg.add(cmd)


def all_commands():
    return _g_cmd_reg;
