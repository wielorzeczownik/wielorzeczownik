from __future__ import annotations

from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

_CREATED_AT_FMT = "%Y-%m-%dT%H:%M:%SZ"


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def account_age(created_at: str) -> str:
    """Format the account age (GitHub ``created_at``) as 'X years, Y months, Z days'."""
    start = (
        datetime.strptime(created_at, _CREATED_AT_FMT)
        .replace(tzinfo=timezone.utc)
        .date()
    )
    age = relativedelta(datetime.now(timezone.utc).date(), start)
    return (
        f"{_plural(age.years, 'year')}, "
        f"{_plural(age.months, 'month')}, "
        f"{_plural(age.days, 'day')}"
    )
