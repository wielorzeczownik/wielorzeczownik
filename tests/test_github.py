from __future__ import annotations

from typing import Any

import pytest
from github.GithubException import GithubException

from neocard.github import GitHubClient, resolve_token

SENTINEL = "ghp_notarealvaluebutlongenoughtolookreal"


def _client_returning(payload: object) -> GitHubClient:
    """A client whose social-accounts route answers with payload."""
    client = GitHubClient("wielorzeczownik", SENTINEL)

    def fake(*_args: Any, **_kwargs: Any) -> tuple[dict[str, str], object]:
        if isinstance(payload, Exception):
            raise payload
        return {}, payload

    client.gh.requester.requestJsonAndCheck = fake  # type: ignore[method-assign]
    return client


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


def test_social_accounts_are_kept_in_profile_order() -> None:
    client = _client_returning(
        [
            {"provider": "twitter", "url": "https://twitter.com/nick"},
            {"provider": "youtube", "url": "https://youtube.com/@nick"},
        ]
    )
    assert client._social_accounts() == (  # noqa: SLF001
        ("twitter", "https://twitter.com/nick"),
        ("youtube", "https://youtube.com/@nick"),
    )


def test_social_accounts_tolerate_a_missing_provider_or_url() -> None:
    """A tuple, not a dict: "generic" repeats once per plain URL."""
    client = _client_returning(
        [
            {"url": "https://furryunicorn.com"},
            {"provider": "generic", "url": "https://example.com"},
            {"provider": "twitter"},
        ]
    )
    assert client._social_accounts() == (  # noqa: SLF001
        ("generic", "https://furryunicorn.com"),
        ("generic", "https://example.com"),
    )


def test_social_accounts_survive_a_rate_limited_api() -> None:
    """The card must still render when this one extra call is refused."""
    client = _client_returning(GithubException(403, "rate limited", None))
    assert client._social_accounts() == ()  # noqa: SLF001
