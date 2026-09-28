# Contributing to tino

Thank you for helping. Field reports from real projects are the most
valuable contribution: most of tino's rules come from mistakes observed in
use.

## Field reports

Open an issue with the **Field report** template: what you asked, what the
agent did, what you expected, and the tino version (the marker in your
instructions file, for example `<!-- tino: continuity v2.0 -->`). Paste
excerpts, never secrets or personal data.

## Changes

- Every change brings its test: a case in `tests/test_suite.py` that fails
  without the change and passes with it. The bench uses only the Python
  standard library (3.8 or later).
- The fixed tokens in [`docs/format.md`](docs/format.md) are a public
  contract: the scripts and existing projects depend on them. Adding an
  alias is fine; renaming or removing a token is a breaking change.
- English is the source language. Installed files are written in the
  project's language, with the English or the Spanish token set.
- Keep each instructions block within its cap (20, 15 and 15 lines): blocks
  are paid in every session of every project that uses them.

Before opening a pull request:

```bash
python3 tests/test_suite.py
claude plugin validate --strict ./plugins/tino
```

Changes to how an installer or a ritual behaves should also pass the eval
suite in `plugins/tino/evals/`, run from a clone of the repository (the
cases seed their projects from `tests/fixtures/`). It runs real agent
sessions on your own account, and by default publishes its report privately to your claude.ai
account (add `--no-publish` to keep it local):

```bash
claude plugin eval ./plugins/tino --scaffold --allow-tools Bash Write Edit
```

## License of contributions

By contributing you agree that your contribution is licensed like the rest
of the repository: MIT for code and skills, CC BY 4.0 for the documentation
in `docs/`.
