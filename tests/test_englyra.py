import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from englyra import EnglyraError, Runtime  # noqa: E402


class EnglyraRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.lines: list[str] = []
        self.runtime = Runtime.create(output=self.lines.append)

    def test_let_and_show_string(self):
        self.runtime.run('Let name be "Raghav"\nShow name')
        self.assertEqual(self.lines, ["Raghav"])

    def test_set_and_arithmetic(self):
        self.runtime.run("Let price be 12\nSet quantity to 4\nLet total be price times quantity\nShow total")
        self.assertEqual(self.lines, ["48"])

    def test_numeric_addition(self):
        self.runtime.run("Let result be 6 plus 7\nSay result")
        self.assertEqual(self.lines, ["13"])

    def test_case_insensitive_variable_names(self):
        self.runtime.run('Let Name be "Ada"\nShow name')
        self.assertEqual(self.lines, ["Ada"])

    def test_comments_and_blank_lines_are_ignored(self):
        self.runtime.run('\n# comment\nSay "ok"\n')
        self.assertEqual(self.lines, ["ok"])

    def test_unknown_variable_reports_error(self):
        with self.assertRaisesRegex(EnglyraError, "Line 1: I don't know a variable"):
            self.runtime.run("Show missing")

    def test_division_by_zero_is_rejected(self):
        with self.assertRaisesRegex(EnglyraError, "Cannot divide by zero"):
            self.runtime.run("Let broken be 5 divided by 0")

    def test_unknown_instruction_is_rejected_even_in_unselected_branch(self):
        with self.assertRaisesRegex(EnglyraError, "Line 2: Unknown instruction"):
            self.runtime.run('If 1 is equal to 2\n  Launch rocket\nEnd If')

    def test_if_true_branch(self):
        self.runtime.run('Let score be 90\nIf score is greater than 50\n  Say "pass"\nOtherwise\n  Say "retry"\nEnd If')
        self.assertEqual(self.lines, ["pass"])

    def test_if_otherwise_branch(self):
        self.runtime.run('Let score be 30\nIf score is at least 50\n  Say "pass"\nOtherwise\n  Say "retry"\nEnd If')
        self.assertEqual(self.lines, ["retry"])

    def test_if_without_otherwise(self):
        self.runtime.run('If 5 is equal to 5\n  Say "yes"\nEnd If')
        self.assertEqual(self.lines, ["yes"])

    def test_nested_if(self):
        self.runtime.run('If 1 is equal to 1\n If 2 is greater than 1\n  Say "nested"\n End If\nEnd If')
        self.assertEqual(self.lines, ["nested"])

    def test_repeat_executes_counted_block(self):
        self.runtime.run('Repeat 3 times\n  Say "hello"\nEnd Repeat')
        self.assertEqual(self.lines, ["hello", "hello", "hello"])

    def test_repeat_uses_variable_count(self):
        self.runtime.run('Let count be 2\nRepeat count times\n Say "again"\nEnd Repeat')
        self.assertEqual(self.lines, ["again", "again"])

    def test_nested_repeat_and_if(self):
        self.runtime.run('Let count be 0\nRepeat 3 times\n Set count to count plus 1\n If count is at most 2\n  Say count\n End If\nEnd Repeat')
        self.assertEqual(self.lines, ["1", "2"])

    def test_repeat_count_must_be_integer(self):
        with self.assertRaisesRegex(EnglyraError, "whole number"):
            self.runtime.run('Repeat 1.5 times\n Say "no"\nEnd Repeat')

    def test_repeat_count_is_bounded(self):
        with self.assertRaisesRegex(EnglyraError, "cannot be greater"):
            self.runtime.run('Repeat 10001 times\n Say "no"\nEnd Repeat')

    def test_unclosed_if_reports_line(self):
        with self.assertRaisesRegex(EnglyraError, "Line 1: This If block needs an 'End If'"):
            self.runtime.run('If 1 is equal to 1\n Say "missing close"')

    def test_unexpected_end_if_is_rejected(self):
        with self.assertRaisesRegex(EnglyraError, "Unexpected 'End If'"):
            self.runtime.run("End If")


if __name__ == "__main__":
    unittest.main()
