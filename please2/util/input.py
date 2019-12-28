def input_indices(prompt):
    sel_str = input(prompt).strip()
    parts = sel_str.split(',')
    indices = []
    for part in parts:
        rng = part.split('-')
        if len(rng) == 1:
            indices.append(int(rng[0]))
        else:
            indices.extend(list(range(int(rng[0]), int(rng[1])+1)))
    return indices
