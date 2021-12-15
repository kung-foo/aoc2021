#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt

src = open("input.txt", "r").readlines()

example = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]
d = len(src[0])

# m = 1  # part1
m = 5  # part2

G = nx.DiGraph()

for i in range(m):
    for j in range(m):
        for y, row in enumerate(src):
            for x, val in enumerate(row):
                v = (int(val) + i * d + j * d - 1) % 9 + 1  # wut
                c = (x + j * d, y + i * d)
                G.add_node(c, val=v)

d *= m

for y in range(d):
    for x in range(d):
        src = (x, y)
        if x < d - 1:
            dx = (x + 1, y)
            G.add_weighted_edges_from([(src, dx, G.nodes[dx]["val"])])
            G.add_weighted_edges_from([(dx, src, G.nodes[src]["val"])])
        if y < d - 1:
            dy = (x, y + 1)
            G.add_weighted_edges_from([(src, dy, G.nodes[dy]["val"])])
            G.add_weighted_edges_from([(dy, src, G.nodes[src]["val"])])

print(G)

p = nx.shortest_path(G, source=(0, 0), target=(d - 1, d - 1), weight="weight")

cost = 0
for i in range(len(p) - 1):
    cost += G.nodes[(p[i + 1])]["val"]

print("cost:", cost)
