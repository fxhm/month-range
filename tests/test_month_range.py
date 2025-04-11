import pytest

from month_range import Month, MonthRange, QuarterYear, HalfYear, Year


def test_parse():
    for v in [202501, "202501", "2025-01", "2025-m01"]:
        assert MonthRange.parse(v) == Month(2025, 1)

    for v in ["2025-q1", "2025-q01", "2025-quarter1"]:
        assert MonthRange.parse(v) == QuarterYear(2025, 1)

    for v in ["2025-h1", "2025-h01", "2025-half1"]:
        assert MonthRange.parse(v) == HalfYear(2025, 1)

    for v in ["sdfg", "2025-m123"]:
        with pytest.raises(Exception):
            MonthRange.parse(v)

    assert MonthRange.parse(20) == Year(20)
    assert MonthRange.parse("20") == Year(20)
    assert MonthRange.parse(12) == Year(12)
    assert MonthRange.parse(202500) == Year(202500)

    assert MonthRange.parse(["2023-01", "2023-03"]) == QuarterYear(2023, 1)


def test_set_ops():
    assert Month(2025, 1) | Month(2025, 2) == [MonthRange(Month(2025, 1), Month(2025, 2))]
    assert Month(2025, 1) | Month(2025, 3) == [Month(2025, 1), Month(2025, 3)]
    assert Month(2025, 1).union(Month(2025, 2), Month(2025, 3)) == [QuarterYear(2025, 1)]
    assert Month(2025, 1).union(Month(2025, 2), Month(2025, 3), simplify=True)[0].__class__ == QuarterYear
    assert Month(2025, 1).union(Month(2025, 2), Month(2025, 3), simplify=False)[0].__class__ == MonthRange

def test_contains():
    assert Month(2025, 1) in Month(2025, 1)
    assert Month(2025, 1) in MonthRange(Month(2025, 1), Month(2025, 1))
    assert MonthRange(Month(2025, 1), Month(2025, 1)) in Month(2025, 1)

    assert Month(2025, 1) in QuarterYear(2025, 1)
    assert Month(2025, 1) in HalfYear(2025, 1)
    assert Month(2025, 1) in Year(2025)
    assert Month(2025, 1) in MonthRange(Month(2025, 1), Month(2025, 2))

    assert QuarterYear(2025, 1) not in Month(2025, 1)
    assert HalfYear(2025, 1) not in Month(2025, 1)
    assert Year(2025) not in Month(2025, 1)
    assert MonthRange(Month(2025, 1), Month(2025, 2)) not in Month(2025, 1)

    assert QuarterYear(2025, 1) in QuarterYear(2025, 1)
    assert QuarterYear(2025, 1) in MonthRange(Month(2025, 1), Month(2025, 3))
    assert MonthRange(Month(2025, 1), Month(2025, 3)) in QuarterYear(2025, 1)

    assert QuarterYear(2025, 1) in HalfYear(2025, 1)
    assert QuarterYear(2025, 1) in Year(2025)

    assert HalfYear(2025, 1) in HalfYear(2025, 1)
    assert HalfYear(2025, 1) in MonthRange(Month(2025, 1), Month(2025, 6))
    assert MonthRange(Month(2025, 1), Month(2025, 6)) in HalfYear(2025, 1)

    assert HalfYear(2025, 1) in Year(2025)
    assert HalfYear(2025, 1) not in Year(2026)
    assert HalfYear(2025, 1) not in HalfYear(2025, 2)
    assert HalfYear(2025, 1) not in MonthRange(Month(2025, 3), Month(2025, 6))
    assert HalfYear(2025, 1) not in MonthRange(Month(2025, 3), Month(2025, 8))

    assert Year(2025) in Year(2025)

def test_simplify():
    mr = MonthRange(Month(2025, 3), Month(2025, 9))
    assert mr.__class__ == MonthRange
    assert mr.simplify().__class__ == MonthRange

    mr = MonthRange(Month(2025, 1), Month(2025, 3))
    assert mr.__class__ == MonthRange
    assert mr.simplify().__class__ == QuarterYear
    assert mr.__class__ == MonthRange

    assert len(mr | QuarterYear(2025, 2)) == 1
    assert (mr | QuarterYear(2025, 2))[0] == HalfYear(2025, 1)

