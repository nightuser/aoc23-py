import sys
from collections.abc import Iterator

numbers = tuple(
    (str(d), word)
    for d, word in enumerate(
        ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine"),
        start=1,
    )
)


def suffixes(s: str) -> Iterator[str]:
    for i in range(len(s)):
        yield line[i:]


def extract_answer(digits: list[str]) -> int:
    return int(digits[0] + digits[-1])


ans1 = 0
ans2 = 0
fname = sys.argv[1]
with open(fname) as fh:
    for line in fh:
        line = line.rstrip()
        digits1 = []
        digits2 = []
        for suffix in suffixes(line):
            if suffix[0].isdigit():
                digits1.append(suffix[0])
                digits2.append(suffix[0])
            else:
                for d, word in numbers:
                    if suffix.startswith(word):
                        digits2.append(d)
        ans1 += extract_answer(digits1)
        ans2 += extract_answer(digits2)

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
