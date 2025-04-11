from __future__ import annotations

import math
from datetime import date, datetime
from functools import total_ordering
from typing import Literal, Any, Self, Mapping, Sequence

from .Month import Month
from .MonthRange import MonthRange
from .parse_util import parse_year_int, parse_half_int


@total_ordering
class HalfYear(MonthRange):
    def __init__(self, year: int, half: int) -> None:
        # handle out of range half offsets
        half -= 1
        year += math.floor(half / 2)
        half = half % 2  # 0 or 1
        super().__init__(
            start=Month(year=year, month=6 * half + 1),
            end=Month(year=year, month=6 * half + 6),
        )

    @classmethod
    def parse(cls, v: Any, *, simplify: bool = True) -> Self:
        try:
            if isinstance(v, date | datetime):
                return cls(v.year, math.ceil(v.month / 6))
            if isinstance(v, str):
                parts = v.split("-")
                cls._abort_parse(v, len(parts) != 2)
                return cls(parse_year_int(parts[0]), parse_half_int(parts[1]))
            if isinstance(v, Mapping):
                return cls(parse_year_int(v), parse_half_int(v))
            if isinstance(v, Sequence) and len(v) == 2:
                return cls(parse_year_int(v[0]), parse_half_int(v[1]))
        except Exception:
            pass
        cls._abort_parse(v)

    @classmethod
    def current(cls) -> HalfYear:
        today = date.today()
        return cls(today.year, math.ceil(today.month / 6))

    @property
    def year(self) -> int:
        return self.first_month.year

    @property
    def half(self) -> Literal[1] | Literal[2]:
        return 1 if self.first_month.month == 1 else 2

    def __str__(self) -> str:
        return str(self.year) + "-h" + str(self.half)

    def next(self, offset: int = 1) -> HalfYear:
        return HalfYear(year=self.year, half=self.half + offset)

    def prev(self, offset: int = 1) -> HalfYear:
        return HalfYear(year=self.year, half=self.half - offset)
