import math
from abc import ABC
from datetime import date
from functools import total_ordering
from typing import Self, Generic, TypeVar, Literal

from .month_range import MonthRange

TI = TypeVar("TI", bound=Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])


@total_ordering
class YearAlignedMonthRange(MonthRange, Generic[TI], ABC):
    MONTH_COUNT: Literal[1, 2, 3, 4, 6, 12]

    def __init__(self, year: int, index: int) -> None:
        # handle out of range index offsets
        index -= 1
        year_divider = 12 // self.MONTH_COUNT
        year += math.floor(index / year_divider)
        index = index % year_divider
        super().__init__(
            start=MonthRange.__month_type__(year=year, index=self.MONTH_COUNT * index + 1),
            end=MonthRange.__month_type__(year=year, index=self.MONTH_COUNT * index + self.MONTH_COUNT),
        )

    @property
    def month_count(self) -> int:
        return self.MONTH_COUNT

    @property
    def year(self) -> int:
        return self.first_month.year

    @property
    def index(self) -> TI:
        return math.ceil(self.first_month.index / self.MONTH_COUNT)  # type: ignore

    @classmethod
    def current(cls) -> Self:
        today = date.today()
        return cls(year=today.year, index=math.ceil(today.month / cls.MONTH_COUNT))

    def next(self, offset: int = 1) -> Self:
        return self.__class__(year=self.year, index=self.index + offset)

    def prev(self, offset: int = 1) -> Self:
        return self.__class__(year=self.year, index=self.index - offset)
