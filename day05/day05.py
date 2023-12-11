import bisect
import operator
import sys
from typing import cast

MappingRange = tuple[int, int, int]
MappingRanges = list[MappingRange]
mapping_key = operator.itemgetter(1)
InputRange = tuple[int, int]
InputRanges = list[InputRange]
input_key = operator.itemgetter(0)


def group_input(input: list[int]) -> InputRanges:
    args = [iter(input)] * 2
    return list(zip(*args))


def find_range(ranges: MappingRanges, id: int) -> int:
    return bisect.bisect_right(ranges, id, key=mapping_key) - 1


def compactify(input: InputRanges) -> InputRanges:
    result: InputRanges = []

    input.sort(key=input_key)
    i = 0
    while i < len(input):
        id, size = input[i]
        i += 1
        while i < len(input):
            new_id, new_size = input[i]
            if id + size != new_id:
                break
            size += new_size
            i += 1
        result.append((id, size))

    return result


def transform(ranges: MappingRanges, input: InputRanges) -> InputRanges:
    result: InputRanges = []
    id = 0
    size = 0

    def add_range(new_id: int, new_size: int) -> None:
        nonlocal id, size
        if new_size > 0:
            result.append((new_id, new_size))
            id += new_size
            size -= new_size

    for id, size in input:
        range_id = find_range(ranges, id)
        while size > 0:
            if range_id >= 0:
                target_id, source_id, range_size = ranges[range_id]
                new_id = id + target_id - source_id
                new_size = new_size = min(size, range_size - (id - source_id))
                add_range(new_id, new_size)

            if size == 0:
                break

            new_size = size
            if range_id + 1 < len(ranges):
                next_source_id = ranges[range_id + 1][1]
                new_size = min(new_size, next_source_id - id)
            add_range(id, new_size)

            range_id += 1

    return compactify(result)


def extract_answer(input: InputRanges) -> int:
    return min(input, key=input_key)[0]


fname = sys.argv[1]
with open(fname) as fh:
    seeds = fh.readline().rstrip()
    _, seeds = seeds.split(": ", maxsplit=1)
    seeds = [int(seed) for seed in seeds.split()]
    fh.readline()

    current1: InputRanges = [(seed, 1) for seed in seeds]
    current2: InputRanges = group_input(seeds)

    current1 = compactify(current1)
    current2 = compactify(current2)

    for title in fh:
        title = title.rstrip()
        if not title:
            break
        mapping, _ = title.split(" ", maxsplit=1)
        source, target = mapping.split("-to-", maxsplit=1)

        ranges: MappingRanges = []
        for line in fh:
            line = line.rstrip()
            if not line:
                break
            new_range = cast(MappingRange, tuple(map(int, line.split(" ", maxsplit=2))))
            ranges.append(new_range)

        ranges.sort(key=mapping_key)

        current1 = transform(ranges, current1)
        current2 = transform(ranges, current2)

ans1 = extract_answer(current1)
ans2 = extract_answer(current2)

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
