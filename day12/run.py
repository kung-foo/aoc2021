#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import typing as t

src = open("input.txt", "r").readlines()

example = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".splitlines()

example2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

G = nx.Graph()


def is_valid(p):
    for n, c in Counter(p).items():
        if c > 1 and not G.nodes[n]["big"]:
            return False

    return True


def is_valid_part2(p):
    twice = True

    for n, c in Counter(p).items():
        if c > 1:
            if n in ("start", "end"):
                return False

            if not G.nodes[n]["big"]:
                if c > 2 or not twice:
                    return False

                twice = False

    return True


for line in src:
    G.add_edge(*line.split("-"))

for name in G.nodes:
    G.nodes[name]["big"] = name == name.upper()


def explore(p: t.List[str], part: int) -> t.List[t.List[str]]:
    if part == 1:
        if not is_valid(p):
            return []

    if part == 2:
        if not is_valid_part2(p):
            return []

    if p[-1] == "end":
        return [p]

    paths = []

    for n in G[p[-1]]:
        cp = p.copy()
        cp.append(n)
        paths.extend(explore(cp, part))

    return paths


paths = explore(["start"], 1)
print("part1:", len(paths))

paths = explore(["start"], 2)
print("part2:", len(paths))

# nx.spring_layout(G)
# nx.draw(G, with_labels=True, font_weight="bold")
#
# plt.savefig("path.png")
