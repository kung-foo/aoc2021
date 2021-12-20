#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
from scipy import signal

src = open("input.txt", "r").readlines()

example = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

algo = np.array([0 if c == "." else 1 for c in list(src.pop(0))], dtype=int)
assert len(algo) == 512

flicker = algo[0] == 1


p = np.ndarray(shape=(len(src), len(src)), dtype=int)

for i, row in enumerate(src):
    for j, px in enumerate(row):
        p[i][j] = 1 if px == "#" else 0

pad_width = 3

c = np.array(
    [
        [1 << 0, 1 << 1, 1 << 2],
        [1 << 3, 1 << 4, 1 << 5],
        [1 << 6, 1 << 7, 1 << 8],
    ]
)

for s in range(50):
    fillvalue = 0 if not flicker or s % 2 == 0 else 1
    p = np.pad(p, pad_width=pad_width, constant_values=fillvalue)
    p = algo[signal.convolve2d(p, c, mode="same", fillvalue=fillvalue)]
    if s == 1:
        print("part1:", np.sum(p))

print("part2:", np.sum(p))
