import collections
import sys

ans1 = 0
ans2 = 0

copies: collections.deque[int] = collections.deque()

fname = sys.argv[1]
with open(fname) as fh:
    for line in fh:
        line = line.rstrip()
        prefix, arrays = line.split(":", maxsplit=1)
        _, card_id = prefix.split()
        card_id = int(card_id)
        winning, ours = (
            map(int, array.strip().split()) for array in arrays.split(" | ", maxsplit=1)
        )
        winning = set(winning)
        ours = list(ours)

        if copies:
            amount = copies.popleft()
        else:
            amount = 1

        matches = 0
        for x in ours:
            if x in winning:
                if matches >= len(copies):
                    copies.append(1)
                copies[matches] += amount
                matches += 1

        if matches > 0:
            ans1 += 1 << (matches - 1)
        ans2 += amount

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
