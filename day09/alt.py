#!/usr/bin/env python3
import sys

ans1 = 0
ans2 = 0

fname = sys.argv[1]
with open(fname) as fh:
    for line in fh:
        line = line.rstrip()
        xs = list(map(int, line.split()))
        n = len(xs)

        new_last = 0
        new_first = 0
        sign = 1
        coeff1 = 1
        coeff2 = n
        for j, x in enumerate(xs, start=1):
            new_last += x * sign * coeff1
            new_first += x * sign * coeff2
            sign *= -1
            coeff1 = coeff2
            coeff2 = (coeff2 * (n - j)) // (j + 1)
        if n % 2 == 0:
            new_last *= -1

        ans1 += new_last
        ans2 += new_first


print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
