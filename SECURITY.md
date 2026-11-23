# Security

Thanks for taking the time to look. Please report vulnerabilities privately
through
[GitHub Security Advisories](https://github.com/wielorzeczownik/wielorzeczownik/security/advisories/new)
instead of a public issue, so there's a chance to fix them first. You'll be
credited unless you'd rather not be. There are no releases, only `main` gets
fixes.

## In scope

- the GitHub token read from `--token`, `GH_TOKEN` or `GITHUB_TOKEN`
- the two network reads: the GitHub API, and the avatar URL it returns
- the workflow that publishes the cards to the `output-neofetch` branch

Problems in the GitHub API itself are out of scope. So is the content of the
card, which is public by construction.

## If you reuse the generator

- The token needs no scopes. It only raises the anonymous rate limit above 60
  requests per hour, so grant it nothing.
- Don't pass it with `--token` on a shared machine, because arguments show up
  in the process list. Use `GH_TOKEN`.
- The SVG embeds the account's avatar and public profile fields. Don't point it
  at an account whose profile you don't want on a public branch.
