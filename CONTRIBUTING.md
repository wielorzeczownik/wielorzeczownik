# Contributing to neocard

Thank you for considering a contribution. This document covers everything you
need to get started.

## Overview

`neocard` is the generator behind this profile's card. It reads a GitHub
account through the GitHub API and renders a neofetch-style SVG in a light and
a dark variant. A scheduled workflow runs it daily and publishes the result to
the `output-neofetch` branch, which the profile `README.md` embeds.

The profile `README.md` deliberately contains nothing but the card. What the
tool does, every environment variable and every flag are documented in
[docs/neocard.md](docs/neocard.md).

## Project structure

```text
.
├── neocard/
│   ├── __main__.py     module entry point (python -m neocard)
│   ├── cli.py          argument parsing and the run sequence
│   ├── config.py       defaults used when a flag is omitted
│   ├── constants.py    themes, icons, language colours, markup language set
│   ├── github.py       GitHub API client, the only network boundary
│   ├── models.py       Profile, Theme and Settings value types
│   ├── languages.py    language ranking and usage-bar segmentation
│   ├── colors.py       language colours clamped to the theme background
│   ├── avatar.py       avatar downscaling and quantisation
│   ├── time_utils.py   account-age formatting
│   ├── panel.py        text panel layout
│   ├── svg.py          SVG assembly
│   └── assets/         embedded Nerd Font subset and its OFL notice
├── docs/neocard.md     usage, environment and every CLI flag
└── tests/              pytest suite, one module per source module
```

The card content is not hardcoded: everything specific to a person lives in the
`python -m neocard` invocation inside
[.github/workflows/neofetch.yml](.github/workflows/neofetch.yml). Changing what
the card says is a workflow edit, not a code edit.

## Development setup

```bash
git clone https://github.com/wielorzeczownik/wielorzeczownik.git
cd wielorzeczownik
python3 -m venv .venv
source .venv/bin/activate
pip install --require-hashes -r requirements_dev.lock
python -m neocard --output-dir dist
```

An unauthenticated run works but is limited to 60 API requests per hour. Export
`GH_TOKEN` with a token that has no scopes to raise that limit; the tool needs
no permissions beyond reading public data.

## Running checks locally

### With tools installed locally

```bash
# Python
ruff format --check .
ruff check .
mypy neocard tests
pytest

# Dependencies
pip-audit --require-hashes -r requirements_prod.lock

# GitHub Actions workflows
actionlint

# Markdown
markdownlint-cli2 "**/*.md"

# YAML, JSON and Markdown formatting
npx prettier --check .
```

### With Docker (no local installs required)

```bash
docker run --rm -v "$(pwd):/workdir" davidanson/markdownlint-cli2 "**/*.md"

docker run --rm -v "$(pwd):/repo" -w /repo rhysd/actionlint:latest -color
```

### Refreshing the lockfiles

`requirements_*.txt` hold the direct dependencies; `requirements_*.lock` are
generated from them and pin every transitive package to an exact version and
hash. Never hand-edit a `.lock`. Regenerate all three after changing any
`requirements_*.txt`:

```bash
for tier in prod lint dev; do
  uv pip compile --generate-hashes --python-version 3.10 \
    "requirements_${tier}.txt" -o "requirements_${tier}.lock"
done
```

## Commit style

This project uses [Conventional Commits](https://www.conventionalcommits.org/):
`type(scope): imperative summary`, lower case, no trailing period.

| Prefix      | When to use                             |
| ----------- | --------------------------------------- |
| `feat:`     | New card section, flag or capability    |
| `fix:`      | Bug fix                                 |
| `perf:`     | Smaller or faster output                |
| `test:`     | Adding or updating tests                |
| `chore:`    | Maintenance, dependency updates         |
| `refactor:` | Code change without behaviour change    |
| `docs:`     | Documentation only                      |
| `style:`    | Formatting, no logic change             |
| `build:`    | Packaging, dependencies, Python version |
| `ci:`       | Workflow changes                        |

Scope names the area, not the file: `github`, `svg`, `languages`, `avatar`,
`deps`, `renovate`. Breaking changes carry `!` and a `BREAKING CHANGE:` footer.

Explain **why** in the body, not what — the diff already says what. Wrap at
72–80 columns.

## Tests

Tests live in [tests/](tests/), one module per source module, and are linted and
type-checked exactly like production code. Cover behaviour changes with tests;
a bug fix should come with a test that fails without the fix.

Prefer asserting properties over output shape: the SVG is a rendering detail,
but "the segments sum to the bar width" and "the token never appears in a
repr" are contracts. Anything touching the API token asserts that the secret
does **not** appear.

## Pull requests

- Keep pull requests focused on a single concern.
- Reference any related issue in the description.
- All CI checks must pass: Ruff, mypy, pytest, dependency audit, workflow lint,
  Markdown lint and Prettier.

## Reporting bugs

Open an [issue](https://github.com/wielorzeczownik/wielorzeczownik/issues) and
include what you ran, what you expected, what happened, and the output of
`python -m neocard --output-dir dist` if it failed.

> For security issues, please read [SECURITY.md](SECURITY.md) before opening a
> public issue.

## License

By contributing you agree that your changes will be licensed under the
[MIT License](LICENSE).
