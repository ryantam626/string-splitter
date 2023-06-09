# cython: language_level=3

import string

cdef set non_word_boundaries = set(string.digits + string.ascii_letters + '_')

def split_sentence(str sentence):
    cdef str word, c
    word = ''
    for c in sentence:
        if c in non_word_boundaries:
            word += c
        else:
            if word:  # to avoid adding empty strings
                yield word
                word = ''
            yield c
    if word:  # check if there is a word that we haven't added yet
        yield word


def splitter(sentence: str) -> list[str]:
    return list(split_sentence(sentence))
