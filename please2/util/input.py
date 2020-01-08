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

def resolve_smart_input(input_str):
    if input_str == '[paste]':
        return clipboard.paste()
    if input_str.lower() == '[ask]':
        return input(' > ')
    else:
        return input_str
