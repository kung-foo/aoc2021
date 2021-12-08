#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

src = open("input.txt", "r").readlines()

example = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".splitlines()

# example = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf".splitlines()

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

# src = example

src = [r.strip() for r in src if r.strip()]

dc = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]

#  0 is a subset of 8
# *1 is a subset of 0, 3, 4, 7, 8, 9 ^[2, 5, 6]
#  2 is a subset of 8
#  3 is a subset of 8, 9
# *4 is a subset of 8, 9
#  5 is a subset of 8, 9
#  6 is a subset of 8
# *7 is a subset of 0, 3, 8, 9 ^[1, 2, 4, 5, 6]
# *8 is a subset of
#  9 is a subset of 8

part1 = 0


def collapse(digits):
    # clean up where we only have a "new" single guess
    for v in digits.values():
        if len(v) == 1:
            for i, j in digits.items():
                if len(j) == 1:
                    continue
                j.difference_update(v)

    # cleanup where a digit has multiple guesses, but one of the guesses only appears once
    guesses = [0 for _ in range(10)]

    for d in digits.values():
        for v in d:
            guesses[v] += 1

    for gi, c in enumerate(guesses):
        if c > 1:
            continue

        for i, j in digits.items():
            if gi in j:
                j.difference_update(j.difference({gi}))

    return digits


def get_choices(digits, idx):
    choices = []

    for k, v in digits.items():
        if idx in v:
            choices.append(k)

    return choices


total = 0

for line in src:
    scram, outp = line.split(" | ")

    scram = [frozenset(x) for x in scram.split()]
    outp = [frozenset(x) for x in outp.split()]

    for d in outp:
        if len(d) in (2, 4, 3, 7):
            part1 += 1

    digits = {}
    rdigits = {}

    for d in scram:
        if len(d) == 2:
            digits[d] = {1}
            rdigits[1] = d
        elif len(d) == 4:
            digits[d] = {4}
            rdigits[4] = d
        elif len(d) == 3:
            digits[d] = {7}
            rdigits[7] = d
        elif len(d) == 7:
            digits[d] = {8}
            rdigits[8] = d
        elif len(d) == 6:
            digits[d] = {0, 6, 9}
        elif len(d) == 5:
            digits[d] = {2, 3, 5}
        else:
            assert "wut"

    for d in scram:
        if rdigits[1].issubset(d):
            digits[d].difference_update({2, 5, 6})

    four = rdigits[4]

    for c in get_choices(digits, 9):
        if four.issubset(c):
            digits[c] = {9}
            nine = c

    for c in get_choices(digits, 5):
        if c.issubset(nine):
            digits[c] = {5}

    digits = collapse(digits)

    c = ""
    for d in outp:
        c += str(list(digits[d])[0])

    total += int(c)

print("part1:", part1)
print("part1:", total)
