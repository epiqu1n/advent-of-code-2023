from dataclasses import dataclass
from io import TextIOWrapper
from operator import itemgetter
import re
from typing import Self, cast
from math import lcm

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
    start_nodes: list[Node]
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
    def is_start_node(node: Node) -> bool:
        return node.value[-1] == 'A'
    
    @staticmethod
    def is_end_node(node: Node) -> bool:
        return node.value[-1] == 'Z'

    @staticmethod
    def parse_map_from_file(file: TextIOWrapper) -> 'DesertMap':
        temp_node_map: dict[str, TempNode] = { }
        start_nodes: list[Node] = []

        # Get instructions from first line
        instructions = DesertMap.__parse_instructions(file.readline())

        # Parse out the nodes from the file, without yet building node links
        for line in file:
            temp_node = DesertMap.__parse_temp_node(line)
            if not temp_node:
                continue
            actual_node = temp_node.node
            temp_node_map[actual_node.value] = temp_node
            if DesertMap.is_start_node(actual_node):
                start_nodes.append(actual_node)

        if len(start_nodes) == 0:
            raise RuntimeError('No nodes could be found in the given file')

        # Now go back and establish actual node links
        for temp_node in temp_node_map.values():
            DesertMap.__link_node(temp_node, temp_node_map)

        return DesertMap(instructions, start_nodes)

    @staticmethod
    def check_all_node_ends_found(node_final_steps: list[int]) -> bool:
        for steps in node_final_steps:
            if steps == -1:
                return False
        return True

    def wacky_traversal(self) -> list[int]:
        """
        Traverses the node tree using the instructions,returning the number of steps
        to simulateously reach each end node from each starting node
        """
        steps = 0
        curr_nodes: list[Node] = self.start_nodes
        node_final_steps: list[int] = [ -1 for _ in curr_nodes ]
        while True:
            for instruction in self.instructions:
                if DesertMap.check_all_node_ends_found(node_final_steps):
                    print('Found all end nodes!')
                    return node_final_steps
                if steps >= 100000000:
                    raise RuntimeError('Ah shite')
                
                for idx, node in enumerate(curr_nodes):
                    if node_final_steps[idx] == -1 and DesertMap.is_end_node(node):
                        node_final_steps[idx] = steps
                    curr_nodes[idx] = cast(Node, node.left if instruction == 'L' else node.right)
                
                steps += 1
        

def main():
    with open('resources/day_8_values.txt', encoding='utf8') as file:
        desert_map = DesertMap.parse_map_from_file(file)
        step_counts = desert_map.wacky_traversal()
        print(f'Step count: {lcm(*step_counts)}')

if __name__ == '__main__':
    main()
