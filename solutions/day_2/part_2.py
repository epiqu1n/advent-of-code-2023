"""Day 2 - Part 1 solution"""
import re
from pprint import pprint
from typing import Literal, List, TypedDict
from dataclasses import dataclass

CubeColor = Literal["red", "green", "blue"]

@dataclass
class CubeCountMatch:
    """A regex match for a single color of cube and its count"""
    color: CubeColor
    count: int

    def __init__(self, count: str, color: CubeColor):
        self.count = int(count)
        self.color = color

class RoundResult(TypedDict):
    """Cube pull results from a round of the game"""
    red: int
    green: int
    blue: int

class CubeBag(TypedDict):
    """A bag of cubes and the count of each color"""
    red: int = 0
    green: int = 0
    blue: int = 0

class GameResult(TypedDict):
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

    return { "game_num": game_num, "round_results": round_results }

def get_min_necessary_cubes(game_result: GameResult) -> CubeBag:
    """Determines the minimum necessary number of colored cubes
    needed in the bag for the game result to valid.
    """
    cube_bag: CubeBag = { "red": 0, "blue": 0, "green": 0 }
    for round_result in game_result["round_results"]:
        for color in round_result:
            if round_result[color] > cube_bag[color]:
                cube_bag[color] = round_result[color]

    return cube_bag

def cube_bag_power(cube_bag: CubeBag) -> int:
    """Calculates the "power" of cubes in a bag as the product of the cube counts"""
    power = 1
    for color in cube_bag:
        power *= cube_bag[color]

    return power

def main() -> None:
    """Main"""
    total_cube_power = 0

    with open("resources/day_2_values.txt", encoding="utf-8") as input_data:
        for line in input_data:
            game_result = parse_game_results(line)
            cube_bag = get_min_necessary_cubes(game_result)
            total_cube_power += cube_bag_power(cube_bag)

    print(total_cube_power)

if __name__ == "__main__":
    main()
