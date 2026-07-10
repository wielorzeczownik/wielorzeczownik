from __future__ import annotations

from typing import TYPE_CHECKING

from svgwrite.text import Text, TSpan

from .colors import language_color
from .constants import (
    BAR_CELLS,
    BLOCKS_BRIGHT,
    BLOCKS_NORMAL,
    COLUMN_X,
    LEADER,
    LINE_HEIGHT,
)
from .languages import OTHER, Segment, split_languages, usage_segments
from .time_utils import account_age

if TYPE_CHECKING:
    from collections.abc import Callable

    from .models import Profile, Settings, Theme

# API identity rows: name -> (label, value getter).
_IDENTITY: dict[str, tuple[str, Callable[[Profile], object]]] = {
    "uptime": ("Uptime", lambda p: account_age(p.created_at)),
    "host": ("Host", lambda p: p.company),
    "kernel": ("Kernel", lambda p: p.bio),
    "website": (
        "Website",
        lambda p: (
            p.blog.replace("https://", "").replace("http://", "")
            if p.blog
            else None
        ),
    ),
}

# Stat rows
_STATS: dict[str, tuple[str, Callable[[Profile], int]]] = {
    "repos": ("Repos", lambda p: p.public_repos),
    "stars": ("Stars", lambda p: p.stars),
    "followers": ("Followers", lambda p: p.followers),
    "following": ("Following", lambda p: p.following),
    "commits": ("Commits", lambda p: p.commits),
    "prs": ("PRs", lambda p: p.prs),
    "issues": ("Issues", lambda p: p.issues),
}
STATS_PER_ROW = 4

Children = list[TSpan]


def _cc(text: str) -> TSpan:
    return TSpan(text, class_="cc")


def _key(text: str) -> TSpan:
    return TSpan(text, class_="key")


def _val(text: str) -> TSpan:
    return TSpan(text, class_="value")


def _colored(text: str, color: str) -> TSpan:
    return TSpan(text, fill=color)


def _icon(name: str, icons: dict[str, str]) -> Children:
    """Leading Nerd Font icon (glyph + trailing space) for a field, if any"""
    glyph = icons.get(name, "")
    return [TSpan(f"{glyph} ", class_="key")] if glyph else []


def _icon_pad(name: str, icons: dict[str, str]) -> int:
    return 2 if icons.get(name) else 0


def _dotted_key(key: str) -> Children:
    """Render Languages.Programming as colored keys joined by muted dots"""
    spans: Children = []
    for i, part in enumerate(key.split(".")):
        if i:
            spans.append(_cc("."))
        spans.append(_key(part))
    return spans


def _kv(key: str, value: Children, icons: dict[str, str]) -> Children:
    count = max(LEADER - 3 - _icon_pad(key, icons) - len(key), 1)
    leader = _cc(f" {'.' * count} ")
    return [*_icon(key, icons), *_dotted_key(key), TSpan(":"), leader, *value]


def _section(title: str) -> Children:
    dashes = "—" * (56 - len(title)) + "-—-"
    return [TSpan(title), _cc(f" {dashes}")]


def _language_value(names: list[str], theme: Theme) -> Children:
    spans: Children = []
    for i, name in enumerate(names):
        if i:
            spans.append(_cc(", "))
        spans.append(_colored(name, language_color(name, theme)))
    return spans


def _legend(segments: list[Segment], theme: Theme) -> Children:
    langs = [s for s in segments if s.name != OTHER][:3]
    other = [s for s in segments if s.name == OTHER]
    spans: Children = []
    for i, seg in enumerate([*langs, *other]):
        if i:
            spans.append(_cc("  "))
        spans.append(_colored("●", language_color(seg.name, theme)))
        spans.append(_cc(f" {seg.name} {seg.percent}%"))
    return spans


def _stats(pairs: list[tuple[str, int]], icons: dict[str, str]) -> Children:
    spans: Children = []
    for i, (label, value) in enumerate(pairs):
        if i:
            spans.append(_cc(" | "))
        spans += [*_icon(label, icons), _key(label), _val(f" {value:,}")]
    return spans


