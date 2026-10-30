# Contributing to Englyra

Thanks for helping explore a more approachable programming language.

## Before proposing syntax

1. Describe the beginner problem the instruction solves.
2. Show a small `.eng` example.
3. Explain how unclear or edge-case inputs should behave.
4. Update the language sketch and add tests with any implementation change.

## Local development

Requirements: Python 3.10+.

```bash
python -m unittest discover -s tests -v
python src/englyra.py examples/hello.eng
python src/englyra.py examples/calculator.eng
```

## Principles

- Prefer explicit, deterministic syntax over guessing at arbitrary English.
- Keep the prototype dependency-free where practical.
- Never use `eval`, unrestricted shell execution, or hidden side effects to interpret source code.
- Add tests for successful behavior and meaningful errors.
- Keep documentation and examples aligned with the implementation.
