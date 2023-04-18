import datetime
import json
import os
import timeit

import pyximport
from colorsys import hsv_to_rgb
from types import FunctionType
from typing import List

from statistics import fmean

import click
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.box import HEAVY_HEAD


pyximport.install()

from implementation import (
    python_re,
    python_native,
    python_np_mask,
    cython_generator,
    cython_class,
    cython_generator2,
    cython_generator3,
    cython_generator4,
)

content = "hello"


def base_runner():
    python_re.splitter(content)


def cython_class_runner():
    cython_class.splitter(content)


def cython_generator_runner():
    cython_generator.splitter(content)


def cython_generator2_runner():
    cython_generator2.splitter(content)


def cython_generator3_runner():
    cython_generator3.splitter(content)


def cython_generator4_runner():
    cython_generator4.splitter(content)


def python_np_mask_runner():
    python_np_mask.splitter(content)


def python_native_runner():
    python_native.splitter(content)


__benchmarks__ = {
    "Base": base_runner,
    "Cython class": cython_class_runner,
    "Cython generator": cython_generator_runner,
    "Cython generator 2": cython_generator2_runner,
    "Cython generator 3": cython_generator3_runner,
    "Cython generator 4": cython_generator4_runner,
    # "Python Numpy mask": python_np_mask_runner,
    # "Python native": python_native_runner,
}


def benchmark_function(func: FunctionType, repeats: int, times: int) -> List[float]:
    result = timeit.repeat(func, repeat=repeats, number=times)
    return result


def compute_style(hue: float) -> str:
    rgb = ",".join(
        str(int(component * 255)) for component in hsv_to_rgb(hue / 360, 0.94, 0.93)
    )
    return f"rgb({rgb})"


@click.command()
@click.option("--repeats", default=5, help="Number of times to repeat the content")
@click.option("--times", default=5, help="Number of times to run the script")
@click.option(
    "--content-type",
    type=click.Choice([fname.strip(".txt") for fname in os.listdir("./fixtures")]),
    default="lorem30",
)
def benchmark(repeats: int, times: int, content_type: str):
    global content
    with open(f"./fixtures/{content_type}.txt", "r") as fd:
        content = fd.read()

    results = {
        name: benchmark_function(function, repeats=repeats, times=times)
        for name, function in __benchmarks__.items()
    }

    df_stats = pd.DataFrame(
        [
            {
                "name": name,
                "min": min(timings),
                "mean": fmean(timings),
                "max": max(timings),
                "timings": json.dumps(timings),  # YOLO!
            }
            for name, timings in results.items()
        ]
    )
    df_stats.to_csv(
        f"./local/timings-{datetime.datetime.utcnow().isoformat()}.csv", index=False
    )

    for field in ["min", "max", "mean"]:
        df_stats[f"hue_{field}"] = (
            (df_stats[field].max() - df_stats[field])
            / (df_stats[field].max() - df_stats[field].min())
            * 150
        )
        df_stats[f"improvement_{field}"] = df_stats[field].max() / df_stats[field]

    table = Table(
        title=f"Benchmarks, repeat={repeats}, number={times}, content_type={content_type}",
        box=HEAVY_HEAD,
    )

    table.add_column("Benchmark", justify="right", style="cyan", no_wrap=True)
    table.add_column("Min", width=15)
    table.add_column("Max", width=15)
    table.add_column("Mean", width=15)

    for _, row in df_stats.iterrows():
        table.add_row(
            row["name"],
            Text(
                "{:.3f} ({:.2f}x)".format(row["min"], row["improvement_min"]),
                style=compute_style(row["hue_min"]),
            ),
            Text(
                "{:.3f} ({:.2f}x)".format(row["mean"], row["improvement_mean"]),
                style=compute_style(row["hue_mean"]),
            ),
            Text(
                "{:.3f} ({:.2f}x)".format(row["max"], row["improvement_max"]),
                style=compute_style(row["hue_max"]),
            ),
        )

    console = Console(width=300)
    console.print(table)


if __name__ == "__main__":
    benchmark()
