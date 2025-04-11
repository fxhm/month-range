from __future__ import annotations

import math
from datetime import date, datetime
from functools import total_ordering
from typing import Literal, Any, Self, Sequence, Mapping

from .Month import Month
from .MonthRange import MonthRange
from .parse_util import parse_quarter_int, parse_year_int


@total_ordering
class QuarterYear(MonthRange):
    def __init__(self, year: int, quarter: int) -> None:
        # handle out of range quarter offsets
        quarter -= 1
        year += math.floor(quarter / 4)
        quarter = quarter % 4  # 0, 1, 2 or 3
        super().__init__(
            start=Month(year=year, month=3 * quarter + 1),
            end=Month(year=year, month=3 * quarter + 3),
        )

    @classmethod
    def parse(cls, v: Any, *, simplify: bool = True) -> Self:
        try:
            if isinstance(v, date | datetime):
                return cls(v.year, math.ceil(v.month / 3))
            if isinstance(v, str):
                parts = v.split("-")
                cls._abort_parse(v, len(parts) != 2)
                return cls(parse_year_int(parts[0]), parse_quarter_int(parts[1]))
            if isinstance(v, Mapping):
                return cls(parse_year_int(v), parse_quarter_int(v))
            if isinstance(v, Sequence) and len(v) == 2:
                return cls(parse_year_int(v[0]), parse_quarter_int(v[1]))
        except Exception:
            pass
        cls._abort_parse(v)

    @classmethod
    def current(cls) -> QuarterYear:
        today = date.today()
        return cls(today.year, math.ceil(today.month / 3))

    @property
    def year(self) -> int:
        return self.first_month.year

    @property
    def quarter(self) -> Literal[1] | Literal[2] | Literal[3] | Literal[4]:
        return math.ceil(self.first_month.month / 3)

    def __str__(self) -> str:
        return str(self.year) + "-q" + str(self.quarter)

    def next(self, offset: int = 1) -> QuarterYear:
        return QuarterYear(year=self.year, quarter=self.quarter + offset)

    def prev(self, offset: int = 1) -> QuarterYear:
        return QuarterYear(year=self.year, quarter=self.quarter - offset)
