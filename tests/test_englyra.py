import unittest

from pathlib import Path
import sys

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

    def test_unknown_instruction_is_rejected(self):
        with self.assertRaisesRegex(EnglyraError, "Unknown instruction"):
            self.runtime.run("Launch a rocket")


if __name__ == "__main__":
    unittest.main()
