# Contributing to Englyra

Thanks for helping explore a more approachable programming language.

## Before proposing syntax

1. Describe the beginner problem the instruction solves.
2. Show a small .eng example.
3. Explain how unclear or edge-case inputs should behave.
4. Update the current language specification and add tests with any implementation change.
5. Keep the VS Code grammar and snippets in sync when adding syntax.

## Local development

Requirements: Python 3.10+.

    python -m unittest discover -s tests -v
    python src/englyra.py examples/hello.eng
    python src/englyra.py examples/decisions.eng
    python src/englyra.py examples/repeat.eng

## Principles

- Prefer explicit, deterministic syntax over guessing at arbitrary English.
- Keep the prototype dependency-free where practical.
- Never use eval, unrestricted shell execution, or hidden side effects to interpret source code.
- Add tests for successful behavior and meaningful errors.
- Keep documentation, examples, and the VS Code grammar aligned with the implementation.
