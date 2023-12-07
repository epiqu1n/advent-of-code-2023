"""Day 5 part 1"""

import re
from typing import List, Self, Dict
from dataclasses import dataclass
from io import TextIOWrapper
from pprint import pprint, pformat
from math import floor

@dataclass
class IdMap:
    source_range_start: int
    target_range_start: int
    range_length: int

    def compare_to_range(self, number: int, against: 'source' or 'target') -> -1 or 0 or 1:
        """Compares a number against a range (source or target), to see if it is
        in the range (0), before it (-1), or after it (1)
        """
        range_start = self.source_range_start if against == 'source' else self.target_range_start
        return (
            -1 if number < range_start
            else 1 if number > (range_start + self.range_length - 1)
            else 0
        )

    def compare_to_source(self, number: int) -> -1 or 0 or 1:
        return self.compare_to_range(number, 'source')

    def compare_to_target(self, number: int) -> -1 or 0 or 1:
        return self.compare_to_range(number, 'target')

    def convert_source_to_target(self, source_number: int) -> int:
        range_diff = self.target_range_start - self.source_range_start
        return source_number + range_diff

    @staticmethod
    def from_text(text: str) -> Self:
        """Takes in a line such as `1923 485 243` and converts it to an IdMap"""
        (target_range_start, source_range_start, range_length) = text.split(' ')
        return IdMap(int(source_range_start), int(target_range_start), int(range_length))


class IdMapTree:
    maps: Dict[str, List[IdMap]] = { }
    map_order = [
        'seed-to-soil',
        'soil-to-fertilizer',
        'fertilizer-to-water',
        'water-to-light',
        'light-to-temperature',
        'temperature-to-humidity',
        'humidity-to-location',
    ]

    @staticmethod
    def from_file(file: TextIOWrapper) -> Self:
        map_name_regex = r'(?P<map_name>[\w-]+) map:'
        curr_map_name: str or None = None

        id_map_tree = IdMapTree()

        for line in file:
            map_name_result = re.search(map_name_regex, line)

            if map_name_result is not None:
                curr_map_name = map_name_result.groupdict().get('map_name')
                id_map_tree.maps[curr_map_name] = []
            elif curr_map_name is None or not line.strip():
                pass # Pass if no map name has been seen yet, or if the line is blank
            else:
                id_map = IdMap.from_text(line)
                id_map_tree.add_id_map_sorted(curr_map_name, id_map)

        return id_map_tree

    def add_id_map_sorted(self, map_key: str, new_map: IdMap) -> None:
        map_list = self.maps[map_key]
        for idx, id_map in enumerate(map_list):
            if new_map.source_range_start < id_map.source_range_start:
                map_list.insert(idx, new_map)
                break
        else:
            map_list.append(new_map)


    def convert_value(self, num: int, map_key: str) -> int:
        """Finds a value in the given map, and coverts it to its corresponding value
        e.g. Takes in a seed value and outputs a soil value
        """
        map_list = self.maps[map_key].copy()

        while len(map_list) > 0:
            mid_idx = floor(len(map_list) / 2)
            curr_map: IdMap = map_list[mid_idx]
            relative_num_pos = curr_map.compare_to_source(num)

            match relative_num_pos:
                case 0:
                    return curr_map.convert_source_to_target(num)
                case 1:
                    map_list = map_list[(mid_idx + 1) : len(map_list)]
                    continue
                case -1:
                    map_list = map_list[0 : (mid_idx)]
                    continue

        return num

    def find_location_from_seed(self, seed: int) -> int:
        curr_value = seed
        for map_key in self.map_order:
            curr_value = self.convert_value(curr_value, map_key)
        return curr_value

    def __repr__(self):
        return pformat(self.maps)


def main():
    with open('resources/day_5_values.txt', encoding='utf-8') as file:
        seeds_line = file.readline()
        seeds_regex = r'(\d+)'
        seeds = [ int(num) for num in re.findall(seeds_regex, seeds_line) ]

        id_map_tree = IdMapTree.from_file(file)

        locations = [ id_map_tree.find_location_from_seed(seed) for seed in seeds ]
        min_location = min(locations)

        print(f'Lowest location: {min_location}')

if __name__ == "__main__":
    main()
