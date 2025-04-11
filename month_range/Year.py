from __future__ import annotations

from datetime import date
from functools import total_ordering
from typing import List, Any

from .QuarterYear import QuarterYear
from .MonthRange import MonthRange
from .Month import Month
from .parse_util import parse_year_int


@total_ordering
class Year(MonthRange):
    def __init__(self, year: int) -> None:
        super().__init__(
            start=Month(year=year, month=1),
            end=Month(year=year, month=12),
        )

    @classmethod
    def parse(cls, v: Any, *, simplify: bool = True) -> Year:
        try:
            return cls(parse_year_int(v))
        except Exception:
            pass
        cls._abort_parse(v)

    @classmethod
    def current(cls) -> Year:
        return cls(date.today().year)

    def split(self) -> List[QuarterYear]:
        return [QuarterYear(year=self.year, quarter=q) for q in range(1, 5)]

    @property
    def year(self) -> int:
        return self.first_month.year

    def __str__(self) -> str:
        return str(self.year)

    def next(self, offset: int = 1) -> Year:
        return Year(year=self.year + offset)

    def prev(self, offset: int = 1) -> Year:
        return Year(year=self.year - offset)
