#!/usr/bin/env python3
"""A tiny, dependency-free Englyra v0.1 interpreter prototype.

This is intentionally a small and safe language experiment, not a general-purpose
English-to-code AI. It interprets only the statements documented in the spec.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


class EnglyraError(Exception):
    """Raised when an Englyra statement cannot be interpreted."""


@dataclass
class Runtime:
    variables: dict[str, object]
    output: Callable[[str], None]

    @classmethod
    def create(cls, output: Callable[[str], None] = print) -> "Runtime":
        return cls(variables={}, output=output)

    def evaluate(self, expression: str) -> object:
        expr = expression.strip()
        if not expr:
            raise EnglyraError("Expected a value after the instruction.")

        # Quoted text uses JSON string rules so escaping is unambiguous.
        if expr.startswith('"'):
            try:
                value = json.loads(expr)
            except json.JSONDecodeError as exc:
                raise EnglyraError(f"Invalid quoted text: {exc.msg}.") from exc
            if not isinstance(value, str):
                raise EnglyraError("Quoted text must be one complete string.")
            return value

        if re.fullmatch(r"-?\d+", expr):
            return int(expr)
        if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", expr):
            return float(expr)

        # One basic operation per expression is enough for the first prototype.
        op_pattern = re.compile(r"^(.+?)\s+(divided by|plus|minus|times)\s+(.+)$", re.IGNORECASE)
        match = op_pattern.match(expr)
        if match:
            left = self.evaluate(match.group(1))
            operator = match.group(2).lower()
            right = self.evaluate(match.group(3))
            if isinstance(left, bool) or isinstance(right, bool) or not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise EnglyraError("Arithmetic works with numbers only in v0.1.")
            if operator == "plus":
                return left + right
            if operator == "minus":
                return left - right
            if operator == "times":
                return left * right
            if operator == "divided by":
                if right == 0:
                    raise EnglyraError("Cannot divide by zero.")
                return left / right

        variable_key = expr.casefold()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", expr):
            if variable_key in self.variables:
                return self.variables[variable_key]
            raise EnglyraError(f"I don't know a variable named '{expr}'. Set it before using it.")

        raise EnglyraError(
            f"I can't interpret '{expr}'. Use a quoted string, a number, a known variable, "
            "or one basic operation (for example: 6 times 7)."
        )

    def run_line(self, raw_line: str) -> None:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            return

        match = re.fullmatch(r"let\s+([A-Za-z_][A-Za-z0-9_]*)\s+be\s+(.+)", line, re.IGNORECASE)
        if not match:
            match = re.fullmatch(r"set\s+([A-Za-z_][A-Za-z0-9_]*)\s+to\s+(.+)", line, re.IGNORECASE)
        if match:
            name, expression = match.groups()
            self.variables[name.casefold()] = self.evaluate(expression)
            return

        match = re.fullmatch(r"(?:say|show|print)\s+(.+)", line, re.IGNORECASE)
        if match:
            self.output(str(self.evaluate(match.group(1))))
            return

        raise EnglyraError(
            "Unknown instruction. Try 'Let name be \"Ada\"', 'Set count to 3', "
            "'Say \"Hello\"', or 'Show name'."
        )

    def run(self, source: str) -> None:
        for line_number, line in enumerate(source.splitlines(), start=1):
            try:
                self.run_line(line)
            except EnglyraError as exc:
                raise EnglyraError(f"Line {line_number}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a small Englyra v0.1 program.")
    parser.add_argument("file", type=Path, help="Path to an .eng source file")
    args = parser.parse_args(argv)

    try:
        source = args.file.read_text(encoding="utf-8")
        Runtime.create().run(source)
    except OSError as exc:
        print(f"englyra: cannot read '{args.file}': {exc}", file=sys.stderr)
        return 2
    except EnglyraError as exc:
        print(f"englyra: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
