from __future__ import annotations

import math
from datetime import date, datetime
from typing import Literal, Any, Self, Mapping, Sequence

from ..year_aligned_month_range import YearAlignedMonthRange
from .parse_util import parse_year_int, parse_half_int


class HalfYear(YearAlignedMonthRange):
    MONTH_COUNT: Literal[6] = 6

    @classmethod
    def parse(cls, v: Any, *, year_align: bool = True) -> Self:
        try:
            if isinstance(v, date | datetime):
                return cls(v.year, math.ceil(v.month / 6))
            if isinstance(v, str):
                parts = v.split("-")
                if len(parts) != 2:
                    cls._abort_parse(v)
                return cls(parse_year_int(parts[0]), parse_half_int(parts[1]))
            if isinstance(v, Mapping):
                return cls(parse_year_int(v), parse_half_int(v))
            if isinstance(v, Sequence) and len(v) == 2:
                return cls(parse_year_int(v[0]), parse_half_int(v[1]))
        except Exception:
            pass
        cls._abort_parse(v)

    def __str__(self) -> str:
        return str(self.year) + "-h" + str(self.index)
