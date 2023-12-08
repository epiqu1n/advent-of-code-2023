from dataclasses import dataclass
from io import TextIOWrapper
from operator import itemgetter
from pprint import pprint
import re
from typing import Self

@dataclass
class Node:
    value: str
    left: Self | None = None
    right: Self | None = None

@dataclass
class TempNode:
    node: Node
    left_value: str
    right_value: str

@dataclass
class DesertMap:
    instructions: list[str]
    root_node: Node
    __node_regex = r'(?P<node_value>\w{3}) = \((?P<left_value>\w{3}), (?P<right_value>\w{3})\)'

    @staticmethod
    def __parse_temp_node(text: str) -> TempNode | None:
        node_match = re.search(DesertMap.__node_regex, text)
        if not node_match:
            return None
        node_value, left_value, right_value = itemgetter('node_value', 'left_value', 'right_value')(node_match.groupdict())
        node = Node(node_value)
        return TempNode(node, left_value, right_value)
    
    @staticmethod
    def __link_node(temp_node: TempNode, temp_node_map: dict[str, TempNode]) -> None:
        """Links a Node from a given TempNode to the actual Nodes."""
        node = temp_node.node
        if node.value not in temp_node_map:
            raise ValueError(f'Temp node with value {node.value} could not be found in the given map')
        
        node.left = temp_node_map[temp_node.left_value].node
        node.right = temp_node_map[temp_node.right_value].node

    @staticmethod
    def __parse_instructions(text: str) -> list[str]:
        return list(text.strip())

    @staticmethod
    def parse_map_from_file(file: TextIOWrapper) -> 'DesertMap':
        temp_node_map: dict[str, TempNode] = { }
        root_node: Node | None = None

        # Get instructions from first line
        instructions = DesertMap.__parse_instructions(file.readline())

        # Parse out the nodes from the file, without yet building node links
        for line in file:
            temp_node = DesertMap.__parse_temp_node(line)
            if not temp_node:
                continue
            temp_node_map[temp_node.node.value] = temp_node
            if not root_node:
                root_node = temp_node.node

        if not root_node:
            raise RuntimeError('No nodes could be found in the given file')

        # Now go back and establish actual node links
        for temp_node in temp_node_map.values():
            DesertMap.__link_node(temp_node, temp_node_map)

        return DesertMap(instructions, root_node)

    def traverse_to_zzz(self) -> int:
        """Traverses the node tree using the instructions, returning the number of steps to reach 'ZZZ'"""
        def traverse_with_instructions(from_node: Node, step_count: int = 0) -> int:
            steps = step_count
            curr_node: Node | None = from_node
            for instruction in self.instructions:
                if not curr_node:
                    raise RuntimeError('No current node')
                if curr_node.value == 'ZZZ':
                    print('Found ZZZ!')
                    return steps
                if steps >= 1000:
                    raise RuntimeError('Ah shite')
                
                last_node = curr_node
                curr_node = curr_node.left if instruction == 'L' else curr_node.right
                steps += 1
                print(f'Step {steps}: Traversing {"left" if instruction == "L" else "right"} from {last_node.value} to {curr_node.value}') # type: ignore -- logging

            if not curr_node:
                raise RuntimeError('No current node')
            
            return traverse_with_instructions(curr_node, steps)
        
        return traverse_with_instructions(self.root_node)

def main():
    with open('resources/day_8_values.txt', encoding='utf8') as file:
        desert_map = DesertMap.parse_map_from_file(file)
        pprint(desert_map.instructions)
        step_count = desert_map.traverse_to_zzz()
        print(f'Step count: {step_count}')

if __name__ == '__main__':
    main()
