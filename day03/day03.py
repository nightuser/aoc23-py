import collections
import itertools
import re
import sys

Position = tuple[int, int]

number_re = re.compile(r"\d+")
symbol_re = re.compile(r"[^\d.]")

numbers = []
symbols = {}
fname = sys.argv[1]
with open(fname) as fh:
    for i, line in enumerate(fh):
        line = line.rstrip()
        numbers.extend(
            [(int(m.group()), i, m.start(), m.end()) for m in number_re.finditer(line)]
        )
        symbols.update({(i, m.start()): m.group() for m in symbol_re.finditer(line)})

ans1 = 0
gears = collections.defaultdict(list)
for number, i, start, end in numbers:
    border = itertools.chain(
        [(i, start - 1), (i, end)],
        itertools.product([i - 1, i + 1], range(start - 1, end + 1)),
    )
    adjacent = False
    for pos in border:
        if pos in symbols:
            adjacent = True
            if symbols[pos] == "*":
                gears[pos].append(number)
    if adjacent:
        ans1 += number

ans2 = 0
for neighbors in gears.values():
    if len(neighbors) == 2:
        ans2 += neighbors[0] * neighbors[1]

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
