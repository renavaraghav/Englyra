<div align="center">

# Englyra

### Write software in language that feels like English.

**An English-first programming language experiment** — designed to make programming more approachable without giving up clarity, predictable behavior, or safety.

[![Status](https://img.shields.io/badge/status-early%20prototype-f5b6c8?style=for-the-badge)](#project-status)
[![Python](https://img.shields.io/badge/prototype-Python%203.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-8b7cff?style=for-the-badge)](LICENSE)

*Less syntax to memorize. More ideas to bring to life.*

</div>

---

## What is Englyra?

Englyra explores a simple question: **what if writing a small program felt closer to giving clear instructions in English?**

    Let name be "world"
    Say "Hello, "
    Say name

    Let answer be 6 times 7
    Show answer

The goal is not to pretend that a computer can safely execute every free-form sentence. Englyra uses a readable, deliberately defined English-like syntax that people can learn quickly and that a computer can interpret consistently.

## Why this project?

- **Approachable:** reduce the amount of punctuation and syntax beginners have to learn first.
- **Readable:** programs should communicate intent to people, not just to a compiler.
- **Predictable:** instructions have explicit meanings and understandable errors.
- **Safe by design:** the language should never silently execute arbitrary system commands just because a sentence sounds like an instruction.
- **Extensible:** start with a small core and expand only when a feature can be specified and tested well.

## Try the prototype

Requires Python 3.10 or newer. No third-party packages are needed.

    python src/englyra.py examples/hello.eng
    python src/englyra.py examples/calculator.eng
    python src/englyra.py examples/decisions.eng
    python src/englyra.py examples/repeat.eng
    python src/englyra.py examples/control-flow.eng

Run the tests:

    python -m unittest discover -s tests -v

## Language examples

### Variables and output

    Let name be "Ada"
    Say "Hello, "
    Show name

### Conditions

    Let score be 82

    If score is at least 50
      Say "You passed!"
    Otherwise
      Say "Try again — you can do it."
    End If

### Counted loops

    Let counter be 0

    Repeat 3 times
      Set counter to counter plus 1
      Say counter
    End Repeat

### Current syntax

| Instruction | Meaning |
| --- | --- |
| Let name be "Ada" | Store a text value in a variable |
| Set score to 42 | Assign a value to a variable |
| Say "Hello" / Show name | Display text or a value |
| Let answer be 6 times 7 | Evaluate a basic arithmetic expression |
| If score is at least 50 | Start a conditional block |
| Otherwise / End If | Select the alternative branch and close the condition |
| Repeat 3 times / End Repeat | Repeat a block a fixed number of times |

See [docs/language-spec-v0.2.md](docs/language-spec-v0.2.md) for the current syntax and [docs/language-spec-v0.1.md](docs/language-spec-v0.1.md) for the original prototype.

## Visual Studio Code support

An initial extension lives in [editors/vscode-englyra](editors/vscode-englyra). It recognizes .eng files and provides syntax highlighting, block folding, comment handling, and starter snippets. Open that folder in VS Code and press F5 to try it in an Extension Development Host. It does not execute programs from the editor yet; use the Python command above to run them.

## Project status

Englyra is in the **idea-to-prototype stage**. The interpreter supports assignments, text/numeric values, basic arithmetic, output, nested If / Otherwise blocks, and bounded counted Repeat blocks. It does not yet support while loops, functions, external libraries, or arbitrary natural-language instructions.

## Roadmap

- [x] Define a small, explicit English-like syntax
- [x] Build a dependency-free interpreter prototype
- [x] Add runnable examples and automated tests
- [x] Specify conditionals and counted repeat blocks
- [x] Add initial VS Code .eng language support, syntax highlighting, and snippets
- [ ] Gather beginner feedback on readability and errors
- [ ] Add while loops, functions, and carefully scoped capabilities
- [ ] Add a formatter, autocomplete, richer diagnostics, and execution support in VS Code
- [ ] Evaluate whether to keep interpreting source or add a compilation stage

## Design principles

1. **Human-readable, not ambiguous:** when an instruction could mean two things, ask for explicit syntax rather than guessing.
2. **Errors should teach:** report the line and explain what Englyra expected.
3. **No hidden execution:** file, network, and system operations will need explicit capabilities and safety boundaries.
4. **Test every feature:** new syntax should come with examples, specification updates, and automated tests.

## Contributing

Ideas and constructive feedback are welcome. Before proposing a new instruction, describe the problem it solves, show a short example program, and explain how ambiguous cases should behave. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

<div align="center">

**Englyra — clear instructions, real programs.** ✨

</div>
