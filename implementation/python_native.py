import re
import string
from typing import Iterator

split_pattern = re.compile(r'([^a-zA-Z\d])')
non_word_boundaries = set(string.digits + string.ascii_letters + '_')


def _helper(sentence: str) -> Iterator[str]:
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
    return list(_helper(sentence))
