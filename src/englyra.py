#!/usr/bin/env python3
"""A small, dependency-free interpreter for the Englyra language prototype."""
from __future__ import annotations
import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

MAX_REPEAT_COUNT = 10_000

class EnglyraError(Exception):
    """Raised when an Englyra program cannot be parsed or executed."""

@dataclass(frozen=True)
class Statement:
    kind: str
    line: int
    text: str = ""
    condition: str = ""
    body: tuple["Statement", ...] = ()
    otherwise_body: tuple["Statement", ...] = ()

class Parser:
    """Parses indentation-independent, explicitly terminated Englyra blocks."""
    def __init__(self, source: str):
        self.lines = source.splitlines()
        self.index = 0

    @staticmethod
    def _marker(line: str) -> str | None:
        normalized = re.sub(r"\s+", " ", line.strip()).casefold()
        if normalized == "otherwise":
            return "OTHERWISE"
        if normalized == "end if":
            return "END_IF"
        if normalized == "end repeat":
            return "END_REPEAT"
        return None

    def parse(self) -> tuple[Statement, ...]:
        statements, marker = self._parse_block(set())
        if marker is not None:
            raise EnglyraError(f"Line {self.index}: Unexpected '{marker.replace('_', ' ').title()}'.")
        return tuple(statements)

    def _parse_block(self, stop_markers: set[str]) -> tuple[list[Statement], str | None]:
        statements: list[Statement] = []
        while self.index < len(self.lines):
            line_number = self.index + 1
            raw = self.lines[self.index]
            self.index += 1
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            marker = self._marker(line)
            if marker:
                if marker in stop_markers:
                    return statements, marker
                label = marker.replace("_", " ").title()
                raise EnglyraError(f"Line {line_number}: Unexpected '{label}'.")
            if re.match(r"^if\b", line, re.IGNORECASE):
                condition = re.sub(r"^if\s+", "", line, flags=re.IGNORECASE).strip()
                if not condition:
                    raise EnglyraError(f"Line {line_number}: Add a condition after 'If'.")
                body, end_marker = self._parse_block({"OTHERWISE", "END_IF"})
                otherwise_body: list[Statement] = []
                if end_marker == "OTHERWISE":
                    otherwise_body, end_marker = self._parse_block({"END_IF"})
                if end_marker != "END_IF":
                    raise EnglyraError(f"Line {line_number}: This If block needs an 'End If'.")
                statements.append(Statement("if", line_number, condition=condition,
                                            body=tuple(body), otherwise_body=tuple(otherwise_body)))
                continue
            repeat_match = re.fullmatch(r"repeat\s+(.+?)\s+times", line, re.IGNORECASE)
            if repeat_match:
                count_expression = repeat_match.group(1).strip()
                if not count_expression:
                    raise EnglyraError(f"Line {line_number}: Add a count before 'times'.")
                body, end_marker = self._parse_block({"END_REPEAT"})
                if end_marker != "END_REPEAT":
                    raise EnglyraError(f"Line {line_number}: This Repeat block needs an 'End Repeat'.")
                statements.append(Statement("repeat", line_number, text=count_expression, body=tuple(body)))
                continue
            if re.match(r"^(?:end\b|otherwise\b|repeat\b)", line, re.IGNORECASE):
                raise EnglyraError(f"Line {line_number}: Unrecognized block instruction '{line}'.")
            if not self._is_simple_statement(line):
                raise EnglyraError(
                    f"Line {line_number}: Unknown instruction. Try 'Let name be 3', "
                    "'Say \"Hello\"', 'If score is at least 10', or 'Repeat 3 times'."
                )
            statements.append(Statement("line", line_number, text=line))
        return statements, None

    @staticmethod
    def _is_simple_statement(line: str) -> bool:
        assignment = r"(?:let\s+[A-Za-z_][A-Za-z0-9_]*\s+be|set\s+[A-Za-z_][A-Za-z0-9_]*\s+to)\s+.+"
        output = r"(?:say|show|print)\s+.+"
        return bool(re.fullmatch(assignment, line, re.IGNORECASE) or
                    re.fullmatch(output, line, re.IGNORECASE))

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
        arithmetic = re.compile(r"^(.+?)\s+(divided by|plus|minus|times)\s+(.+)$", re.IGNORECASE)
        match = arithmetic.match(expr)
        if match:
            left = self.evaluate(match.group(1))
            operator = match.group(2).casefold()
            right = self.evaluate(match.group(3))
            if (isinstance(left, bool) or isinstance(right, bool) or
                    not isinstance(left, (int, float)) or not isinstance(right, (int, float))):
                raise EnglyraError("Arithmetic works with numbers only.")
            if operator == "plus":
                return left + right
            if operator == "minus":
                return left - right
            if operator == "times":
                return left * right
            if right == 0:
                raise EnglyraError("Cannot divide by zero.")
            return left / right
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", expr):
            key = expr.casefold()
            if key in self.variables:
                return self.variables[key]
            raise EnglyraError(f"I don't know a variable named '{expr}'. Set it before using it.")
        raise EnglyraError(
            f"I can't interpret '{expr}'. Use quoted text, a number, a known variable, "
            "or one basic arithmetic operation."
        )

    def evaluate_condition(self, condition: str) -> bool:
        comparison = re.compile(
            r"^(.+?)\s+(is not equal to|is greater than or equal to|is less than or equal to|"
            r"is equal to|is greater than|is less than|is at least|is at most|equals)\s+(.+)$",
            re.IGNORECASE,
        )
        match = comparison.match(condition.strip())
        if not match:
            raise EnglyraError(
                "I couldn't read that condition. Use 'is equal to', 'is not equal to', "
                "'is greater than', 'is less than', 'is at least', or 'is at most'."
            )
        left = self.evaluate(match.group(1))
        operator = match.group(2).casefold()
        right = self.evaluate(match.group(3))
        if operator in {"is equal to", "equals"}:
            return left == right
        if operator == "is not equal to":
            return left != right
        if (isinstance(left, bool) or isinstance(right, bool) or
                not isinstance(left, (int, float)) or not isinstance(right, (int, float))):
            raise EnglyraError("Greater-than and less-than comparisons require numbers.")
        if operator in {"is greater than", "is greater than or equal to"}:
            return left > right if operator == "is greater than" else left >= right
        if operator in {"is less than", "is less than or equal to"}:
            return left < right if operator == "is less than" else left <= right
        if operator == "is at least":
            return left >= right
        return left <= right

    def _run_simple_line(self, raw_line: str) -> None:
        line = raw_line.strip()
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
        raise EnglyraError("Unknown instruction.")

    def _execute(self, statements: tuple[Statement, ...]) -> None:
        for statement in statements:
            try:
                if statement.kind == "line":
                    self._run_simple_line(statement.text)
                elif statement.kind == "if":
                    selected = statement.body if self.evaluate_condition(statement.condition) else statement.otherwise_body
                    self._execute(selected)
                elif statement.kind == "repeat":
                    count = self.evaluate(statement.text)
                    if isinstance(count, bool) or not isinstance(count, int):
                        raise EnglyraError("Repeat count must be a whole number.")
                    if count < 0:
                        raise EnglyraError("Repeat count cannot be negative.")
                    if count > MAX_REPEAT_COUNT:
                        raise EnglyraError(f"Repeat count cannot be greater than {MAX_REPEAT_COUNT}.")
                    for _ in range(count):
                        self._execute(statement.body)
            except EnglyraError as exc:
                raise EnglyraError(f"Line {statement.line}: {exc}") from exc

    def run(self, source: str) -> None:
        program = Parser(source).parse()
        self._execute(program)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an Englyra source file.")
    parser.add_argument("file", type=Path, help="Path to an .eng source file")
    args = parser.parse_args(argv)
    try:
        Runtime.create().run(args.file.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"englyra: cannot read '{args.file}': {exc}", file=sys.stderr)
        return 2
    except EnglyraError as exc:
        print(f"englyra: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
