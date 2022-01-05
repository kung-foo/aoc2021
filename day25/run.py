#!/usr/bin/env python3

import numpy as np
from scipy.signal import convolve2d

src = open("input.txt", "r").readlines()


cucumber_right = 1
cucumber_down = 4


def dump(h):
    m = {
        0: ".",
        cucumber_right: ">",
        cucumber_down: "v",
    }
    for row in h:
        for c in row:
            print(m[c], end="")
        print()
    print()


example = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".splitlines()

# src = example

src = [
    r.strip()
    .replace(".", "0")
    .replace(">", str(cucumber_right))
    .replace("v", str(cucumber_down))
    for r in src
    if r.strip()
]

herd = np.stack([np.array(list(line), dtype=int) for line in src])

conv_right = np.array(
    [
        [0, 0, 0],
        [-1, 1, 0],
        [0, 0, 0],
    ]
)

conv_down = np.array(
    [
        [0, -1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
)


def move(conv: np.array, cucumber: int, axis: int) -> bool:
    can_move = convolve2d(herd, conv, mode="same", boundary="wrap") == cucumber

    if np.sum(can_move) == 0:
        return False

    herd[can_move] = 0
    herd[np.roll(can_move, 1, axis=axis)] = cucumber

    return True


c = 0
while True:
    c += 1

    r = move(conv_right, cucumber_right, 1)
    d = move(conv_down, cucumber_down, 0)

    if not r and not d:
        break

print(c)
# dump(herd)
