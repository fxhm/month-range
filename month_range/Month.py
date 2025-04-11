from __future__ import annotations

import math
from collections.abc import Mapping
from datetime import date, datetime
from functools import total_ordering
from typing import List, Any, Self, Sequence

from .MonthRange import MonthRange
from .parse_util import parse_month_int, parse_year_int


@total_ordering
class Month(MonthRange):
    _year: int
    _month: int

    def __init__(self, year: int, month: int) -> None:
        month = month - 1
        self._year = year + math.floor(month / 12)
        self._month = (month % 12) + 1
        self._first_month = self
        self._last_month = self
        # super().__init__(self, self)

    @classmethod
    def parse(cls, v: Any, *, simplify: bool = True) -> Self:
        try:
            if isinstance(v, date | datetime):
                return cls(v.year, v.month)
            if isinstance(v, str):
                if v.isdigit():
                    v = int(v)
                else:
                    parts = v.split("-")
                    cls._abort_parse(v, len(parts) != 2)
                    return cls(parse_year_int(parts[0]), parse_month_int(parts[1]))
            if isinstance(v, float):
                v = math.floor(v)
            if isinstance(v, int):
                # YYYYMM format
                if 100001 <= v <= 999912:
                    month = v % 100
                    cls._abort_parse(v, month < 1 or month > 12)
                    return cls(v // 100, month)
            if isinstance(v, Mapping):
                return cls(parse_year_int(v), parse_month_int(v))
            if isinstance(v, Sequence) and len(v) == 2:
                return cls(parse_year_int(v[0]), parse_month_int(v[1]))
        except Exception:
            pass
        cls._abort_parse(v)

    @classmethod
    def current(cls) -> Month:
        today = date.today()
        return cls(today.year, today.month)

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    def __str__(self) -> str:
        return str(self.year) + "-" + str(self.month).zfill(2)

    def next(self, offset: int = 1) -> Month:
        return Month(year=self.year, month=self.month + offset)

    def prev(self, offset: int = 1) -> Month:
        return Month(year=self.year, month=self.month - offset)

    def split(self) -> List[Month]:
        return [self]
