#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").readlines()

example = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".splitlines()

# src = example
# src = "1,1 -> 3,3".splitlines()

src = [r.strip() for r in src if r.strip()]


def step_size(c1, c2):
    if c1 > c2:
        return -1
    if c1 < c2:
        return 1
    return 0


def points(s1, s2):
    p = s1.copy()

    sx = step_size(s1[0], s2[0])
    sy = step_size(s1[1], s2[1])

    while True:
        yield p[0], p[1]

        if p == s2:
            break

        p[0] += sx
        p[1] += sy


segments = []

for line in src:
    x1, y1, x2, y2 = map(int, line.replace(" -> ", ",").split(","))
    segments.append([[x1, y1], [x2, y2]])

sq_segments = list(filter(lambda s: s[0][0] == s[1][0] or s[0][1] == s[1][1], segments))


def run(segments):
    sea_floor = {}

    for s in segments:
        for p in points(s[0], s[1]):
            if p not in sea_floor:
                sea_floor[p] = 0
            sea_floor[p] += 1

    cnt = 0
    for _, v in sea_floor.items():
        if v >= 2:
            cnt += 1

    return cnt


print(f"part1: {run(sq_segments)}")
print(f"part2: {run(segments)}")
