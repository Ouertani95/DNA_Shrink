import numpy

def bwt(original):
    string_array = numpy.fromstring(original, dtype = "uint8")
    n = len(string_array)
    offset_table = numpy.zeros((n, n), dtype = "uint8")
    for i in range(n):
        for j in range(n):
            offset_table[i][j] = string_array[(j + i) % n]
    suffix_array = numpy.lexsort(numpy.flip(offset_table, axis = 0))
    bwt_array = offset_table[suffix_array, -1]
    return suffix_array, bwt_array

def inverse_bwt(bwt_array):
    n = len(bwt_array)
    inverse_table = numpy.zeros((n, n), dtype = "uint8")
    for i in range(n):
        inverse_table[i] = bwt_array
        sort_indices = numpy.lexsort(inverse_table)
        inverse_table = inverse_table[:, sort_indices]
    for row in inverse_table.transpose():
        if row[0] == min(bwt_array):
            return numpy.flip(row).tostring().decode("utf-8")

