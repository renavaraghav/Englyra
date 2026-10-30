# Englyra Language Support for Visual Studio Code

This small extension adds .eng file recognition, syntax highlighting, comment support, block folding, and starter snippets. It does not bundle the Python interpreter or run Englyra programs from VS Code yet.

## Try it locally

1. Open this vscode-englyra folder in Visual Studio Code.
2. Press F5 to launch an Extension Development Host window.
3. Create or open a file ending in .eng.
4. Type ifelse, repeat, hello, or let and press Tab to insert a snippet.

For a packaged extension, install the VS Code Extension Manager (vsce) and run vsce package from this directory. The generated .vsix can be installed with Extensions: Install from VSIX...

## Current scope

- Language identifier: englyra
- File extension: .eng
- Syntax scopes for comments, strings, numbers, statements, block instructions, comparisons, and arithmetic words
- Snippets for hello world, assignments, conditional blocks, and repeat blocks

Execution, diagnostics, autocomplete, and a debugger are future work. Run programs with the repository's Python prototype for now:

    python src/englyra.py examples/decisions.eng
