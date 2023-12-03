"""Day 2 - Part 1 solution"""
import re
from pprint import pprint
from typing import Literal, List
from dataclasses import dataclass

CubeColor = Literal["red", "green", "blue"]

def dict_access(cls):
    """A decorator to enable dynamic attribute access for classes"""
    cls.__getitem__ = lambda self, attr: getattr(self, attr)
    return cls


@dataclass
@dict_access
class CubeCountMatch:
    """A regex match for a single color of cube and its count"""
    color: CubeColor
    count: int

    def __init__(self, count: str, color: CubeColor):
        self.count = int(count)
        self.color = color

@dataclass
@dict_access
class RoundResult:
    """Cube pull results from a round of the game"""
    red: int
    green: int
    blue: int

@dataclass
@dict_access
class CubeBag:
    """A bag of cubes and the count of each color"""
    red: int = 0
    green: int = 0
    blue: int = 0

@dataclass
@dict_access
class GameResult:
    """Results from a single game"""
    game_num: int
    round_results: List[RoundResult]

def parse_round_result(round_result: str) -> RoundResult:
    """Parses out the results of cube pulls from a single round of the game"""
    round_regex = r"(?P<count>\d+) (?P<color>red|blue|green)"
    cube_counts: List[CubeCountMatch] = [
        match.groupdict() for match in re.finditer(round_regex, round_result)
    ]
    round_result: RoundResult = { cube['color']:int(cube['count']) for cube in cube_counts }
    return round_result

def parse_game_results(line: str) -> GameResult:
    """Parses out data from an input line"""
    game_regex = r"Game (\d+):"
    game_num = int(re.search(game_regex, line).groups()[0])
    game_result_str = re.split(r"Game \d+:", line)[1].strip()

    round_results: List[RoundResult] = [
        parse_round_result(round) for round in re.split('; ', game_result_str)
    ]

    return GameResult(game_num, round_results)

def check_if_game_valid(game_result: GameResult, cube_bag: CubeBag) -> bool:
    """Checks to see if a game result is valid based on the given cube bag"""
    for round_result in game_result.round_results:
        for color in round_result:
            if round_result[color] > cube_bag[color]:
                return False

    return True


def main() -> None:
    """Main"""
    cube_bag = CubeBag(red=12, green=13, blue=14)
    game_id_total = 0

    with open("resources/day_2_values.txt", encoding="utf-8") as input_data:
        for line in input_data:
            game_result = parse_game_results(line)
            if check_if_game_valid(game_result, cube_bag):
                game_id_total += game_result.game_num

    print(game_id_total)

if __name__ == "__main__":
    main()
