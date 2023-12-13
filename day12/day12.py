import functools
import re
import sys


def drop(xs: tuple[str, ...], n: int) -> tuple[str, ...]:
    head = xs[0]
    if len(head) == n:
        return xs[1:]
    return (head[n:],) + xs[1:]


@functools.lru_cache
def count(patterns: tuple[str, ...], numbers: tuple[int, ...]) -> int:
    if not patterns:
        if numbers:
            return 0
        return 1
    if not numbers:
        if any("#" in pattern for pattern in patterns):
            return 0
        return 1

    pattern = patterns[0]
    number = numbers[0]

    if len(pattern) <= number:
        result = 0
        if len(pattern) == number:
            result += count(patterns[1:], numbers[1:])
        if "#" not in pattern:
            result += count(patterns[1:], numbers)
        return result

    first_match = pattern[number] != "#"
    if pattern[0] == "#" and not first_match:
        return 0
    result = 0
    if first_match:
        result += count(drop(patterns, number + 1), numbers[1:])
    if pattern[0] == "?":
        result += count(drop(patterns, 1), numbers)
    return result


def solve(pattern: str, numbers: tuple[int, ...]) -> int:
    patterns = tuple(filter(None, pattern.split(".")))
    return count(patterns, numbers)


def main() -> None:
    ans1 = 0
    ans2 = 0
    pattern_re = re.compile(r"\.\.+")
    fname = sys.argv[1] if len(sys.argv) == 2 else "in.txt"
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            pattern, numbers_raw = line.split()
            pattern = pattern_re.sub(".", pattern)
            numbers = tuple(map(int, numbers_raw.split(",")))
            ans1 += solve(pattern, numbers)
            ans2 += solve(
                "?".join([pattern] * 5),
                numbers * 5,
            )
    print(f"part1 = {ans1}")
    print(f"part2 = {ans2}")


if __name__ == "__main__":
    main()
