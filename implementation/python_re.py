import re

split_pattern = re.compile(r"([^a-zA-Z\d])")


def splitter(sentence: str) -> list[str]:
    return list(filter(None, split_pattern.split(sentence)))
