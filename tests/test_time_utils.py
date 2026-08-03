from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from neocard.time_utils import _plural, account_age


def _ago(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


@pytest.mark.parametrize(
    ("count", "expected"),
    [(0, "0 years"), (1, "1 year"), (2, "2 years")],
)
def test_plural_only_drops_the_s_for_exactly_one(
    count: int, expected: str
) -> None:
    assert _plural(count, "year") == expected


def test_account_age_names_all_three_units() -> None:
    parts = account_age(_ago(400)).split(", ")
    assert len(parts) == 3
    assert parts[0].endswith(("year", "years"))
    assert parts[1].endswith(("month", "months"))
    assert parts[2].endswith(("day", "days"))


def test_account_age_of_a_brand_new_account_is_all_zeroes() -> None:
    assert account_age(_ago(0)) == "0 years, 0 months, 0 days"


def test_account_age_counts_a_full_year() -> None:
    assert account_age(_ago(366)).startswith("1 year,")
