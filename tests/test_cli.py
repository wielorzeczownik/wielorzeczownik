from __future__ import annotations

import pytest

from neocard.cli import _csv, _glyph, _icons, _jokes, _manual, build_parser
from neocard.constants import ICONS

# The Nerd Font display glyph, written as a codepoint so the source stays
# readable in editors without the font installed.
GPU_GLYPH = chr(0xF108)


def test_csv_falls_back_to_a_copy_the_caller_cannot_mutate() -> None:
    fallback = ["identity", "stats"]
    result = _csv(None, fallback)
    result.append("languages")
    assert fallback == ["identity", "stats"]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("identity,stats", ["identity", "stats"]),
        (" Identity , STATS ", ["identity", "stats"]),
        ("identity,,stats,", ["identity", "stats"]),
        ("", []),
    ],
)
def test_csv_normalises_the_list(text: str, expected: list[str]) -> None:
    assert _csv(text, ["unused"]) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("U+F108", GPU_GLYPH),
        ("u+f108", GPU_GLYPH),
        (" U+F108 ", GPU_GLYPH),
        (GPU_GLYPH, GPU_GLYPH),
        ("", ""),
    ],
)
def test_glyph_accepts_a_codepoint_or_the_character_itself(
    text: str, expected: str
) -> None:
    assert _glyph(text) == expected


def test_icons_override_one_entry_and_leave_the_rest_alone() -> None:
    args = build_parser().parse_args(["--icon", "GPU=U+F108"])
    icons = _icons(args)
    assert icons["GPU"] == GPU_GLYPH
    assert {k: v for k, v in icons.items() if k != "GPU"} == {
        k: v for k, v in ICONS.items() if k != "GPU"
    }


def test_icons_leave_the_shared_default_table_untouched() -> None:
    """ICONS is module state; mutating it would leak across renderings."""
    before = dict(ICONS)
    _icons(build_parser().parse_args(["--icon", "GPU=X"]))
    assert before == ICONS


def test_jokes_keep_the_order_they_were_passed_in() -> None:
    args = build_parser().parse_args(
        ["--system", "CPU=fast", "--system", "GPU=slow", "--system", "RAM=48K"]
    )
    assert list(_jokes(args)) == ["CPU", "GPU", "RAM"]


@pytest.mark.parametrize("item", ["noseparator", ""])
def test_jokes_and_icons_ignore_a_line_without_a_separator(item: str) -> None:
    args = build_parser().parse_args(["--system", item, "--icon", item])
    assert _jokes(args) == {}
    assert _icons(args) == dict(ICONS)


def test_manual_omits_the_rows_that_were_not_given() -> None:
    args = build_parser().parse_args(["--frameworks", "React, Vue"])
    assert _manual(args) == {"Frameworks": "React, Vue"}


def test_parser_defaults_match_the_documented_ones() -> None:
    args = build_parser().parse_args([])
    assert args.language_sort == "size"
    assert args.programming_limit == 4
    assert args.markup_limit == 4
    assert args.bar_top == 6
    assert args.token is None
    assert args.user is None
