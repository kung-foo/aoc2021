#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").readlines()

example = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

h = 0
d = 0

for line in src:
    direction, x = line.split(" ")
    x = int(x)

    if direction == "forward":
        h += x

    if direction == "down":
        d += x

    if direction == "up":
        d -= x

print(h * d)

h = 0
d = 0
a = 0

for line in src:
    direction, x = line.split(" ")
    x = int(x)

    if direction == "forward":
        h += x
        d += a * x

    if direction == "down":
        a += x

    if direction == "up":
        a -= x

print(h * d)
