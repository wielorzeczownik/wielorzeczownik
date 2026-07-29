from __future__ import annotations

import pytest

from neocard.github import GitHubClient, resolve_token

SENTINEL = "ghp_notarealvaluebutlongenoughtolookreal"


@pytest.mark.parametrize(
    ("explicit", "env", "expected"),
    [
        (SENTINEL, {}, SENTINEL),
        (SENTINEL, {"GH_TOKEN": "env", "GITHUB_TOKEN": "env"}, SENTINEL),
        (None, {"GH_TOKEN": "gh", "GITHUB_TOKEN": "actions"}, "gh"),
        (None, {"GITHUB_TOKEN": "actions"}, "actions"),
        (None, {}, None),
        (None, {"GH_TOKEN": ""}, None),
        ("", {"GH_TOKEN": "gh"}, "gh"),
    ],
)
def test_resolve_token_prefers_the_explicit_value_then_gh_token(
    explicit: str | None, env: dict[str, str], expected: str | None
) -> None:
    assert resolve_token(explicit, env) == expected


def test_client_repr_does_not_leak_the_secret() -> None:
    """One stray log line of a client must not become a credential leak."""
    client = GitHubClient("wielorzeczownik", SENTINEL)
    assert SENTINEL not in repr(client)
    assert "wielorzeczownik" in repr(client)


def test_client_never_stores_the_secret_on_the_instance() -> None:
    """Nothing downstream can print what the object does not hold."""
    client = GitHubClient("wielorzeczownik", SENTINEL)
    assert SENTINEL not in str(vars(client))


def test_client_reports_whether_it_found_a_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    assert GitHubClient("wielorzeczownik", SENTINEL).authenticated
    assert not GitHubClient("wielorzeczownik", "").authenticated
