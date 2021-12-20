#!/usr/bin/env python3

import os
import sys
import random
from itertools import permutations
from math import floor, ceil
import attr

src = open("input.txt", "r").readlines()

example = """
[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]
""".splitlines()


@attr.s(eq=False)
class Snail:
    x = attr.ib(default=None)
    y = attr.ib(default=None)
    p = attr.ib(default=None)

    def is_number(self):
        return isinstance(self.x, int) and isinstance(self.y, int)

    def is_dead(self):
        return self.is_number() and self.x == -1 and self.y == -1

    @classmethod
    def load(cls, n, p=None):
        if isinstance(n, str):
            n = eval(n)
        assert len(n) == 2

        s = cls(p=p)

        if isinstance(n[0], int):
            s.x = n[0]
        else:
            s.x = Snail.load(n[0], s)

        if isinstance(n[1], int):
            s.y = n[1]
        else:
            s.y = Snail.load(n[1], s)

        return s

    def adj_right(self) -> "Snail":
        if not self.p:
            return None

        s = self

        while s.p.y == s:  # ascend
            s = s.p
            if s.p is None:
                return None

        s = s.p

        if isinstance(s.y, int):
            return s

        s = s.y
        while isinstance(s.x, Snail):  # descend
            s = s.x

        return s

    def adj_left(self) -> "Snail":
        if not self.p:
            return None

        s = self

        while s.p.x == s:  # ascend
            s = s.p
            if s.p is None:
                return None

        s = s.p

        if isinstance(s.x, int):
            return s

        s = s.x
        while isinstance(s.y, Snail):  # descend
            s = s.y

        return s

    def gc(self):
        if isinstance(self.x, Snail) and self.x.is_dead():
            self.x = 0
        if isinstance(self.y, Snail) and self.y.is_dead():
            self.y = 0

    def depth(self):
        if not self.p:
            return 1
        return 1 + self.p.depth()

    def magnitude(self) -> int:
        m = 0

        if isinstance(self.x, int):
            m += self.x * 3
        else:
            m += self.x.magnitude() * 3

        if isinstance(self.y, int):
            m += self.y * 2
        else:
            m += self.y.magnitude() * 2

        return m

    def __add__(self, other_snail):
        assert isinstance(other_snail, Snail)
        s = Snail(x=self, y=other_snail)
        self.p = s
        other_snail.p = s
        return s

    def __str__(self):
        return f"[{self.x},{self.y}]"


def walk(root, func):
    if isinstance(root.x, Snail):
        if walk(root.x, func):
            return True
    else:
        if func(root):
            return True

    if isinstance(root.y, Snail):
        if walk(root.y, func):
            return True
    else:
        if func(root):
            return True

    return func(root)


def split(s: Snail):
    if isinstance(s.x, int) and s.x >= 10:
        x = s.x
        s.x = Snail(x=floor(x / 2), y=ceil(x / 2), p=s)
        return True

    if isinstance(s.y, int) and s.y >= 10:
        y = s.y
        s.y = Snail(x=floor(y / 2), y=ceil(y / 2), p=s)
        return True

    return False


def explode(s: Snail):
    if not isinstance(s, Snail):
        return False

    if s.depth() < 5:
        return False

    r = s.adj_right()
    if r:
        if isinstance(r.x, int):
            r.x += s.y
        else:
            r.y += s.y

    l = s.adj_left()
    if l:
        if isinstance(l.y, int):
            l.y += s.x
        else:
            l.x += s.x

    s.x = -1
    s.y = -1

    s.p.gc()

    return True


s1 = Snail.load([1, 2])
s2 = Snail.load([[3, 4], 5])

assert str(s1 + s2) == "[[1,2],[[3,4],5]]"

s1 = Snail.load("[[[[[9,8],1],2],3],4]")
walk(s1, explode)
assert str(s1) == "[[[[0,9],2],3],4]", s1

s2 = Snail.load("[7,[6,[5,[4,[3,2]]]]]")
walk(s2, explode)
assert str(s2) == "[7,[6,[5,[7,0]]]]", s2

s3 = Snail.load("[[6,[5,[4,[3,2]]]],1]")
walk(s3, explode)
assert str(s3) == "[[6,[5,[7,0]]],3]", s3

s4 = Snail.load("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
walk(s4, explode)
assert str(s4) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", s4

s5 = Snail.load(str(s4))
walk(s5, explode)
assert str(s5) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"

s7 = Snail.load("[0, 11]")
walk(s7, split)
assert str(s7) == "[0,[5,6]]"

s6 = Snail.load("[[[[4,3],4],4],[7,[[8,4],9]]]") + Snail.load("[1,1]")
assert str(s6) == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", s6

print(walk(s6, explode))
assert str(s6) == "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", s6

print(walk(s6, explode))
assert str(s6) == "[[[[0,7],4],[15,[0,13]]],[1,1]]", s6

print(walk(s6, split))
assert str(s6) == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", s6

print(walk(s6, split))
assert str(s6) == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", s6

print(walk(s6, explode))
assert str(s6) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", s6

assert Snail.load("[9,1]").magnitude() == 29

assert (
    Snail.load("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude()
    == 3488
)


def reduce(s: Snail):
    while True:
        if walk(s, explode):
            continue

        if walk(s, split):
            continue

        break
    return s


def solve(problem):
    cs = Snail.load(problem[0])

    for i in range(1, len(problem)):
        cs += Snail.load(problem[i])
        reduce(cs)

    return cs, cs.magnitude()


p1 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]""".splitlines()

s, m = solve(p1)
assert str(s) == "[[[[5,0],[7,4]],[5,5]],[6,6]]", s

p2 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".splitlines()

s, m = solve(p2)
assert str(s) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", s

p3 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".splitlines()

s, m = solve(p3)
assert m == 4140

s, m = solve(src)
print("part1:", m)

mm = 0

for pair in permutations(src, r=2):
    _, m = solve(pair)
    mm = max(mm, m)

print("part2:", mm)
