import numpy


def generate_from_map(page_map):
    dimension = len(page_map.items())
    matrix = numpy.zeros((dimension, dimension))

    indexes = {}
    i = 0
    for page in page_map.keys():
        indexes[page] = i
        i += 1

    for url, refs in page_map.items():
        curr_index = indexes[url]

        total = get_total(refs)
        if total == 0:
            for i in range(dimension):
                matrix[i][curr_index] = 1.0 / dimension
            continue

        for ref, num in refs.items():
            index = indexes[ref]
            matrix[index][curr_index] = num / total

    return matrix, indexes


def get_total(refs):
    total = 0
    for num in refs.values():
        total += num
    return total
