#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

ROWS: int = 200
COLUMNS: int = 100
ITEM_WIDTH: int = 28
ITEM_HEIGHT: int = 28
SRC_DIR: str = "mnist_png/training"


def process(img: Image) -> Image:
    # https://stackoverflow.com/a/54148416/10477326
    x = np.asarray(img.convert('RGBA')).copy()
    x[:, :, 3] = (255 * (x[:, :, :3] != 0).any(axis=2)).astype(np.uint8)
    return Image.fromarray(x)


def worker():
    # https://stackoverflow.com/a/30228308/10477326
    page = 0
    while True:
        x = 0
        y = 0
        buf = Image.new('RGBA', (COLUMNS * ITEM_WIDTH, ROWS * ITEM_HEIGHT))
        try:
            while True:
                path = yield
                img = Image.open(path)
                img = process(img)
                buf.paste(img, (x * ITEM_WIDTH, y * ITEM_HEIGHT))
                x += 1
                if x == COLUMNS:
                    x = 0
                    y += 1
                if y == ROWS:
                    break
                print(f"{page} {x} {y}")
        finally:
            if x or y:
                buf.save(f"atlas/{page}.png")
                page += 1


def main() -> None:
    gen = worker()
    next(gen)
    for digit in range(0, 10):
        for filename in sorted(os.listdir(f"{SRC_DIR}/{digit}")):
            gen.send(f"{SRC_DIR}/{digit}/{filename}")
    gen.close()


if __name__ == "__main__":
    main()
