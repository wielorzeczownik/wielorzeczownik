# neocard

`neocard` is the generator behind the card on the profile page. It reads a
GitHub account through the GitHub API and renders a neofetch-style SVG in a dark
and a light variant. A [scheduled workflow](../.github/workflows/neofetch.yml)
runs it daily and publishes the result to the `output-neofetch` branch, which
the profile [README.md](../README.md) embeds.

Nothing about a person is hardcoded – it is all passed on the command line, so
the generator is reusable as-is.

## Usage

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements_prod.txt
python -m neocard --output-dir dist --user <your-username>
```

This writes `dist/neofetch-dark.svg` and `dist/neofetch-light.svg`.

## Environment

| Variable                  | Required | Default           | Meaning                                                                         |
| ------------------------- | -------- | ----------------- | ------------------------------------------------------------------------------- |
| `GH_TOKEN`                | no       | _unset_           | GitHub token used to raise the anonymous rate limit. Needs no scopes.           |
| `GITHUB_TOKEN`            | no       | _unset_           | Same, checked after `GH_TOKEN`. Set automatically inside GitHub Actions.        |
| `GITHUB_REPOSITORY_OWNER` | no       | `wielorzeczownik` | Account to render when `--user` is not given. Set automatically inside Actions. |

Without a token the GitHub API allows 60 requests per hour, which is enough for
one run but not for repeated local iteration.

## Options

| Flag                    | Default                                              | Meaning                                                                          |
| ----------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| `-u`, `--user`          | `GITHUB_REPOSITORY_OWNER`, else `wielorzeczownik`    | Account to render.                                                               |
| `-t`, `--token`         | `GH_TOKEN`, else `GITHUB_TOKEN`, else anonymous      | GitHub token. Prefer the environment variable — an argument is visible in `ps`.  |
| `-o`, `--output-dir`    | current directory                                    | Directory to write `neofetch-dark.svg` and `neofetch-light.svg` into.            |
| `--sections`            | `identity,system,languages,hobbies,stats`            | Sections to render, in order.                                                    |
| `--fields`              | `uptime,host,kernel,website,socials`                 | API-sourced identity rows to show, in order.                                     |
| `--stats`               | `repos,stars,followers,following,commits,prs,issues` | Stats to show, in order.                                                         |
| `--frameworks`          | row omitted                                          | Free text for the `Frameworks` row.                                              |
| `--real`                | row omitted                                          | Free text for the `Real` (spoken languages) row.                                 |
| `--hobbies-software`    | row omitted                                          | Free text for the `Software` row.                                                |
| `--hobbies-hardware`    | row omitted                                          | Free text for the `Hardware` row.                                                |
| `--system LABEL=VALUE`  | section empty                                        | One line of the System section. Repeatable.                                      |
| `--social PROVIDER=URL` | API accounts only                                    | Extra socials bar entry, appended to the linked accounts. Repeatable.            |
| `--icon LABEL=GLYPH`    | built-in icon set                                    | Override a row's Nerd Font icon, as a literal glyph or `U+F108`. Repeatable.     |
| `--language-sort`       | `size`                                               | `size` orders by bytes, `name` alphabetically. Applies to the lists and the bar. |
| `--programming-limit`   | `4`                                                  | Programming languages listed.                                                    |
| `--markup-limit`        | `4`                                                  | Markup languages listed.                                                         |
| `--bar-top`             | `6`                                                  | Languages in the usage bar; the rest collapse into `Other`. `0` hides the bar.   |

Rows sourced from the API (`uptime`, `host`, `kernel`, `website`) have no
override – they are whatever the account says.

`socials` is not a key/value row but a bar of the profile's linked social
accounts, laid out like the GitHub Stats rows and wrapping every three
entries. It renders an icon plus the handle the link ends in; the accounts
come from GitHub's own settings, so adding one there is enough.

`--social` is the one exception to API rows having no override – it appends
entries GitHub cannot store, and a URL already linked on the profile is not
repeated:

```sh
neocard --social "discord=https://discord.gg/xyz" --icon "discord=U+F066F"
```

`--icon` is keyed by the provider slug for these, so `--icon "twitter=U+F31A"`
swaps the bird for the X glyph. A provider without a built-in icon falls back
to a link glyph. Dropping `socials` from `--fields` hides the bar entirely,
including the `--social` entries.

## Where the card's content lives

The values that make the published card personal are the arguments in
[.github/workflows/neofetch.yml](../.github/workflows/neofetch.yml). Changing
what the card says is a workflow edit, not a code edit.

## See also

- [CONTRIBUTING.md](../CONTRIBUTING.md) – development setup and every check
- [SECURITY.md](../SECURITY.md) – how to report a vulnerability
