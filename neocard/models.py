from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class Theme:
    """A color scheme for one rendering"""

    name: str
    bg: str
    fg: str
    cc: str  # muted comment color for dots and separators
    key: str
    value: str
    v_floor: float  # language/text color lightness clamp
    v_ceil: float
    px_floor: float  # avatar pixel lightness clamp
    px_ceil: float
    sat: float  # saturation multiplier


@dataclass(frozen=True)
class Profile:
    """Everything pulled from the GitHub API for a single user"""

    user: str
    created_at: datetime
    public_repos: int
    followers: int
    following: int
    stars: int
    commits: int
    prs: int
    issues: int
    avatar: bytes
    company: str | None = None
    bio: str | None = None
    blog: str | None = None
    socials: tuple[tuple[str, str], ...] = ()
    lang_bytes: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class Settings:
    """User-tunable content and parameters."""

    manual: dict[str, str]
    jokes: dict[str, str]
    socials: tuple[tuple[str, str], ...]
    icons: dict[str, str]
    sections: list[str]
    fields: list[str]
    stats: list[str]
    language_sort: str
    programming_limit: int
    markup_limit: int
    bar_top: int
