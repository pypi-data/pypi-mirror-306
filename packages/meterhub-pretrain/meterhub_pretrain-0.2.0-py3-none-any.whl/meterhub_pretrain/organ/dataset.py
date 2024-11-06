import pathlib
import typing as t

import numpy as np
from PIL import Image
from tqdm import tqdm


def output_func():
    i = 1

    def output_once(name):
        nonlocal i
        if i == 1:
            print(name)
        i = 0

    return output_once


output_once = output_func()


def iter_gen_image(
    get_x_y: t.Callable,
    stage: t.Literal["train", "valid"],
    get_output: t.Callable,
):
    is_write, labels_file, output_folder = get_output()
    labels_file.parent.mkdir(parents=True, exist_ok=True)

    f = open(labels_file, "w")
    x, y = get_x_y()
    for i in tqdm(range(x.shape[0]), desc=f"Processing {stage} data"):
        im = Image.fromarray(x[i])
        filename = str(i).zfill(6)  # max length is 6
        filename_in_label = pathlib.Path("rec") / stage.lower() / f"{filename}.png"
        output_once(filename_in_label)

        def write_file():
            filepath = output_folder / filename_in_label
            im.save(filepath)

        if is_write:
            write_file()

        # ignore same label-clustering rule, just append to list
        f.write(f"{filename_in_label}\t{y[i][0]}\n")

    f.close()
