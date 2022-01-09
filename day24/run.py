#!/usr/bin/env pypy3
import math
import random
import curses
import time
from datetime import datetime
import typing as t
from itertools import product

random.seed(5)

src = open("input.txt", "r").readlines()

low = (1,) * 14
high = (9,) * 14


# def b2i(b):
#     if b:
#         return 1
#     return 0
#
#
# def exact(w, z=0, p0=1, p1=12, p2=15):
#     x, y = 0, 0
#     x *= 0
#     x += z
#     x %= 26
#     z = math.floor(z / p0)
#     x += p1
#     x = b2i(x == w)
#     x = b2i(x == 0)
#     y *= 0
#     y += 25
#     y *= x
#     y += 1
#     z *= y
#     y *= 0
#     y += w
#     y += p2
#     y *= x
#     z += y
#     return z

"""
inp w       # w = input()
mul x 0     # x = 0
add x z     # x = z
mod x 26    # x = x mod 26
div z 1     # z = floor(z)
add x 12    # x += 12
eql x w     # x = (x == w)
eql x 0     # x = !x
mul y 0     # y = 0
add y 25    # y = 25
mul y x     # y = 25 * x
add y 1     # y+= 1
mul z y     # z = z * y
mul y 0     # y = 0
add y w     # y = w
add y 15    # y += 15
mul y x     # y = y * x 
add z y     # z += y
"""


# fully optimized and golfed partial func
# only option for further optimization would be to unroll the whole prog at once
def monad(p0, p1, p2):
    def func(w, z):
        x = (z % 26) + p1  # can be negative, last round is zero

        z = math.floor(z / p0)  # p0 is 1 or 26

        if x == w:
            return z

        return z * 26 + w + p2

    return func


src = [r.strip() for r in src if r.strip()]

plen = 18
assert len(src) % plen == 0

first = src[0:plen]

rounds = []

for i in range(int(len(src) / plen)):
    sp = src[i * plen : (i + 1) * plen]
    for j in range(plen):
        if j not in (4, 5, 15):  # these are the only line that are different
            assert first[j] == sp[j]

    p0 = int(sp[4].split(" ")[2])
    p1 = int(sp[5].split(" ")[2])
    p2 = int(sp[15].split(" ")[2])

    rounds.append(monad(p0, p1, p2))


# generates an exhaustive list of part numbers
def make_part_list_all(greater_than: t.Sequence[int], less_than: t.Sequence[int]):
    iterables = []

    for i in range(14):
        gt = greater_than[i]
        lt = less_than[i]
        iterables.append(range(gt, lt + 1))

    for part in product(*iterables):
        if part != greater_than:
            yield part


def make_part_list_rng(
    greater_than: t.Sequence[int],
    less_than: t.Sequence[int],
) -> t.List[int]:
    pn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    while True:
        for i in range(14):
            gt = greater_than[i]
            lt = less_than[i]
            # this is the key bit.
            # via manual inspection of solutions, I observed that for the "final" solution, every digit will be
            # greater than or equal to a previous solution. this allows a _signifigant_ reduction in space
            pn[i] = int(random.random() * (lt - gt + 1)) + gt
        if pn != greater_than:  # don't return our starting number accidentally
            return pn


def permutations_left(l):
    p = 1

    for c in l:
        p *= 9 - c + 1

    return p


def list_to_str(l):
    return "".join(str(c) for c in l)


def find_zero(stdscr, start: t.List[int]) -> t.Tuple[t.List[int], int]:
    c = 0
    mz = math.inf

    begin = datetime.now()

    def update_screen(count: int):
        exec_per_second = int(count / (datetime.now() - begin).total_seconds())
        stdscr.deleteln()
        stdscr.addstr(
            0,
            0,
            f"{list_to_str(start)} {list_to_str(model_number)} z={mz} eps={exec_per_second:,}/s",
        )
        stdscr.refresh()

    while True:
        c += 1
        model_number = make_part_list_rng(start, high)

        z = 0
        for i in range(14):
            z = rounds[i](model_number[i], z)

        if z < mz:
            mz = z
            update_screen(c)

        if c % 50_000 == 0:
            update_screen(c)

        if z == 0:
            return model_number, c


def part1(stdscr):
    stdscr.clear()

    start = low
    ct = 0
    zeros = []

    begin = datetime.now()

    def print_solutions():
        stdscr.clear()
        for i, z in enumerate(zeros):
            stdscr.addstr(f"z{i + 1}={list_to_str(z)} p={permutations_left(z):,}\n")
        stdscr.refresh()

    # first, look for solutions using brute force with rng
    while True:
        print_solutions()

        start, c = find_zero(stdscr, start)
        zeros.append(start)
        ct += c

        # if we are close to the end of the space, switch to exhaustive
        if permutations_left(start) < 10_000_000:
            break

    # exhaustively search remaining space
    while True:
        print_solutions()

        for model_number in make_part_list_all(start, high):
            z = 0
            for i in range(14):
                z = rounds[i](model_number[i], z)

            ct += 1

            if z == 0:
                zeros.append(model_number)
                start = model_number
                break
        else:
            # we made it through the for loop (for/else FTW!).
            stdscr.addstr(
                f"\nwoot! part1={list_to_str(zeros[-1])} time={int((datetime.now() - begin).total_seconds())}s prog_execs={ct:,}"
            )
            stdscr.refresh()
            time.sleep(3600)


def bench_rng():
    n = 10_000_000
    start = datetime.now()

    for _ in range(n):
        model_number = make_part_list_rng(low, high)

    print(f"rng: {int(n / (datetime.now() - start).total_seconds()):,}/s")


def bench_prog():
    n = 50_000_000
    start = datetime.now()

    model_number = make_part_list_rng(low, high)

    for _ in range(n):
        z = 0
        for i in range(14):
            z = rounds[i](model_number[i], z)

    print(f"prog: {int(n / (datetime.now() - start).total_seconds()):,}/s")


# bench_rng()
# bench_prog()
curses.wrapper(part1)


# targets = []
#
# for i in range(1, 10):
#     for z in range(10000000):
#         z2 = rounds[-1](i, z)
#         if z2 == 0:
#             print(i, z, z2)
#             targets.append([[i], [z]])
#             break
#
# for t in targets:
#     r = rounds[-2]
#     for i in range(1, 10):
#         for z in range(1000):
#             z2 = r(i, z)
#             if z2 == t[1][0]:
#                 print(t, i, z, z2)
