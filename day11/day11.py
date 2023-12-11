import functools
import itertools
import sys
from typing import TypeVar

T = TypeVar("T")
Point = tuple[int, int]


def prefix_sums(xs: list[int], expansion: int) -> dict[int, int]:
    xs_iter = iter(xs)
    result: list[tuple[int, int]] = [(next(xs_iter), 1)]
    for x in xs_iter:
        prev_x, prev_sum = result[-1]
        spacing = x - prev_x - 1
        result.append((x, prev_sum + expansion * spacing + 1))
    return dict(result)


def dist(
    rows_sums: dict[int, int], cols_sums: dict[int, int], p: Point, q: Point
) -> int:
    return abs(cols_sums[p[0]] - cols_sums[q[0]]) + abs(
        rows_sums[p[1]] - rows_sums[q[1]]
    )


galaxies: list[Point] = []
cols_set: set[int] = set()
rows_set: set[int] = set()
fname = sys.argv[1]
with open(fname) as fh:
    for y, line in enumerate(fh, start=1):
        line = line.rstrip()
        for x, p in enumerate(line, start=1):
            if p == "#":
                galaxies.append((x, y))
                rows_set.add(y)
                cols_set.add(x)

rows = list(sorted(rows_set))
cols = list(sorted(cols_set))

rows_sums1 = prefix_sums(rows, 2)
cols_sums1 = prefix_sums(cols, 2)
dist1 = functools.partial(dist, rows_sums1, cols_sums1)
rows_sums2 = prefix_sums(rows, 1000000)
cols_sums2 = prefix_sums(cols, 1000000)
dist2 = functools.partial(dist, rows_sums2, cols_sums2)

ans1 = 0
ans2 = 0
for g1, g2 in itertools.combinations(galaxies, 2):
    ans1 += dist1(g1, g2)
    ans2 += dist2(g1, g2)

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
