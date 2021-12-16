#!/usr/bin/env python3

import bitstruct
import numpy as np
from bitstruct import *

src = open("input.txt", "r").read()

example = "D2FE28"
example = "38006F45291200"
example = "A0016C880162017C3686B18A3D4780"
example = "9C0141080250320F1802104A08"

# src = example

buf = bytearray.fromhex(src)

literal = 4


# def pad(o):
#     return 8 - o % 8


offset = 0


def unpack(fmt):
    global offset, buf
    vals = bitstruct.unpack_from(fmt, buf, offset=offset)
    offset += bitstruct.calcsize(fmt)
    if len(vals) == 1:
        return vals[0]
    return vals


ver_sum = 0


def read_packet():
    global offset, ver_sum

    v, t = unpack("u3u3")
    ver_sum += v

    if t == literal:
        sv = ""
        while True:
            c, v = unpack("u1u4")
            sv += f"{v:x}"

            if c == 0:
                break

        return int(sv, 16)
    else:
        length_type = unpack("u1")

        results = []

        if length_type == 0:
            sub_packet_length = unpack("u15")
            current_offset = offset
            while offset < current_offset + sub_packet_length:
                results.append(read_packet())

        if length_type == 1:
            for _ in range(unpack("u11")):
                results.append(read_packet())

        if t == 0:
            return np.sum(results)
        if t == 1:
            return np.product(results)
        if t == 2:
            return np.min(results)
        if t == 3:
            return np.max(results)

        assert len(results) == 2

        if t == 5:
            return 1 if results[0] > results[1] else 0
        if t == 6:
            return 1 if results[0] < results[1] else 0
        if t == 7:
            return 1 if results[0] == results[1] else 0


v = read_packet()

print("part1:", ver_sum)
print("part2:", v)
