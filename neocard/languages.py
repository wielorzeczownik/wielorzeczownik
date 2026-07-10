from __future__ import annotations

from dataclasses import dataclass

from .constants import MARKUP_LANGS

OTHER = "Other"


@dataclass(frozen=True)
class Segment:
    """One slice of the language-usage bar"""

    name: str
    cells: int
    percent: int


def _ranked(lang_bytes: dict[str, int], sort: str) -> list[tuple[str, int]]:
    if sort == "name":
        return sorted(lang_bytes.items(), key=lambda kv: kv[0].lower())
    return sorted(lang_bytes.items(), key=lambda kv: -kv[1])


def split_languages(
    lang_bytes: dict[str, int],
    programming_limit: int = 4,
    markup_limit: int = 4,
    sort: str = "size",
) -> tuple[list[str], list[str]]:
    """Order languages, then split into programming vs markup lists"""
    ranked = [name for name, _ in _ranked(lang_bytes, sort)]
    programming = [n for n in ranked if n not in MARKUP_LANGS]
    markup = [n for n in ranked if n in MARKUP_LANGS]
    return programming[:programming_limit], markup[:markup_limit]


def _largest_remainder(weights: list[float], total: int) -> list[int]:
    """Distribute total integer cells across weights, preserving the sum"""
    raw = [w * total for w in weights]
    base = [int(x) for x in raw]
    remainder = total - sum(base)
    order = sorted(
        range(len(raw)), key=lambda i: raw[i] - base[i], reverse=True
    )
    for i in order[:remainder]:
        base[i] += 1
    return base


def usage_segments(
    lang_bytes: dict[str, int],
    cells: int,
    top: int = 6,
    sort: str = "size",
) -> list[Segment]:
    """Full-width bar segments for the biggest languages plus an Other slice"""
    total = sum(lang_bytes.values())
    if total == 0 or cells <= 0 or top <= 0:
        return []
    head = sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:top]
    other = total - sum(v for _, v in head)
    if sort == "name":
        head = sorted(head, key=lambda kv: kv[0].lower())
    entries = [*head, (OTHER, other)] if other > 0 else list(head)
    counts = _largest_remainder([v / total for _, v in entries], cells)
    return [
        Segment(name=name, cells=count, percent=round(value / total * 100))
        for (name, value), count in zip(entries, counts)
    ]
