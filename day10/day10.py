from __future__ import annotations

import enum
import sys


class Dir(enum.Enum):
    TOP = enum.auto()
    BOTTOM = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class Pipe(enum.Enum):
    TB = "|"
    LR = "-"
    TL = "J"
    TR = "L"
    BL = "7"
    BR = "F"

    @classmethod
    def from_dirs(cls, dirs: tuple[Dir, ...]) -> tuple[Pipe, Dir]:
        match dirs:
            case (Dir.TOP, Dir.BOTTOM):
                pipe = cls.TB
            case (Dir.LEFT, Dir.RIGHT):
                pipe = cls.LR
            case (Dir.TOP, Dir.LEFT):
                pipe = cls.TL
            case (Dir.TOP, Dir.RIGHT):
                pipe = cls.TR
            case (Dir.BOTTOM, Dir.LEFT):
                pipe = cls.BL
            case (Dir.BOTTOM, Dir.RIGHT):
                pipe = cls.BR
            case _:
                raise ValueError
        return pipe, dirs[0]


PIPES = {p.value for p in Pipe}
TOP_PIPES = {Pipe.TB, Pipe.TL, Pipe.TR}
BOTTOM_PIPES = {Pipe.TB, Pipe.BL, Pipe.BR}
LEFT_PIPES = {Pipe.LR, Pipe.TL, Pipe.BL}
RIGHT_PIPES = {Pipe.LR, Pipe.TR, Pipe.BR}


Node = tuple[int, int]
Graph = dict[Node, Pipe]


def get_start_type(graph: Graph, start: Node) -> tuple[Pipe, Dir]:
    x, y = start
    top = (x, y - 1)
    bottom = (x, y + 1)
    left = (x - 1, y)
    right = (x + 1, y)
    dirs = []
    if top in graph and graph[top] in BOTTOM_PIPES:
        dirs.append(Dir.TOP)
    if bottom in graph and graph[bottom] in TOP_PIPES:
        dirs.append(Dir.BOTTOM)
    if left in graph and graph[left] in RIGHT_PIPES:
        dirs.append(Dir.LEFT)
    if right in graph and graph[right] in LEFT_PIPES:
        dirs.append(Dir.RIGHT)
    dirs = tuple(dirs)
    return Pipe.from_dirs(dirs)


def move_up(node: Node) -> tuple[Node, Dir]:
    x, y = node
    return (x, y - 1), Dir.BOTTOM


def move_down(node: Node) -> tuple[Node, Dir]:
    x, y = node
    return (x, y + 1), Dir.TOP


def move_left(node: Node) -> tuple[Node, Dir]:
    x, y = node
    return (x - 1, y), Dir.RIGHT


def move_right(node: Node) -> tuple[Node, Dir]:
    x, y = node
    return (x + 1, y), Dir.LEFT


def move(graph: Graph, node: Node, dir: Dir) -> tuple[Node, Dir]:
    type = graph[node]
    match (dir, type):
        case (Dir.BOTTOM, Pipe.TB) | (Dir.LEFT, Pipe.TL) | (Dir.RIGHT, Pipe.TR):
            return move_up(node)
        case (Dir.TOP, Pipe.TB) | (Dir.LEFT, Pipe.BL) | (Dir.RIGHT, Pipe.BR):
            return move_down(node)
        case (Dir.TOP, Pipe.TL) | (Dir.BOTTOM, Pipe.BL) | (Dir.RIGHT, Pipe.LR):
            return move_left(node)
        case (Dir.TOP, Pipe.TR) | (Dir.BOTTOM, Pipe.BR) | (Dir.LEFT, Pipe.LR):
            return move_right(node)
        case _:
            raise ValueError


start = None
graph: Graph = {}
fname = sys.argv[1]
with open(fname) as fh:
    for y, line in enumerate(fh):
        line = line.rstrip()
        for x, type in enumerate(line):
            node = (x, y)
            if type == "S":
                assert start is None
                start = node
            if type in PIPES:
                graph[node] = Pipe(type)
assert start
graph[start], dir = get_start_type(graph, start)
node = start
path = 0
area = 0
while True:
    x1, y1 = node
    node, dir = move(graph, node, dir)
    x2, y2 = node
    path += 1
    area += x1 * y2 - x2 * y1
    if node == start:
        break
area = abs(area) // 2

ans1 = path // 2
ans2 = area - path // 2 + 1

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
