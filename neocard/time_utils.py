from __future__ import annotations

from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def account_age(created_at: datetime) -> str:
    """Format the account age as 'X years, Y months, Z days'"""
    age = relativedelta(datetime.now(timezone.utc).date(), created_at.date())
    return (
        f"{_plural(age.years, 'year')}, "
        f"{_plural(age.months, 'month')}, "
        f"{_plural(age.days, 'day')}"
    )
