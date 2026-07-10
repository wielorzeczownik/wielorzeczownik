from __future__ import annotations

import os
import urllib.request

from github import Auth, Github
from github.GithubException import GithubException

from .models import Profile

_TIMEOUT = 30
_CREATED_AT_FMT = "%Y-%m-%dT%H:%M:%SZ"


class GitHubClient:
    """GitHub data source backed by PyGithub"""

    def __init__(self, user: str, token: str | None = None) -> None:
        self.user = user
        resolved = (
            token
            or os.environ.get("GH_TOKEN")
            or os.environ.get("GITHUB_TOKEN")
        )
        auth = Auth.Token(resolved) if resolved else None
        self.gh = Github(auth=auth)

    @staticmethod
    def _download(url: str) -> bytes:
        request = urllib.request.Request(url, headers={"User-Agent": "neocard"})
        with urllib.request.urlopen(request, timeout=_TIMEOUT) as response:
            data: bytes = response.read()
            return data

    def _search_count(self, query: str) -> int:
        try:
            return self.gh.search_issues(query=query).totalCount
        except GithubException:  # rate limit / transient API failure
            return 0

    def fetch_profile(self) -> Profile:
        """Gather everything the card needs from the GitHub API."""
        user = self.gh.get_user(self.user)
        repos = [repo for repo in user.get_repos() if not repo.fork]
        lang_bytes: dict[str, int] = {}
        for repo in repos:
            for name, size in repo.get_languages().items():
                if name == "url":  # PyGithub injects the endpoint URL as a key
                    continue
                lang_bytes[name] = lang_bytes.get(name, 0) + int(size)
        try:
            commits = self.gh.search_commits(
                query=f"author:{self.user}"
            ).totalCount
        except GithubException:
            commits = 0
        return Profile(
            user=self.user,
            created_at=user.created_at.strftime(_CREATED_AT_FMT),
            public_repos=user.public_repos,
            followers=user.followers,
            following=user.following,
            stars=sum(repo.stargazers_count for repo in repos),
            commits=commits,
            prs=self._search_count(f"author:{self.user} type:pr"),
            issues=self._search_count(f"author:{self.user} type:issue"),
            avatar=self._download(user.avatar_url),
            company=(user.company or "").lstrip("@") or None,
            bio=user.bio or None,
            blog=user.blog or None,
            lang_bytes=lang_bytes,
        )
