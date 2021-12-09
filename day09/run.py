#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
from scipy import signal
from skimage.segmentation import flood_fill

src = open("input.txt", "r").readlines()

example = """
2199943210
3987894922
9856789892
8767896789
9899965678
""".splitlines()

# src = example

src = [[int(h) for h in r.strip()] for r in src if r.strip()]

a = np.array(src)

c = np.array([[0, -1, 0], [0, 1, 0], [0, 0, 0]])

m = np.ones(a.shape)

for _ in range(4):
    x = signal.convolve2d(src, c, mode="same", fillvalue=10)
    m = np.logical_and(m, (x < 0))
    c = np.rot90(c)

print("part1:", sum(a[m] + 1))

m = np.where(m, a, -1)
row, col = np.where(m >= 0)

nines = np.where(a != 9, 0, a)

basins = []

for i in range(len(row)):
    ff = flood_fill(nines, (row[i], col[i]), 42, connectivity=1)
    basins.append(len(np.where(ff == 42)[0]))

basins.sort()

print("part2", np.prod(basins[-3:]))
