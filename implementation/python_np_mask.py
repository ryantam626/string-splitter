import string
import numpy as np

non_word_boundaries = string.ascii_letters + string.digits + "_"

np_non_word_boundaries = np.str_(non_word_boundaries)
np_non_word_boundaries_i32 = np_non_word_boundaries.reshape([1]).view(np.int32)


def _helper(sentence, mask):
    start = None

    for ind, current in enumerate(mask):
        if current:
            if start is not None:
                yield sentence[start:ind]
            yield sentence[ind]
            start = None
        else:
            if start is None:
                start = ind

    if start is not None:
        yield sentence[start:]


def splitter(sentence) -> list[str]:
    np_sentence = np.str_(sentence)
    np_sentence_i32 = np_sentence.reshape([1]).view(np.int32)
    return list(
        _helper(sentence, ~np.isin(np_sentence_i32, np_non_word_boundaries_i32))
    )
