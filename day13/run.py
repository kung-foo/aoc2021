#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").readlines()

example = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]


def splity(a, y):
    return a[0:y], a[y + 1 :]


def splitx(a, x):
    return a[:, 0:x], a[:, x + 1 :]


mx, my = 0, 0
folds = []

for line in src:
    if "y=" in line or "x=" in line:
        folds.append(line.split(" ")[2])
    else:
        x, y = line.split(",")
        x = int(x)
        y = int(y)
        mx = max(mx, x)
        my = max(my, y)

paper = np.zeros((my + 1, mx + 1), dtype=int)

for line in src:
    if "," in line:
        x, y = line.split(",")
        paper[int(y)][int(x)] = 1


for i, fold in enumerate(folds):
    v = int(fold.split("=")[1])

    if fold[0] == "x":
        paper, fold = splitx(paper, v)
        fold = np.flip(fold, axis=1)

        if fold.shape > paper.shape:
            paper = np.pad(paper, ((0, 0), (abs(fold.shape[0] - paper.shape[0]), 0)))
        else:
            fold = np.pad(fold, ((0, 0), (abs(fold.shape[0] - paper.shape[0]), 0)))
    else:
        paper, fold = splity(paper, v)
        fold = np.flip(fold, axis=0)

        if fold.shape > paper.shape:
            paper = np.pad(paper, ((abs(fold.shape[0] - paper.shape[0]), 0), (0, 0)))
        else:
            fold = np.pad(fold, ((abs(fold.shape[0] - paper.shape[0]), 0), (0, 0)))

    paper |= fold

    if i == 0:
        print("part1:", np.sum(paper))


print("part2:")
for row in paper:
    r = ""
    for col in row:
        if col == 0:
            r += "  "
        else:
            r += "**"  # two stars for readability :)
    print(r)