def _title(profile: Profile) -> Children:
    dashes = "-" + "—" * 39 + "-—-"
    return [TSpan(f"{profile.user}@github"), _cc(f" {dashes}")]


def _identity(profile: Profile, settings: Settings) -> list[Children]:
    lines: list[Children] = []
    for name in settings.fields:
        entry = _IDENTITY.get(name)
        if entry is None:
            continue
        label, getter = entry
        value = getter(profile)
        if value:
            lines.append(_kv(label, [_val(str(value))], settings.icons))
    return lines


def _language_section(
    profile: Profile, theme: Theme, settings: Settings
) -> list[Children]:
    programming, markup = split_languages(
        profile.lang_bytes,
        settings.programming_limit,
        settings.markup_limit,
        settings.language_sort,
    )
    rows: list[Children] = []
    if programming:
        rows.append(
            _kv(
                "Programming",
                _language_value(programming, theme),
                settings.icons,
            )
        )
    if markup:
        rows.append(
            _kv("Markup", _language_value(markup, theme), settings.icons)
        )
    rows += [
        _kv(key, [_val(settings.manual[key])], settings.icons)
        for key in ("Frameworks", "Real")
        if settings.manual.get(key)
    ]
    segments = usage_segments(
        profile.lang_bytes, BAR_CELLS, settings.bar_top, settings.language_sort
    )
    if segments:
        rows.append(
            [
                _colored("█" * seg.cells, language_color(seg.name, theme))
                for seg in segments
                if seg.cells
            ]
        )
        rows.append(_legend(segments, theme))
    if not rows:
        return []
    return [_section("Languages"), *rows]


def _hobbies(settings: Settings) -> list[Children]:
    rows = [
        _kv(key, [_val(settings.manual[key])], settings.icons)
        for key in ("Software", "Hardware")
        if settings.manual.get(key)
    ]
    if not rows:
        return []
    return [_section("Hobbies"), *rows]


def _system(settings: Settings) -> list[Children]:
    if not settings.jokes:
        return []
    return [
        _section("System"),
        *(
            _kv(label, [_val(value)], settings.icons)
            for label, value in settings.jokes.items()
        ),
    ]


def _stats_section(profile: Profile, settings: Settings) -> list[Children]:
    pairs = [
        (_STATS[name][0], _STATS[name][1](profile))
        for name in settings.stats
        if name in _STATS
    ]
    if not pairs:
        return []
    return [
        _section("GitHub Stats"),
        *(
            _stats(pairs[start : start + STATS_PER_ROW], settings.icons)
            for start in range(0, len(pairs), STATS_PER_ROW)
        ),
    ]


def _blocks() -> list[Children]:
    return [
        [_colored("███", color) for color in BLOCKS_NORMAL],
        [_colored("███", color) for color in BLOCKS_BRIGHT],
    ]


def _build_section(
    name: str, profile: Profile, theme: Theme, settings: Settings
) -> list[Children]:
    if name == "identity":
        return _identity(profile, settings)
    if name == "languages":
        return _language_section(profile, theme, settings)
    if name == "hobbies":
        return _hobbies(settings)
    if name == "system":
        return _system(settings)
    if name == "stats":
        return _stats_section(profile, settings)
    return []


def build_panel(
    profile: Profile, theme: Theme, settings: Settings
) -> tuple[Text, int]:
    """Build the right-hand info column"""
    lines: list[Children] = [_title(profile)]
    for name in settings.sections:
        section = _build_section(name, profile, theme, settings)
        if section:
            lines.append([])  # blank spacer before each populated section
            lines += section
    lines.append([])
    lines += _blocks()

    text = Text("", insert=(COLUMN_X, 30), fill=theme.fg)
    y = 30
    for children in lines:
        row = TSpan("", x=[COLUMN_X], y=[y])
        for child in children:
            row.add(child)
        text.add(row)
        y += LINE_HEIGHT
    return text, y - LINE_HEIGHT
