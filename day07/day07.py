from __future__ import annotations

import collections
import dataclasses
import enum
import operator
import sys


def build_card_order(name: str, order: str) -> dict[str, int]:
    return {card: pos for pos, card in enumerate(order)}


CARDS_ORDER1 = build_card_order("Cards1", "23456789TJQKA")
CARDS_ORDER2 = build_card_order("Cards2", "J23456789TQKA")


def transform_hand(hand: str, cards_order: dict[str, int]) -> tuple[int, ...]:
    return tuple(cards_order[card] for card in hand)


class HandType(enum.IntEnum):
    HIGH_CARD = enum.auto()
    ONE_PAIR = enum.auto()
    TWO_PAIR = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    FIVE_OF_A_KIND = enum.auto()

    @classmethod
    def from_hand(cls, hand: str) -> HandType:
        occurs = collections.Counter(hand)
        shape = tuple(sorted(occurs.values()))
        match shape:
            case (1, 1, 1, 1, 1):
                return cls.HIGH_CARD
            case (_, _, _, _):
                return cls.ONE_PAIR
            case (1, 2, 2):
                return cls.TWO_PAIR
            case (_, _, _):
                return cls.THREE_OF_A_KIND
            case (2, _):
                return cls.FULL_HOUSE
            case (1, _):
                return cls.FOUR_OF_A_KIND
            case (_,):
                return cls.FIVE_OF_A_KIND
            case ():
                return cls.FIVE_OF_A_KIND
            case _:
                raise ValueError(f"unknown shape {shape}")


@dataclasses.dataclass(init=False, slots=True)
class Hand:
    hand: tuple[int, ...]
    type: HandType

    def __lt__(self, other: Hand) -> bool:
        return (self.type, self.hand) < (other.type, other.hand)


class Hand1(Hand):
    def __init__(self, hand: str):
        self.hand = transform_hand(hand, CARDS_ORDER1)
        self.type = HandType.from_hand(hand)


class Hand2(Hand):
    def __init__(self, hand: str):
        self.hand = transform_hand(hand, CARDS_ORDER2)
        hand_without_jokers = str("".join(card for card in hand if card != "J"))
        self.type = HandType.from_hand(hand_without_jokers)


def extract_answer(hands: list[tuple[Hand, int]]) -> int:
    return sum(rank * bid for rank, (_, bid) in enumerate(hands, start=1))


hands1: list[tuple[Hand, int]] = []
hands2: list[tuple[Hand, int]] = []
fname = sys.argv[1]
with open(fname) as fh:
    for line in fh:
        line = line.rstrip()
        hand, bid = line.split(maxsplit=1)
        bid = int(bid)
        hands1.append((Hand1(hand), bid))
        hands2.append((Hand2(hand), bid))

bid_key = operator.itemgetter(0)
hands1.sort(key=bid_key)
hands2.sort(key=bid_key)

ans1 = extract_answer(hands1)
ans2 = extract_answer(hands2)

print(f"part1 = {ans1}")
print(f"part2 = {ans2}")
