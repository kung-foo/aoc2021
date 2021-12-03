#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
from collections import defaultdict

src = open("input.txt", "r").readlines()

example = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

g, e = "", ""
for i in range(len(src[0])):
    zc, oc = 0, 0
    for line in src:
        if line[i] == "0":
            zc += 1
        else:
            oc += 1

    if zc > oc:
        g += "0"
        e += "1"
    else:
        g += "1"
        e += "0"

g = int(g, 2)
e = int(e, 2)

print(g * e)

###

s = list(src)
for i in range(len(s[0])):
    zc, oc = 0, 0
    for line in s:
        if line[i] == "0":
            zc += 1
        else:
            oc += 1

    ns = []
    for line in s:
        if zc > oc:
            if line[i] == "0":
                ns.append(line)
        elif zc < oc:
            if line[i] == "1":
                ns.append(line)
        else:
            if line[i] == "1":
                ns.append(line)

    s = ns

    if len(s) == 1:
        break

og = int(s[0], 2)

###

s = list(src)
for i in range(len(s[0])):
    zc, oc = 0, 0
    for line in s:
        if line[i] == "0":
            zc += 1
        else:
            oc += 1

    ns = []
    for line in s:
        if zc > oc:
            if line[i] == "1":
                ns.append(line)
        elif zc < oc:
            if line[i] == "0":
                ns.append(line)
        else:
            if line[i] == "0":
                ns.append(line)
    s = ns

    if len(s) == 1:
        break

cs = int(s[0], 2)

print(og * cs)
