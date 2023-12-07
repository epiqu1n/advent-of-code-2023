from typing import List
from io import TextIOWrapper
from dataclasses import dataclass
import re
from operator import attrgetter
from pprint import pprint
from collections import OrderedDict



type_matchers = OrderedDict([
    ('5oK', r'(\w)\1{4}'),
    ('4oK', r'(\w)\1{3}'),
    ('FH', r'(\w)\1{1}(\w)\2{2}|(\w)\3{2}(\w)\4{1}'),
    ('3oK', r'(\w)\1{2}'),
    ('2P', r'(\w)\1{1}.*(\w)\2{1}'),
    ('1P', r'(\w)\1{1}'),
    ('HC', r'.'),
])
type_strengths = { hand_type:idx+1 for idx, (hand_type, _) in enumerate(type_matchers.items()) }


card_to_value_map = {
    card:idx for idx, card in enumerate(['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'])
}

@dataclass
class HandResult:
    hand: str
    hand_strength: int
    hand_type_key: str
    bid: int


def upgrade_hand_with_wildcard(hand_type_key: str) -> str:
    match hand_type_key:
        case 'J':
            return 'HC'
        case 'HC':
            return '1P'
        case '1P':
            return '3oK'
        case '2P':
            return 'FH'
        case '3oK':
            return '4oK'
        case '4oK':
            return '5oK'
        case _:
            raise ValueError(f'Unsupported hand_type_key: {hand_type_key}')


def get_hand_type_with_wildcards(hand_type_key: str, wildcard_count: int) -> (int, str):
    if wildcard_count >= 1:
        next_hand_type_key = upgrade_hand_with_wildcard(hand_type_key)
        return get_hand_type_with_wildcards(next_hand_type_key, wildcard_count - 1)
    else:
        return hand_type_key


def get_hand_type(hand: str) -> (int, str):
    """Gets the hand type as an integer representing the strength of the hand (higher is better)"""
    hand_without_j = hand.replace('J', '')
    j_count = len(hand) - len(hand_without_j)

    matched_hand_type_key: str
    for hand_type_key, matcher in type_matchers.items():
        if re.search(matcher, hand_without_j) is not None:
            matched_hand_type_key = hand_type_key
            break
    else:
        matched_hand_type_key = 'J'

    upgraded_hand_type_key = get_hand_type_with_wildcards(matched_hand_type_key, j_count)
    hand_strength = len(type_strengths) - type_strengths[upgraded_hand_type_key]

    return (hand_strength, upgraded_hand_type_key)


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
        # pprint(hands_by_strength)
        winnings = calculate_winnings(hands_by_strength)
        print('Winnings total:', winnings)


if __name__ == '__main__':
    main()
