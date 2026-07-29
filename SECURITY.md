# Security Policy

## Supported versions

This repository has no releases. Only the current `main` branch is supported.

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities privately via
[GitHub Security Advisories](https://github.com/wielorzeczownik/wielorzeczownik/security/advisories/new).

Include as much detail as possible:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You will receive a response within **7 days**. If the issue is confirmed, a fix
will be pushed as soon as possible and you will be credited (unless you prefer
to remain anonymous).

## Scope

`neocard` is a command-line generator that runs in GitHub Actions. The attack
surface is small and consists of:

- handling of the GitHub token read from `--token`, `GH_TOKEN` or
  `GITHUB_TOKEN`
- the two network reads it performs: the GitHub API, and the avatar URL that
  the API returns
- the workflow that publishes the rendered cards to the `output-neofetch`
  branch

Vulnerabilities in the GitHub API itself are out of scope. So is the content of
the generated card, which is public information by construction.

## Notes for anyone reusing this generator

- The token needs no scopes. It is used only to raise the anonymous rate limit
  above 60 requests per hour, so grant it nothing.
- Never pass a token via `--token` on a shared machine; the argument is visible
  in the process list. Use `GH_TOKEN` instead.
- The rendered SVG embeds the account's avatar and public profile fields. Do
  not point the generator at an account whose profile you do not want published
  to a public branch.
