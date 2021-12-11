#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
from scipy import signal

src = open("input.txt", "r").read()

example = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

example_step_1 = """
6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637
"""

example_step_2 = """
8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848
"""

example_step_10 = """
0481112976
0031112009
0041112504
0081111406
0099111306
0093511233
0442361130
5532252350
0532250600
0032240000
"""

example2 = """
11111
19991
19191
19991
11111
"""


def make_cave(s: str):
    lines = [r.strip() for r in s.splitlines() if r.strip()]
    return np.stack([np.array(list(l), dtype=int) for l in lines])


conv = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def step(cave):
    cave += 1

    can_flash = np.ones_like(cave)

    while True:
        full_powah = np.logical_and(np.where(cave > 9, 1, 0), can_flash)

        if np.sum(full_powah) == 0:
            return np.where(cave > 9, 0, cave), np.sum(can_flash == 0)

        can_flash[full_powah] = 0

        cave += signal.convolve2d(full_powah, conv, mode="same", fillvalue=0)


cave = make_cave(src)
total_flashed = 0

for i in range(1000):
    cave, flashed = step(cave)
    total_flashed += flashed

    if i + 1 == 100:
        print("part1:", total_flashed)

    if flashed == 100:
        print("part2:", i + 1)
        break
