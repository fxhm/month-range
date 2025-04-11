from __future__ import annotations

import datetime
from functools import total_ordering
from typing import Type, Optional, List

from .month import Month
from .time_range import MonthRange
from .quarter_year import QuarterYear


@total_ordering
class Year(MonthRange):
    __smaller__: Optional[Type[MonthRange]] = QuarterYear
    _year: int

    def __init__(self, year: int | str | None = None) -> None:
        super().__init__()
        if year is None:
            year = datetime.date.today().year
        else:
            try:
                year = int(year)
            except ValueError:
                raise ValueError(f'unable to parse {year} as Year')
        super().__init__(
            first_month=Month(year=year, month=1),
            last_month=Month(year=year, month=12),
        )

    def split(self) -> List[QuarterYear]:
        return [QuarterYear(year=self.year, quarter=q) for q in range(1, 5)]

    @property
    def year(self) -> int:
        return self.first_month.year

    def __str__(self) -> str:
        return str(self.year)

    def next(self, off: int = 1) -> Year:
        return Year(year=self.year + off)

    def prev(self, off: int = 1) -> Year:
        return Year(year=self.year - off)
