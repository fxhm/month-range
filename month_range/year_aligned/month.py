from __future__ import annotations

import math
from collections.abc import Mapping
from datetime import date, datetime
from typing import Any, Self, Sequence, Literal, Type, List

from ..year_aligned_month_range import YearAlignedMonthRange
from .parse_util import parse_month_int, parse_year_int


class Month(YearAlignedMonthRange[Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]):
    MONTH_COUNT: Literal[1] = 1
    _year: int
    _index: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # noinspection PyMissingConstructor
    def __init__(self, year: int, index: int) -> None:
        index = index - 1
        self._year = year + math.floor(index / 12)
        self._index = (index % 12) + 1  # type: ignore
        self._first_month = self
        self._last_month = self

    @classmethod
    def parse(cls, v: Any, *, year_align: bool = True) -> Self:
        try:
            if isinstance(v, date | datetime):
                return cls(v.year, v.month)
            if isinstance(v, str):
                if v.isdigit():
                    v = int(v)
                else:
                    parts = v.split("-")
                    if len(parts) != 2:
                        cls._abort_parse(v)
                    return cls(parse_year_int(parts[0]), parse_month_int(parts[1]))
            if isinstance(v, float):
                v = math.floor(v)
            if isinstance(v, int):
                # YYYYMM format
                if 100001 <= v <= 999912:
                    month = v % 100
                    if month < 1 or month > 12:
                        cls._abort_parse(v)
                    return cls(v // 100, month)
            if isinstance(v, Mapping):
                return cls(parse_year_int(v), parse_month_int(v))
            if isinstance(v, Sequence) and len(v) == 2:
                return cls(parse_year_int(v[0]), parse_month_int(v[1]))
        except Exception:
            pass
        cls._abort_parse(v)

    def __str__(self) -> str:
        return str(self.year) + "-" + str(self.index).zfill(2)

    # the following methods rely on first_month in superclasses and have to be redefined here to avoid infinite recursion
    @property
    def year(self) -> int:
        return self._year

    @property
    def index(self) -> Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        return self._index

    # the following methods are redefined here for performance reasons
    @classmethod
    def current(cls) -> Month:
        today = date.today()
        return cls(today.year, today.month)

    def next(self, offset: int = 1) -> Month:
        return Month(year=self.year, index=self.index + offset)

    def prev(self, offset: int = 1) -> Month:
        return Month(year=self.year, index=self.index - offset)

    def split(self, by: Type[YearAlignedMonthRange] = None, year_align: bool = True) -> List[Month]:
        return [self]
