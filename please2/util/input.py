import clipboard

def input_indices(prompt):
    sel_str = input(prompt).strip()
    if len(sel_str) == 0:
        return []
    parts = sel_str.split(',')
    indices = []
    for part in parts:
        rng = part.split('-')
        if len(rng) == 1:
            indices.append(int(rng[0]))
        else:
            indices.extend(list(range(int(rng[0]), int(rng[1])+1)))
    return indices

def resolve_smart_input(input_str, prompt_str=' input: '):
    if input_str is None or (len(input_str.strip()) == 0) \
        or input_str.lower() == '[ask]':
        return input(prompt_str)
    elif input_str == '[paste]':
        return clipboard.paste()
    else:
        return input_str
