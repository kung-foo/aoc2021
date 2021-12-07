#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").read()

example = """16,1,2,0,4,2,7,1,2,14"""

# src = example

src = np.array(src.split(","), int)

r = {x: sum(abs(np.subtract(src, x))) for x in range(len(src))}
print("part1:", min(r.values()))

cost = [int(n * (n + 1) / 2) for n in range(max(src) + 1)]

fuel = sys.maxsize

for x in range(len(src)):
    t = abs(np.subtract(src, x))
    f = sum(np.take(cost, t))
    if f < fuel:
        fuel = f

print("part2:", fuel)
