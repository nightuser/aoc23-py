import math
import sys


def extract_input(line: str) -> tuple[list[int], int]:
    parts = line.rstrip().split()[1:]
    return list(map(int, parts)), int("".join(parts))


def calculate_range(t: int, d: int) -> int:
    dt = math.sqrt(t**2 - 4 * d) / 2
    low = int(math.floor(t / 2 - dt)) + 1
    high = int(math.ceil(t / 2 + dt)) - 1
    return high - low + 1


fname = sys.argv[1]
with open(fname) as fh:
    times1, time2 = extract_input(fh.readline())
    distances1, distance2 = extract_input(fh.readline())

ans1 = math.prod((calculate_range(t, d) for t, d in zip(times1, distances1)))
ans2 = calculate_range(time2, distance2)

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
