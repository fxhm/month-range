from month_range import Month, MonthRange, QuarterYear, HalfYear, Year

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

