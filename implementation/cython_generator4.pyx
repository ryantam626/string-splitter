# cython: language_level=3

import string
import cython

cdef set non_word_boundaries = set(string.digits + string.ascii_letters + '_')


@cython.boundscheck(False)
@cython.wraparound(False)
def split_sentence(str sentence):
    cdef str word, c
    cdef int ind;

    start = -1
    ind = -1
    for c in sentence[:]:
        ind += 1
        if c not in non_word_boundaries:
            if start != -1:
                yield sentence[start:ind]
            yield sentence[ind]
            start = -1
        else:
            if start == -1:
                start = ind

    if start != -1:
        yield sentence[start:]


def splitter(sentence: str) -> list[str]:
    return list(split_sentence(sentence))
