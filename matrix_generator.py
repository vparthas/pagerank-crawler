import numpy


def generate_from_map(page_map):
    position_mappings = list(page_map.keys())
    dimension = len(position_mappings)
    matrix = numpy.zeros((dimension, dimension))

    for url, refs in page_map.items():
        curr_index = position_mappings.index(url)

        total = get_total(refs)
        if total == 0:
            matrix[curr_index][curr_index] = 1
            continue

        for ref, num in refs.items():
            index = position_mappings.index(ref)
            matrix[curr_index][index] = num / total

    return matrix


def get_total(refs):
    total = 0
    for num in refs.values():
        total += num
    return total