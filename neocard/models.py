from __future__ import annotations

from dataclasses import dataclass, field


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
    created_at: str
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
    lang_bytes: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class Settings:
    """User-tunable content and parameters"""

    manual: dict[str, str] = field(default_factory=dict)
    jokes: dict[str, str] = field(default_factory=dict)
    icons: dict[str, str] = field(default_factory=dict)
    sections: list[str] = field(default_factory=list)
    fields: list[str] = field(default_factory=list)
    stats: list[str] = field(default_factory=list)
    language_sort: str = "size"
    programming_limit: int = 4
    markup_limit: int = 4
    bar_top: int = 6
