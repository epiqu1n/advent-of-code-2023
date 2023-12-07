from typing import List
from io import TextIOWrapper
from dataclasses import dataclass
import re
from operator import attrgetter
from pprint import pprint

type_matchers = [
    (r'(\w)\1{4}', '5oK'),
    (r'(\w)\1{3}', '4oK'),
    (r'(\w)\1{1}(\w)\2{2}|(\w)\3{2}(\w)\4{1}', 'FH'),
    (r'(\w)\1{2}', '3oK'),
    (r'(\w)\1{1}.*(\w)\2{1}', '2P'),
    (r'(\w)\1{1}', '1P'),
]

card_to_value_map = {
    card:idx for idx, card in enumerate(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
}

@dataclass
class HandResult:
    hand: str
    hand_strength: int
    hand_type_key: str
    bid: int


def get_hand_type(hand: str) -> (int, str):
    """Gets the hand type as an integer representing the strength of the hand (higher is better)"""
    for idx, type_matcher in enumerate(type_matchers):
        matcher, matcher_key = type_matcher
        if re.search(matcher, hand) is not None:
            return (len(type_matchers) - idx, matcher_key)

    return (0, 'HC')


def convert_hand_to_values(hand: str) -> List[int]:
    return [ card_to_value_map[char] for char in hand ]

def get_hands_by_strength(file: TextIOWrapper) -> List[HandResult]:
    """Returns every hand in the input data sorted by the hand type and strength,
    along with the bids for each
    """
    # Sort each hand
    # Pattern match to find type
    # Sort all hands based on type, strength
    # Do math
    hands = []
    for line in file:
        hand, bid = line.split(' ')
        sorted_hand = ''.join(sorted(hand))
        hand_strength, hand_type_key = get_hand_type(sorted_hand)
        hand_result = HandResult(hand=hand, hand_strength=hand_strength, hand_type_key=hand_type_key, bid=int(bid))
        hands.append(hand_result)

    hands.sort(
        key=lambda hand_result: convert_hand_to_values(attrgetter('hand')(hand_result)),
    )
    hands.sort(key=attrgetter('hand_strength'))

    return hands

def calculate_winnings(hands: List[HandResult]) -> int:
    """Calculates and sums winnings of each hand as rank * bid,
    where rank = index + 1
    """
    winnings_sum = 0
    for idx, hand in enumerate(hands):
        winnings_sum += hand.bid * (idx + 1)

    return winnings_sum

def main():
    with open('resources/day_7_values.txt', encoding='utf-8') as input_data:
        hands_by_strength = get_hands_by_strength(input_data)
        pprint(hands_by_strength)
        winnings = calculate_winnings(hands_by_strength)
        print('Winnings total:', winnings)


if __name__ == '__main__':
    main()
