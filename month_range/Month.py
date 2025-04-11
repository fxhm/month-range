from __future__ import annotations

import datetime
import math
from functools import total_ordering
from typing import List

from .MonthRange import MonthRange


@total_ordering
class Month(MonthRange):
    _year: int
    _month: int

    def __init__(self, year: int = None, month: int = None) -> None:
        super().__init__(self, self)
        today = datetime.date.today()
        self._year = int(year) if year is not None else today.year
        if month is not None:
            month = int(month) - 1
            self._year += math.floor(month / 12)
            self._month = (month % 12) + 1
        else:
            self._month = today.month

    def __init__(self, number: int) -> None:
        if 1 <= number <= 12:
            self.__init__(year=None, month=number)
            return
        elif 1900 <= number <= 99999:
            self.__init__(year=number, month=None)
            return
        elif 190001 <= number <= 999999:
            month = number % 100
            if 1 <= month <= 12:
                self.__init__(year=number // 100, month=month)
                return
        raise ValueError(f'unable to parse {number} as Month')


    def __init__(self, string: str) -> None:
        try:
            # todo handle more formats
            vals = string.split('-', maxsplit=1)
            self.__init__(year=int(vals[0]), month=int(vals[1]))
        except (ValueError, IndexError):
            raise ValueError(f'unable to parse {string} as Month')

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    def __str__(self) -> str:
        return str(self.year) + '-' + str(self.month).zfill(2)

    def next(self, off: int = 1) -> Month:
        return Month(year=self.year, month=self.month + off)

    def prev(self, off: int = 1) -> Month:
        return Month(year=self.year, month=self.month - off)

    def split(self) -> List[Month]:
        return [self]

