import math
from typing import List, Type

from .month_range import MonthRange
from .year_aligned_month_range import YearAlignedMonthRange
from .year_aligned import Month, QuarterYear, HalfYear, Year


def year_align_month_range(month_range: MonthRange) -> MonthRange:
    if isinstance(month_range, YearAlignedMonthRange):
        return month_range
    # todo use YearAlignedMonthRange attributes
    first_month = month_range.first_month
    last_month = month_range.last_month
    if first_month.year == last_month.year:
        if first_month.index == last_month.index:
            return first_month
        if first_month.index == 1:
            if last_month.index == 12:
                return Year(year=first_month.year)
            if last_month.index == 6:
                return HalfYear(year=first_month.year, index=1)
            if last_month.index == 3:
                return QuarterYear(year=first_month.year, index=1)
        if first_month.index == 4 and last_month.index == 6:
            return QuarterYear(year=first_month.year, index=2)
        if first_month.index == 7:
            if last_month.index == 12:
                return HalfYear(year=first_month.year, index=2)
            if last_month.index == 9:
                return QuarterYear(year=first_month.year, index=3)
        if first_month.index == 10 and last_month.index == 12:
            return QuarterYear(year=first_month.year, index=4)
    return month_range


def union_month_ranges(*month_ranges: MonthRange, year_align: bool = True) -> List[MonthRange]:
    if len(month_ranges) == 0:
        return []
    result = []
    month_ranges = sorted(month_ranges, key=lambda t: t.first_month)
    prev = month_ranges[0]
    for month_range in month_ranges[1:]:
        if prev.overlaps(other=month_range) or month_range.directly_after(prev):
            prev = MonthRange(
                start=min(prev.first_month, month_range.first_month),
                end=max(prev.last_month, month_range.last_month),
            )
        else:
            result.append(prev)
            prev = month_range
    result.append(prev)
    return list(map(year_align_month_range, result)) if year_align else result


def intersect_month_ranges(*month_ranges: MonthRange, year_align: bool = True) -> MonthRange | None:
    if len(month_ranges) == 0:
        return None
    intersection = month_ranges[0]
    for month_range in month_ranges[1:]:
        if intersection.overlaps(other=month_range):
            intersection = MonthRange(
                start=max(intersection.first_month, month_range.first_month),
                end=min(intersection.last_month, month_range.last_month),
            )
        else:
            return None
    return year_align_month_range(intersection) if year_align else intersection


def split_month_range(
    month_range: MonthRange,
    by: Type[YearAlignedMonthRange] = Month,
    year_align: bool = True,
) -> List[MonthRange]:
    result = []
    split_begin: Month = month_range.first_month
    last_month: Month = month_range.last_month
    if by == Month:
        while split_begin <= last_month:
            result.append(split_begin)
            split_begin = split_begin.next()
        return result
    elif by == Year:
        while split_begin.year < last_month.year:
            result.append(MonthRange(split_begin, Month(split_begin.year, 12)))
            split_begin = Month(split_begin.year + 1, 1)
        result.append(MonthRange(split_begin, last_month))
    else:
        split = MonthRange(
            split_begin,
            Month(
                year=split_begin.year,
                index=math.ceil(split_begin.index / by.MONTH_COUNT) * by.MONTH_COUNT,
            ),
        )
        while last_month not in split:
            result.append(split)
            split_begin = split.last_month.next()
            split = MonthRange(split_begin, split.last_month.next(offset=by.MONTH_COUNT))
        result.append(MonthRange(split_begin, last_month))
    return list(map(year_align_month_range, result)) if year_align else result
