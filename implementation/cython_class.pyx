# cython: language_level=3

import string

cdef set non_word_boundaries = set(string.digits + string.ascii_letters + '_')


cdef class SplitSentence:
    cdef readonly str sentence
    cdef readonly str word
    cdef readonly str c
    cdef readonly int idx

    def __cinit__(SplitSentence self, str sentence):
        self.sentence = sentence
        self.idx = -1
        self.word = ''
        self.c = None

    def __iter__(SplitSentence self):
        return self

    def __next__(SplitSentence self):
        cdef str c, word

        c = self.c
        if c:
            self.c = None
            return c

        while self.idx + 1 < len(self.sentence):
            self.idx += 1
            c = self.sentence[self.idx]
            if c in non_word_boundaries:
                self.word += c
            else:
                word = self.word
                if word:
                    self.word = ''
                    self.c = c
                    return word
                else:
                    return c

        word = self.word
        if word:
            self.word = ''
            return word
        raise StopIteration


def splitter(sentence: str) -> list[str]:
    return list(SplitSentence(sentence))
