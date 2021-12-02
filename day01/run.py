#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").readlines()

example = """
199
200
208
210
200
207
240
269
260
263
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

c = 0
for i in range(len(src) - 1):
    if src[i] < src[i + 1]:
        c += 1

print(c)

c = 0
for i in range(len(src) - 3):
    a = sum(src[i : i + 3])
    b = sum(src[i + 1 : i + 4])

    if b > a:
        c += 1

print(c)
