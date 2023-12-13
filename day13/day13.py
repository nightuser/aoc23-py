import sys
from typing import Optional


def dist(xs: list[str], i: int, k: int) -> int:
    return sum(c1 != c2 for c1, c2 in zip(xs[i + k], xs[i - k - 1], strict=True))


def weak_palindromes(xs: list[str]) -> list[tuple[int, Optional[int]]]:
    left = 0
    right = -1
    big_mismatch = None

    result: list[tuple[int, Optional[int]]] = []

    for i in range(len(xs)):
        k = 0
        mismatch = None
        found = False
        if i <= right:
            j = right - i + left + 1
            small_mismatch = result[j][1]
            k = min(right - i + 1, result[j][0])
            mismatches: set[int] = set()
            if small_mismatch is not None:
                mismatches.add(small_mismatch)
            if big_mismatch is not None:
                pos = (left + right + 1) // 2 + big_mismatch
                if pos >= i:
                    m = pos - i
                else:
                    m = i - pos - 1
                mismatches.add(m)
            mismatch = None
            for m in sorted(mismatches):
                if m >= k:
                    break
                diff = dist(xs, i, m)
                if diff >= 1:
                    if diff > 1 or mismatch is not None:
                        k = m
                        found = True
                        break
                    mismatch = m
        if not found:
            while i + k < len(xs) and i - k - 1 >= 0:
                diff = dist(xs, i, k)
                if diff >= 1:
                    if diff > 1 or mismatch is not None:
                        break
                    mismatch = k
                k += 1
        result.append((k, mismatch))
        if i + k - 1 > right:
            left = i - k
            right = i + k - 1
            big_mismatch = mismatch

    return result


def solve(xs: list[str]) -> tuple[int, int]:
    wps = weak_palindromes(xs)
    result1 = 0
    result2 = 0
    for i, (k, m) in enumerate(wps):
        if k > 0 and (i - k == 0 or i + k - 1 == len(xs) - 1):
            if m is None:
                result1 += i
            else:
                result2 += i
    return result1, result2


def summarize(c: int, r: int) -> int:
    return c + 100 * r


ans1 = 0
ans2 = 0
fname = sys.argv[1]
with open(fname) as fh:
    eof = False
    while not eof:
        eof = True
        rows = []
        for line in fh:
            line = line.rstrip()
            if not line:
                eof = False
                break
            rows.append(line)
        cols = ["".join(col) for col in zip(*rows)]

        c1, c2 = solve(cols)
        r1, r2 = solve(rows)

        ans1 += summarize(c1, r1)
        ans2 += summarize(c2, r2)

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")

if fname == "in.txt":
    assert ans1 == 33195
    assert ans2 == 31836


# print(
#     weak_palindromes(
#         ["....", "#...", ".#..", ".#.#", "#...", "#...", ".#.#", ".#..", "#.#.", "#..."]
#     )
# )
# print(
#     weak_palindromes(
#         ["....", "#...", ".#..", ".#.#", "#...", "#.#.", ".#.#", ".#..", "#...", "#..."]
#     )
# )
