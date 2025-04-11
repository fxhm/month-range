from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, Tuple, Callable, Iterable

from .Year import Year
from .HalfYear import HalfYear
from .QuarterYear import QuarterYear
from .util import intersect, union
from .Month import Month


class MonthRange:
    _first_month: Month
    _last_month: Month
    
    def __init__(self, first_month: Month | str | int, last_month: Month | str | int) -> None:
        if not isinstance(first_month, Month):
            first_month = Month(first_month)
        if not isinstance(last_month, Month):
            last_month = Month(last_month)
        if first_month <= last_month:
            self._first_month = first_month
            self._last_month = last_month
        else:
            self._first_month = last_month
            self._last_month = first_month

    @property
    def month_count(self) -> int:
        first_month = self.first_month
        last_month = self.last_month
        if first_month.year == last_month.year:
            return last_month.month - first_month.month + 1
        return 13 - first_month.month + last_month.month + 12 * (last_month.year - first_month.year - 1)


    @property
    def months(self) -> List[Month]:
        month = self.first_month
        last_month = self.last_month
        months = []
        while month <= last_month:
            months.append(month)
            month = month.next()
        return months

    def split(self) -> List[MonthRange]:
        return self.months

    @property
    def first_month(self) -> Month:
        return self._first_month

    @property
    def last_month(self) -> Month:
        return self._last_month

    def next(self, off: int = 1) -> MonthRange:
        if off == 0:
            return self
        return MonthRange(
            first_month=self.first_month.next(off=off * self.month_count),
            last_month=self.last_month.next(off=off * self.month_count),
        )

    def prev(self, off: int = 1) -> MonthRange:
        if off == 0:
            return self
        return MonthRange(
            first_month=self.first_month.prev(off=off * self.month_count),
            last_month=self.last_month.prev(off=off * self.month_count),
        )

    def simplify(self) -> MonthRange:
        # todo check if is MonthRange or already simplified subclass
        first_month = self.first_month
        last_month = self.last_month
        if first_month.year == last_month.year:
            if first_month.month == last_month.month:
                return first_month
            if first_month.month == 1:
                if last_month.month == 12:
                    return Year(year=first_month.year)
                if last_month.month == 6:
                    return HalfYear(year=first_month.year, half=1)
                if last_month.month == 3:
                    return QuarterYear(year=first_month.year, quarter=1)
            if first_month.month == 4 and last_month.month == 6:
                return QuarterYear(year=first_month.year, quarter=2)
            if first_month.month == 7:
                if last_month.month == 12:
                    return HalfYear(year=first_month.year, half=2)
                if last_month.month == 9:
                    return QuarterYear(year=first_month.year, quarter=3)
            if first_month.month == 10 and last_month.month == 12:
                return QuarterYear(year=first_month.year, quarter=4)
        return self

    def overlaps(self, other: MonthRange) -> bool:
        return other.first_month in self or other.last_month in self or self.first_month in other or self.last_month in other

    def follows_directly(self, other: MonthRange) -> bool:
        return self.first_month.prev() == other.last_month

    def union(self, *others: MonthRange, simplify: bool = True) -> List[MonthRange]:
        return union(self, *others, simplify=simplify)

    def intersect(self, *others: MonthRange, simplify: bool = True) -> MonthRange | None:
        return intersect(self, *others, simplify=simplify)

    def _check_valid_operands(self, other):
        if not hasattr(other, 'first_month') or not hasattr(other, 'last_month'):
            raise NotImplementedError(f'cannot compare {self.__class__.__name__} to {other.__class__.__name__}')

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f'{self.first_month} ↔ {self.last_month}'

    def __hash__(self):
        return hash((self.first_month.year, self.first_month.month, self.last_month.year, self.last_month.month))

    def __len__(self) -> int:
        return self.month_count

    def __contains__(self, other: MonthRange) -> bool:
        self._check_valid_operands(other)
        return other.first_month >= self.first_month and other.last_month <= self.last_month

    def __eq__(self, other: MonthRange) -> bool:
        self._check_valid_operands(other)
        return self.first_month == other.first_month and self.last_month == other.last_month

    def __lt__(self, other: MonthRange) -> bool:
        self._check_valid_operands(other)
        if self.first_month.year < other.first_month.year:
            return True
        if self.first_month.year == other.first_month.year:
            return self.first_month.month < other.first_month.month
        return False

    def __gt__(self, other: MonthRange) -> bool:
        self._check_valid_operands(other)
        if self.last_month.year > other.last_month.year:
            return True
        if self.last_month.year == other.last_month.year:
            return self.last_month.month > other.last_month.month
        return False

    def __add__(self, off: int) -> MonthRange:
        return self.next(off)

    def __sub__(self, off: int) -> MonthRange:
        return self.prev(off)

    def __or__(self, other: MonthRange) -> List[MonthRange]:
        return self.union(other)

    def __and__(self, other: MonthRange) -> MonthRange | None:
        return self.intersect(other)

#     todo xor



