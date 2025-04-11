from __future__ import annotations

import datetime
import math
from functools import total_ordering
from typing import Literal

from .Month import Month
from .MonthRange import MonthRange


@total_ordering
class QuarterYear(MonthRange):
    def __init__(self, year: int = None, quarter: int = None) -> None:
        if year is None or quarter is None:
            today = datetime.date.today()
            year = today.year if year is None else year
            quarter = math.ceil(today.month / 3) if quarter is None else quarter
        # handle out of range quarter offsets
        quarter -= 1
        year += math.floor(quarter / 4)
        quarter = quarter % 4  # 0, 1, 2 or 3
        super().__init__(
            first_month=Month(year=year, month=3 * quarter + 1),
            last_month=Month(year=year, month=3 * quarter + 3),
        )

    @property
    def year(self) -> int:
        return self.first_month.year

    @property
    def quarter(self) -> Literal[1] | Literal[2] | Literal[3] | Literal[4]:
        return math.ceil(self.first_month.month / 3)

    def __str__(self) -> str:
        return str(self.year) + '-q' + str(self.quarter)

    def next(self, off: int = 1) -> QuarterYear:
        return QuarterYear(year=self.year, quarter=self.quarter + off)

    def prev(self, off: int = 1) -> QuarterYear:
        return QuarterYear(year=self.year, quarter=self.quarter - off)

