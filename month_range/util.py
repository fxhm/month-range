from typing import List

from .HalfYear import HalfYear
from .MonthRange import MonthRange
from .QuarterYear import QuarterYear
from .Year import Year


def simplify_month_range(month_range: MonthRange) -> MonthRange:
    # todo check if is MonthRange or already simplified subclass
    first_month = month_range.first_month
    last_month = month_range.last_month
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
    return month_range


def union_month_ranges(*month_ranges: MonthRange, simplify: bool = True) -> List[MonthRange]:
    if len(month_ranges) == 0:
        return []
    result = []
    month_ranges = sorted(month_ranges, key=lambda t: t.first_month)
    prev = month_ranges[0]
    for month_range in month_ranges[1:]:
        if prev.overlaps(other=month_range) or month_range.follows_directly(prev):
            prev = MonthRange(
                start=min(prev.first_month, month_range.first_month),
                end=max(prev.last_month, month_range.last_month),
            )
        else:
            result.append(prev)
            prev = month_range
    result.append(prev)
    return list(map(simplify_month_range, result)) if simplify else result


def intersect_month_ranges(*month_ranges: MonthRange, simplify: bool = True) -> MonthRange | None:
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
    return simplify_month_range(intersection) if simplify else intersection
