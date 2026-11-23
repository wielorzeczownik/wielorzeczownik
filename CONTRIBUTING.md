# Contributing

This repo holds `neocard`, the generator behind the profile card. What it does
and every flag are in [docs/neocard.md](docs/neocard.md). What the card says
lives in [.github/workflows/neofetch.yml](.github/workflows/neofetch.yml), so
changing the content is a workflow edit, not a code edit.

## Setup

```bash
git clone https://github.com/wielorzeczownik/wielorzeczownik.git
cd wielorzeczownik
uv sync
uv run python -m neocard --output-dir dist
```

Without a token the GitHub API allows 60 requests per hour. Export `GH_TOKEN`
with a token that has no scopes to get more.

## Checks

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy neocard tests
uv run pytest
actionlint
markdownlint-cli2 "**/*.md"
npx prettier --check .
```

CI runs the same set and installs with `uv sync --locked`, so `uv.lock` has to
match `pyproject.toml`. Add dependencies with `uv add` (or `uv add --group dev`
for tooling).

## Tests

Tests live in [tests/](tests/), one module per source module. A bug fix should
come with a test that fails without it. Assert properties, not SVG markup:
"the segments sum to the bar width" holds, the exact output doesn't. Anything
touching the token checks that the token never shows up in output.

## Commits

[Conventional Commits](https://www.conventionalcommits.org/), e.g.
`fix(languages): count vendored files`. Scope is the area, not the file.

Security issues go through [SECURITY.md](SECURITY.md), not public issues.
