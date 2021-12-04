#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").readlines()

example = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

nums = list(map(int, src.pop(0).split(",")))

assert len(src) % 5 == 0

boards = []
matches = []

for i in range(int(len(src) / 5)):
    matches.append(np.zeros((5, 5), dtype=bool))
    rows = []
    for j in range(5):
        row = list(map(int, src[i * 5 + j].split()))
        rows.append(np.array(row))
    boards.append(np.asarray(rows, dtype=int))

winners = set()

for n in nums:
    for i, b in enumerate(boards):
        x, y = np.where(b == n)
        if x.size == 0 or y.size == 0:
            continue
        assert x.size == 1 and y.size == 1
        matches[i].itemset((x[0], y[0]), True)
        boards[i].itemset((x[0], y[0]), -1)

    for i, m in enumerate(matches):
        if i not in winners:
            for r in range(5):
                if m[r, :].all() or m[:, r].all():
                    winners.add(i)
                    if len(winners) == 1:
                        print("part1", i, n * np.sum(boards[i][boards[i] >= 0]))
                    if len(winners) == len(boards):
                        print("part2", i, n * np.sum(boards[i][boards[i] >= 0]))
                    break
