from .MonthRange import MonthRange
from .month_number import MonthNumber
from .YearAlignedMonthRange import YearAlignedMonthRange
from .year_aligned import Month, QuarterYear, HalfYear, Year
from .util import union_month_ranges, intersect_month_ranges, simplify_month_range, split_month_range


# resolving circular deps. why do you make me do this python?
MonthRange.__month_type__ = Month
MonthRange.__sub_types__ = (Month, QuarterYear, HalfYear, Year)
MonthRange.split = split_month_range
MonthRange.union = union_month_ranges
MonthRange.intersect = intersect_month_ranges
MonthRange.simplify = simplify_month_range
