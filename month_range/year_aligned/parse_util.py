from datetime import datetime, date
from math import floor, ceil
from typing import Mapping, Collection, Any, Callable

MONTH_KEYWORDS = ["month", "month", "mon", "m"]


def parse_month_int(v: Any) -> int:
    if isinstance(v, int):
        if 1 <= v <= 12:
            return v
        raise ValueError(f"unable to parse {v} as month")
    if isinstance(v, date | datetime):
        return v.month
    return _parse_int(v, MONTH_KEYWORDS, parse_month_int)


QUARTER_KEYWORDS = ["quarter", "quartal", "quart", "q"]


def parse_quarter_int(v: Any) -> int:
    if isinstance(v, int):
        if 1 <= v <= 4:
            return v
        raise ValueError(f"unable to parse {v} as quarter")
    if isinstance(v, date | datetime):
        return ceil(v.month / 3)
    return _parse_int(v, QUARTER_KEYWORDS, parse_quarter_int)


HALF_KEYWORDS = ["half", "h"]


def parse_half_int(v: Any) -> int:
    if isinstance(v, int):
        if 1 <= v <= 2:
            return v
        raise ValueError(f"unable to parse {v} as half")
    if isinstance(v, date | datetime):
        return ceil(v.month / 6)
    return _parse_int(v, HALF_KEYWORDS, parse_half_int)


YEAR_KEYWORDS = ["year", "y"]


def parse_year_int(v: Any) -> int:
    if isinstance(v, int):
        return v
    if isinstance(v, date | datetime):
        return v.year
    return _parse_int(v, YEAR_KEYWORDS, parse_year_int)


def _parse_int(v: Any, keywords: Collection[str], callback: Callable[[Any], int]) -> int:
    if isinstance(v, str):
        v = v.lower().strip()
        for key in keywords:
            if v.startswith(key):
                v = v[len(key) :].strip()
        if v.isdigit():
            return callback(int(v))
    elif isinstance(v, float):
        return callback(floor(v))
    elif isinstance(v, Mapping):
        for key in v.keys():
            if key.lower() in keywords:
                return callback(v[key])
    elif isinstance(v, Collection):
        if len(v) == 1:
            return callback(next(iter(v)))
    raise ValueError(f"unable to parse {v} as int")
