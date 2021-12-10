#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
import math

src = open("input.txt", "r").readlines()

example = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".splitlines()

example2 = """
()
([])
{()()()}
<([{}])>
[<>({}){}[([])<>]]
""".splitlines()

example3 = """[(()[<>])]({[<{<<[]>>(""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

opn = ("[", "{", "(", "<")
cls = ("]", "}", ")", ">")
score = {"]": 57, "}": 1197, ")": 3, ">": 25137}
score2 = {"(": 1, "[": 2, "{": 3, "<": 4}

t = 0
incomplete = set(src)
for line in src:
    s = []
    for c in line:
        if c in opn:
            s.append(c)
        else:
            r = s.pop()
            if cls[opn.index(r)] != c:
                t += score[c]
                incomplete.remove(line)
                break

print("part1:", t)

scores = []
for line in incomplete:
    s = []
    for c in line:
        if c in opn:
            s.append(c)
        else:
            r = s.pop()
            if cls[opn.index(r)] != c:
                assert "wut"

    s.reverse()
    t = 0
    for c in s:
        t = t * 5 + score2[c]
    scores.append(t)

scores.sort()

print("part2:", scores[math.floor(len(scores) / 2)])
