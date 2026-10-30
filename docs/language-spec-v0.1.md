# Englyra Language Sketch — v0.1

This document defines the first prototype's supported syntax. It is intentionally small so behavior can be tested and explained.

## Source format

- UTF-8 plain text with the `.eng` extension.
- One instruction per line.
- Blank lines are ignored.
- A line whose first non-space character is `#` is a comment.
- Commands and variable names are case-insensitive in v0.1.

## Statements

### Assign a value

```text
Let name be "Ada"
Set score to 42
```

`Let name be <expression>` and `Set name to <expression>` create or replace a variable.

### Display a value

```text
Say "Hello, world!"
Show name
Print score
```

`Say`, `Show`, and `Print` evaluate the expression and write its string form followed by a newline.

## Values and expressions

Supported values:

- Double-quoted text, using JSON string escaping, e.g. `"a quote: \\x22"`.
- Integers, e.g. `42` or `-3`.
- Decimal numbers, e.g. `3.14`.
- A previously assigned variable name.

Supported arithmetic operators are words: `plus`, `minus`, `times`, and `divided by`. Arithmetic requires numeric values. Division by zero is an error. The current prototype is intended for simple examples and does not yet specify conventional operator precedence or parentheses; use one operation per expression.

## Errors

An invalid statement or value stops execution and returns an error with its source line number. Unknown variables, invalid quoted strings, arithmetic on text, and division by zero are reported rather than guessed.

## Explicit non-goals for v0.1

The prototype does not translate unrestricted natural language, run arbitrary shell commands, access the network, read or write arbitrary files from program code, import packages, or support loops, conditionals, functions, classes, or user-defined modules.

## Open design questions

1. Which English phrases are most intuitive without becoming ambiguous?
2. Should types be inferred, declared, or both?
3. How should blocks (conditions and repeat loops) be delimited?
4. How should Englyra explain errors to brand-new programmers?
5. Should the language eventually compile to bytecode, transpile, or remain interpreted?
