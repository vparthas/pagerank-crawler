import numpy

def rank(matrix, indexes):
    vects = get_eigenvectors(matrix)
    assert(len(vects) != 0)

    equilibrium_vector = vects[0]
    comp_sum = equilibrium_vector.sum()
    for i in range(len(equilibrium_vector)):
        equilibrium_vector[i] /= comp_sum

    rank_map = {}
    for url, index in indexes.items():
        rank_map[url] = equilibrium_vector[index]

    return rank_map

def get_eigenvectors(matrix):
    eigvals, eigvects = numpy.linalg.eig(matrix)

    ret = []
    for i in range(len(eigvals)):
        if eigvals[i].imag != 0:
            continue
        val = eigvals[i].real
        if round(val, 10) == 1:
            ret.append(eigvects[i])

    for vector in ret:
        # remove trivial solutions
        if all(item == 0 for item in vector):
            ret.remove(vector)
        # remove scalar multiples
        # TODO

    return ret
