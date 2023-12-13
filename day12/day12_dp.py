import functools
import itertools
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
    number_of_dots = list(
        itertools.accumulate((int(c == ".") for c in pattern), initial=0)
    )

    N = len(pattern)
    M = len(numbers)

    dp = [[0 for _ in range(M + 1)] for _ in range(N + 1)]
    dp[N][M] = 1
    for i in range(N - 1, -1, -1):
        dp[i][M] = 0 if pattern[i] == "#" else dp[i + 1][M]
        if pattern[i] == ".":
            dp[i] = dp[i + 1]
            continue
        for j in range(M - 1, -1, -1):
            end = i + numbers[j]
            first_match = 0
            if end <= N:
                if (number_of_dots[end] - number_of_dots[i]) == 0:
                    if end == N:
                        first_match = 1
                    elif pattern[end] != "#":
                        first_match = 2
            if pattern[i] == "#" and first_match == 0:
                continue
            if first_match == 1:
                dp[i][j] = dp[N][j + 1]
            elif first_match == 2:
                dp[i][j] = dp[end + 1][j + 1]
            if pattern[i] == "?":
                dp[i][j] += dp[i + 1][j]

    return dp[0][0]


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
            ans1 += solve(pattern.strip("."), numbers)
            ans2 += solve(
                "?".join([pattern] * 5).strip("."),
                numbers * 5,
            )
    print(f"part1 = {ans1}")
    print(f"part2 = {ans2}")


if __name__ == "__main__":
    main()
