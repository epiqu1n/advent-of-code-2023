from dataclasses import dataclass
import unittest
from solutions.day_8.part_1 import DesertMap
from io import StringIO, TextIOWrapper

@dataclass
class TestCaseData:
    file: TextIOWrapper
    instructions: list[str]
    root_node_value: str
    left_right_node_value: str
    """The value of the node that should be found by going left then right, starting at the root node"""
    steps_to_finish: int


case_1 = TestCaseData(
    file=StringIO(
        """RL
        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)
        """
    ),
    instructions=['R', 'L'],
    root_node_value='AAA',
    left_right_node_value='EEE',
    steps_to_finish=2,
)

case_2 = TestCaseData(
    file=StringIO(
        """LLR
        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """
    ),
    instructions=['L', 'L', 'R'],
    root_node_value='AAA',
    left_right_node_value = 'ZZZ',
    steps_to_finish=6,
)


class TestDay8Part1(unittest.TestCase):
    desert_map_1: DesertMap
    desert_map_2: DesertMap

    @classmethod
    def setUpClass(cls) -> None:
        cls.desert_map_1 = DesertMap.parse_map_from_file(case_1.file)
        cls.desert_map_2 = DesertMap.parse_map_from_file(case_2.file)

    def test_parse_desert_map(self):
        with self.subTest(case=1):
            self.assertEqual(self.desert_map_1.instructions, case_1.instructions)
            self.assertEqual(self.desert_map_1.root_node.value, case_1.root_node_value)
            self.assertEqual(
                self.desert_map_1.root_node.left.right.value, # type: ignore -- root_node.left.right should be defined
                case_1.left_right_node_value,
            )

        with self.subTest(case=2):
            self.assertEqual(self.desert_map_2.instructions, case_2.instructions)
            self.assertEqual(self.desert_map_2.root_node.value, case_2.root_node_value)
            self.assertEqual(
                self.desert_map_2.root_node.left.right.value, # type: ignore -- root_node.left.right should be defined
                case_2.left_right_node_value,
            )

    def test_count_steps(self):
        with self.subTest(case=1):
            zzz_step_count = self.desert_map_1.traverse_to_zzz()
            self.assertEqual(zzz_step_count, case_1.steps_to_finish)

        with self.subTest(case=2):
            zzz_step_count = self.desert_map_2.traverse_to_zzz()
            self.assertEqual(zzz_step_count, case_2.steps_to_finish)


if __name__ == '__main__':
    unittest.main()
