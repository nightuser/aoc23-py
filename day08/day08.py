import math
import re
import sys


def parse_node_name(pos: str) -> int:
    code = 0
    assert pos.isupper()
    assert len(pos) == 3
    for c in pos:
        code = 26 * code + (ord(c) - ord("A"))
    return code


def is_source(code: int) -> bool:
    return code % 26 == 0


def is_target(code: int) -> bool:
    return code % 26 == 25


def find_period(
    rules: dict[int, tuple[int, int]],
    directions: str,
    source: int,
) -> tuple[int, int]:
    period = 0
    dir = 0
    current = source
    while True:
        period += 1
        left, right = rules[current]
        current = left if directions[dir] == "L" else right
        dir += 1
        if dir == len(directions):
            dir = 0
        if is_target(current):
            assert dir == 0
            break

    return current, period


line_re = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")

rules: dict[int, tuple[int, int]] = dict()
sources: list[int] = []

fname = sys.argv[1]
with open(fname) as fh:
    directions = fh.readline().rstrip()
    fh.readline()
    for line in fh:
        line = line.rstrip()
        m = line_re.match(line)
        assert m
        pos, left, right = map(parse_node_name, m.groups())
        rules[pos] = (left, right)
        if is_source(pos):
            sources.append(pos)

ans1 = None
xs: list[int] = []

for source in sources:
    target, period = find_period(rules, directions, source)
    x, r = divmod(period, len(directions))
    assert r == 0
    xs.append(x)
    if source == 0:
        assert target == parse_node_name("ZZZ")
        ans1 = period

assert ans1
ans2 = math.prod(xs) * len(directions)  # all `xs` are coprime

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
