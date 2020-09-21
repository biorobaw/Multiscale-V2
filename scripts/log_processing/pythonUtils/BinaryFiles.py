import numpy as np

# this file assumes data was encoded using little endian

def load_long_vector(file):
    file_is_str = type(file) is str
    if file_is_str:
        file = open(file, 'rb')
    length = read_vector_size(file)
    result = np.fromfile(file, dtype=np.int64, count=length)

    if file_is_str:
        file.close()
    return result

def load_int_vector(file):
    file_is_str = type(file) is str
    if file_is_str:
        file = open(file, 'rb')
    length = read_vector_size(file)
    result = np.fromfile(file, dtype=np.uint32, count=length)

    if file_is_str:
        file.close()
    return result

def load_float_vector(file):
    file_is_str = type(file) is str
    if file_is_str:
        file = open(file, 'rb')
    length = read_vector_size(file)
    result = np.fromfile(file, dtype=np.float32, count=length)

    if file_is_str:
        file.close()
    return result


def read_vector_size(file):
    file_is_str = type(file) is str
    if file_is_str:
        file = open(file, 'rb')
    result = np.fromfile(file, dtype=np.uint32, count=1)
    if file_is_str:
        file.close()
    return result.item()


def load_float_matrix(file):
    file_is_str = type(file) is str
    if file_is_str:
        file = open(file, 'rb')
    lengths = np.fromfile(file, dtype=np.uint32, count=2)
    total = lengths[0]*lengths[1]
    result = np.fromfile(file, dtype=np.float32, count=total).reshape((lengths[0], -1))
    if file_is_str:
        file.close()
    return result
