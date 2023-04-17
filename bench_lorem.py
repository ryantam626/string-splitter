import os

import pyximport; pyximport.install()

from implementation import python_re, python_native, python_np_mask, cython_generator, cython_class


with open('./fixtures/lorem30.txt', 'r') as fd:
    content = fd.read()


def base_runner():
    for _ in range(int(os.environ.get("REPEATS", 20))):
        python_re.splitter(content)


def cython_class_runner():
    for _ in range(int(os.environ.get("REPEATS", 20))):
        cython_class.splitter(content)


def cython_generator_runner():
    for _ in range(int(os.environ.get("REPEATS", 20))):
        cython_generator.splitter(content)


def python_np_mask_runner():
    for _ in range(int(os.environ.get("REPEATS", 20))):
        python_np_mask.splitter(content)


def python_native_runner():
    for _ in range(int(os.environ.get("REPEATS", 20))):
        python_native.splitter(content)


__benchmarks__ = [
    (base_runner, cython_class_runner, "Cython class"),
    (base_runner, cython_generator_runner, "Cython generator"),
    (base_runner, python_np_mask_runner, "Python Numpy mask"),
    (base_runner, python_native_runner, "Python native"),
]
