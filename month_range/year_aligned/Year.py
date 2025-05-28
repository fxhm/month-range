from __future__ import annotations

from datetime import date
from typing import Any, Literal

from ..YearAlignedMonthRange import YearAlignedMonthRange
from .parse_util import parse_year_int


class Year(YearAlignedMonthRange):
    MONTH_COUNT: Literal[12] = 12

    def __init__(self, year: int, index: int = 1) -> None:
        super().__init__(year=year, index=index)

    @classmethod
    def parse(cls, v: Any, *, year_align: bool = True) -> Year:
        try:
            return cls(parse_year_int(v))
        except Exception:
            pass
        cls._abort_parse(v)

    def __str__(self) -> str:
        return str(self.year)

    # the following methods are redefined here for performance reasons
    @property
    def index(self) -> Literal[1]:
        return 1

    @classmethod
    def current(cls) -> Year:
        return cls(date.today().year)
