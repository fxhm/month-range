from typing import List, Any, Dict

from .HalfYear import HalfYear
from .Month import Month
from .MonthRange import MonthRange
from .QuarterYear import QuarterYear
from .Year import Year


def _abort_parse(v: Any, condition: bool = True) -> None:
    if condition:
        raise ValueError(f'unable to parse {v} as {MonthRange.__name__}')

def parse(v: str | Dict[str, Any]) -> MonthRange:
    # todo move logic to classes
    if isinstance(v, str):
        v = v.lower()

        parts = v.split('-q')
        if len(parts) == 2:
            return QuarterYear(year=int(parts[0]), quarter=int(parts[1]))
        _abort_parse(v, len(parts) > 1)

        parts = v.split('-h')
        if len(parts) == 2:
            return HalfYear(year=int(parts[0]), half=int(parts[1]))
        _abort_parse(v, len(parts) > 1)

        parts = v.split('-')
        if len(parts) == 2:
            return Month(year=int(parts[0]), month=int(parts[1]))
        _abort_parse(v, len(parts) > 1)

        return Year(year=int(v))
    elif isinstance(v, dict):
        start = None
        for key in ['start', 'from', 'min', 'begin', 'first']:
            if key in v:
                start = parse(v[key])
                break
        end = None
        for key in ['end', 'to', 'max', 'until', 'last']:
            if key in v:
                end = parse(v[key])
                break
        _abort_parse(v, not start or not end)
        return MonthRange(first_month=start.first_month, last_month=end.last_month).simplify()

    _abort_parse(v)


def union(*month_ranges: MonthRange, simplify: bool = True) -> List[MonthRange]:
    if len(month_ranges) == 0:
        return []
    result = []
    month_ranges = sorted(month_ranges, key=lambda t: t.first_month)
    prev = month_ranges[0]
    for month_range in month_ranges[1:]:
        if prev.overlaps(other=month_range) or month_range.follows_directly(prev):
            prev = MonthRange(
                first_month=min(prev.first_month, month_range.first_month),
                last_month=max(prev.last_month, month_range.last_month),
            )
        else:
            result.append(prev)
            prev = month_range
    result.append(prev)
    return list(map(lambda mr: mr.simplify(), result)) if simplify else result


def intersect(*month_ranges: MonthRange, simplify: bool = True) -> MonthRange | None:
    if len(month_ranges) == 0:
        return None
    intersection = month_ranges[0]
    for month_range in month_ranges[1:]:
        if intersection.overlaps(other=month_range):
            intersection = MonthRange(
                first_month=max(intersection.first_month, month_range.first_month),
                last_month=min(intersection.last_month, month_range.last_month),
            )
        else:
            return None
    return intersection.simplify() if simplify else intersection
