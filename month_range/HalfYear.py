from __future__ import annotations

import datetime
import math
from functools import total_ordering
from typing import Literal

from .Month import Month
from .MonthRange import MonthRange


@total_ordering
class HalfYear(MonthRange):
    def __init__(self, year: int = None, half: int = None) -> None:
        if year is None or half is None:
            today = datetime.date.today()
            year = today.year if year is None else year
            half = math.ceil(today.month / 6) if half is None else half
        # handle out of range half offsets
        half -= 1
        year += math.floor(half / 2)
        half = half % 2  # 0 or 1
        super().__init__(
            first_month=Month(year=year, month=6 * half + 1),
            last_month=Month(year=year, month=6 * half + 6),
        )



    @property
    def year(self) -> int:
        return self.first_month.year

    @property
    def half(self) -> Literal[1] | Literal[2]:
        return 1 if self.first_month.month == 1 else 2

    def __str__(self) -> str:
        return str(self.year) + '-h' + str(self.half)

    def next(self, off: int = 1) -> HalfYear:
        return HalfYear(year=self.year, half=self.half + off)

    def prev(self, off: int = 1) -> HalfYear:
        return HalfYear(year=self.year, half=self.half - off)