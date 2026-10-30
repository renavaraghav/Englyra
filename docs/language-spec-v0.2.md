# Englyra Language Specification — v0.2

This release extends v0.1 with explicit conditional blocks and counted repeat blocks. Indentation is for readability; block boundaries are determined by the closing instructions.

## Source format

- UTF-8 text files use the .eng extension.
- Blank lines are ignored. A line whose first non-space character is # is a comment.
- Command words and variable names are case-insensitive. String values remain case-sensitive.
- Indentation is optional, but two spaces per block level are recommended.

## Values and assignments

    Let name be "Ada"
    Set score to 42

Values are double-quoted strings, integers, decimal numbers, or previously assigned variable names. Arithmetic supports plus, minus, times, and divided by. Arithmetic requires numbers; division by zero is an error.

## Output

    Say "Hello"
    Show name
    Print score

Each output statement writes one line.

## Conditions

An If statement starts a block. Otherwise is optional and may appear once. Every conditional block must end with End If.

    If score is at least 50
      Say "pass"
    Otherwise
      Say "try again"
    End If

Supported comparison phrases:

- is equal to or equals
- is not equal to
- is greater than
- is less than
- is at least (greater than or equal to)
- is at most (less than or equal to)
- is greater than or equal to
- is less than or equal to

Equality works with matching value types. Greater-than and less-than comparisons require numbers. Conditions currently contain one comparison; logical combinations such as and / or are not part of v0.2.

## Counted repeat blocks

    Repeat 3 times
      Say "hello"
    End Repeat

The count may be an integer literal or a variable containing an integer. Zero is allowed; negative, decimal, and non-numeric counts are rejected. A single repeat block is limited to 10,000 iterations to prevent accidental runaway work. Repeat blocks can be nested and can contain If blocks.

## Block rules

- Every If requires exactly one matching End If.
- Every Repeat requires one matching End Repeat.
- Otherwise belongs only inside an If block and may occur at most once.
- Blocks may be nested. Their closing words must match their opening instruction.
- A malformed instruction is reported with its source line number, even if it appears in a branch that would not run.

## Safety and non-goals

Englyra v0.2 remains a small interpreted language. It does not execute arbitrary English, shell commands, imported modules, network requests, or arbitrary file operations. It has no while loop, functions, user-defined types, or and / or condition composition yet. New capabilities should be explicit, documented, bounded where appropriate, and covered by tests.
