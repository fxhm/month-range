import pytest

from month_range import Month


def test_init():
    with pytest.raises(Exception):
        Month(None, None)

    with pytest.raises(Exception):
        Month(2025, None)

    with pytest.raises(Exception):
        Month(None, 1)

    with pytest.raises(Exception):
        Month("2025", "1")

    with pytest.raises(Exception):
        Month("2025", 1)

    with pytest.raises(Exception):
        Month(None, "1")

    month = Month(2025, 1)
    assert month.year == 2025
    assert month.month == 1

    month = Month(2025, 13)
    assert month.year == 2026
    assert month.month == 1

    month = Month(2025, 0)
    assert month.year == 2024
    assert month.month == 12

    month = Month(2025, 0)
    assert month.year == 2024
    assert month.month == 12

def test_parse():
    for v in [202501, "202501", "2025-01", "2025-m01"]:
        month = Month.parse(v)
        assert month.year == 2025
        assert month.month == 1

    for v in [202500, "202500", "sdfg", "2025-m123"]:
        with pytest.raises(Exception):
            Month.parse(v)

