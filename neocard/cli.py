from __future__ import annotations

import argparse
import os
from pathlib import Path

from .config import (
    DEFAULT_BAR_TOP,
    DEFAULT_FIELDS,
    DEFAULT_LANGUAGE_SORT,
    DEFAULT_MARKUP_LIMIT,
    DEFAULT_PROGRAMMING_LIMIT,
    DEFAULT_SECTIONS,
    DEFAULT_STATS,
    DEFAULT_USER,
)
from .constants import ICONS, THEMES
from .github import GitHubClient
from .models import Settings
from .svg import render


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate neofetch profile cards",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-u",
        "--user",
        default=None,
        help="GitHub username",
    )
    parser.add_argument("-t", "--token", default=None, help="GitHub token.")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory to write neofetch-<theme>.svg into",
    )

    content = parser.add_argument_group("content (API rows have no override)")
    content.add_argument("--frameworks", help="Frameworks row")
    content.add_argument("--real", help="Real (spoken) row")
    content.add_argument("--hobbies-software", help="Software row")
    content.add_argument("--hobbies-hardware", help="Hardware row")
    content.add_argument(
        "--system",
        action="append",
        metavar="LABEL=VALUE",
        help="System section line, repeatable",
    )
    content.add_argument(
        "--icon",
        action="append",
        metavar="LABEL=GLYPH",
        help="Set a field's Nerd Font icon, repeatable"
        "literal glyph or a codepoint, e.g. --icon 'GPU=U+F108'",
    )

    layout = parser.add_argument_group("layout / selection")
    layout.add_argument(
        "--sections",
        metavar="A,B,...",
        help="Section order (identity,system,languages,hobbies,stats)",
    )
    layout.add_argument(
        "--fields",
        metavar="A,B,...",
        help="API rows to show, in order (uptime,host,kernel,website)",
    )
    layout.add_argument(
        "--stats",
        metavar="A,B,...",
        help="Stats to show, in order "
        "(repos,stars,followers,following,commits,prs,issues)",
    )
    layout.add_argument(
        "--language-sort",
        choices=("size", "name"),
        default=DEFAULT_LANGUAGE_SORT,
        help="Language ordering",
    )
    layout.add_argument(
        "--programming-limit", type=int, default=DEFAULT_PROGRAMMING_LIMIT
    )
    layout.add_argument(
        "--markup-limit", type=int, default=DEFAULT_MARKUP_LIMIT
    )
    layout.add_argument(
        "--bar-top",
        type=int,
        default=DEFAULT_BAR_TOP,
        help="Languages in the usage bar (0 hides it)",
    )
    return parser


def _csv(text: str | None, fallback: list[str]) -> list[str]:
    if text is None:
        return list(fallback)
    return [item.strip().lower() for item in text.split(",") if item.strip()]


def _manual(args: argparse.Namespace) -> dict[str, str]:
    rows = {
        "Frameworks": args.frameworks,
        "Real": args.real,
        "Software": args.hobbies_software,
        "Hardware": args.hobbies_hardware,
    }
    return {key: value for key, value in rows.items() if value}


def _glyph(text: str) -> str:
    """Accept a literal glyph or a 'U+XXXX' codepoint (readable in YAML)"""
    text = text.strip()
    if text[:2].upper() == "U+":
        codepoint = text[2:]
        return chr(int(codepoint, 16))
    return text


def _icons(args: argparse.Namespace) -> dict[str, str]:
    icons = dict(ICONS)
    for item in args.icon or []:
        label, sep, glyph = item.partition("=")
        if sep:
            icons[label.strip()] = _glyph(glyph)
    return icons


def _jokes(args: argparse.Namespace) -> dict[str, str]:
    jokes: dict[str, str] = {}
    for item in args.system or []:
        label, sep, value = item.partition("=")
        if sep:
            jokes[label.strip()] = value.strip()
    return jokes


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    user = (
        args.user or os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USER
    )
    settings = Settings(
        manual=_manual(args),
        jokes=_jokes(args),
        icons=_icons(args),
        sections=_csv(args.sections, DEFAULT_SECTIONS),
        fields=_csv(args.fields, DEFAULT_FIELDS),
        stats=_csv(args.stats, DEFAULT_STATS),
        language_sort=args.language_sort,
        programming_limit=args.programming_limit,
        markup_limit=args.markup_limit,
        bar_top=args.bar_top,
    )
    profile = GitHubClient(user, args.token).fetch_profile()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        path = args.output_dir / f"neofetch-{theme.name}.svg"
        path.write_text(render(profile, theme, settings), encoding="utf-8")
        print(f"wrote {path}")
    return 0
