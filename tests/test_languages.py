from __future__ import annotations

import pytest

from neocard.constants import MARKUP_LANGS
from neocard.languages import (
    OTHER,
    _largest_remainder,
    split_languages,
    usage_segments,
)

LANG_BYTES = {
    "Rust": 5000,
    "TypeScript": 3000,
    "PHP": 1500,
    "Python": 700,
    "C++": 300,
    "HTML": 900,
    "CSS": 400,
}


def test_split_languages_keeps_markup_out_of_programming() -> None:
    programming, markup = split_languages(LANG_BYTES, 4, 4, "size")
    assert not set(programming) & MARKUP_LANGS
    assert set(markup) <= MARKUP_LANGS


def test_split_languages_honours_the_limits() -> None:
    programming, markup = split_languages(LANG_BYTES, 2, 1, "size")
    assert len(programming) == 2
    assert len(markup) == 1


def test_split_languages_picks_the_biggest_before_sorting_by_name() -> None:
    """Name sorting must reorder the selection, not change what is selected."""
    by_size, _ = split_languages(LANG_BYTES, 2, 4, "size")
    by_name, _ = split_languages(LANG_BYTES, 2, 4, "name")
    assert set(by_name) == set(by_size)
    assert by_name == sorted(by_name, key=str.lower)


def test_usage_segments_fill_the_bar_exactly() -> None:
    cells = 40
    segments = usage_segments(LANG_BYTES, cells, 6, "size")
    assert sum(segment.cells for segment in segments) == cells


def test_usage_segments_collapse_the_tail_into_other() -> None:
    segments = usage_segments(LANG_BYTES, 40, 2, "size")
    assert segments[-1].name == OTHER


def test_usage_segments_omit_other_when_nothing_is_left_over() -> None:
    segments = usage_segments(LANG_BYTES, 40, len(LANG_BYTES), "size")
    assert OTHER not in [segment.name for segment in segments]


@pytest.mark.parametrize(
    ("lang_bytes", "cells", "top"),
    [
        ({}, 40, 6),
        ({"Rust": 0}, 40, 6),
        (LANG_BYTES, 0, 6),
        (LANG_BYTES, 40, 0),
    ],
)
def test_usage_segments_return_nothing_when_there_is_no_bar_to_draw(
    lang_bytes: dict[str, int], cells: int, top: int
) -> None:
    assert usage_segments(lang_bytes, cells, top, "size") == []


def test_usage_segments_name_sort_keeps_percentages_with_languages() -> None:
    """Reordering must move a percentage with its language, not past it."""
    by_size = {
        segment.name: segment.percent
        for segment in usage_segments(LANG_BYTES, 40, 6, "size")
    }
    by_name = {
        segment.name: segment.percent
        for segment in usage_segments(LANG_BYTES, 40, 6, "name")
    }
    assert by_name == by_size


@pytest.mark.parametrize("total", [0, 1, 7, 40, 101])
def test_largest_remainder_always_distributes_the_whole_total(
    total: int,
) -> None:
    weights = [0.5, 0.28, 0.21, 0.01]
    assert sum(_largest_remainder(weights, total)) == total
