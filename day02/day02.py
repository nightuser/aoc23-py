from __future__ import annotations

import dataclasses
import sys


@dataclasses.dataclass
class Round:
    r: int = 0
    g: int = 0
    b: int = 0

    def update(self, other: Round) -> None:
        self.r = max(self.r, other.r)
        self.g = max(self.g, other.g)
        self.b = max(self.b, other.b)

    def fits(self, r: int, g: int, b: int) -> bool:
        return self.r <= r and self.g <= g and self.b <= b

    def power(self) -> int:
        return self.r * self.g * self.b


games = []
fname = sys.argv[1]
with open(fname) as fh:
    for line in fh:
        line = line.rstrip()
        prefix_raw, rounds_raw = line.split(": ", maxsplit=1)
        _, game_id = prefix_raw.split(" ", maxsplit=1)
        game_id = int(game_id)
        rounds = []
        for round_raw in rounds_raw.split("; "):
            round = Round()
            for entry_raw in round_raw.split(", "):
                amount, color = entry_raw.split(" ", maxsplit=1)
                amount = int(amount)
                match color:
                    case "red":
                        round.r = amount
                    case "green":
                        round.g = amount
                    case "blue":
                        round.b = amount
                    case _:
                        raise ValueError(f"Unexpected color: `{color}`")
            rounds.append(round)
        games.append((game_id, rounds))

ans1 = 0
ans2 = 0
for game_id, rounds in games:
    bag = Round(r=0, g=0, b=0)
    for round in rounds:
        bag.update(round)

    if bag.fits(12, 13, 14):
        ans1 += game_id
    ans2 += bag.power()

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
