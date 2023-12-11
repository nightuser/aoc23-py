#!/usr/bin/env python3
import itertools
import sys

ans1 = 0
ans2 = 0

fname = sys.argv[1]
with open(fname) as fh:
    for line in fh:
        line = line.rstrip()
        xs = list(map(int, line.split()))
        first: list[int] = []
        last: list[int] = []
        while not all(x == 0 for x in xs):
            first.append(xs[0])
            last.append(xs[-1])
            xs = [x2 - x1 for x1, x2 in itertools.pairwise(xs)]
        new_last = sum(last)
        ans1 += new_last
        print(first)
        new_first = 0
        for x in reversed(first):
            new_first = x - new_first
        ans2 += new_first

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
