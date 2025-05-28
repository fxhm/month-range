from .month_range import MonthRange
from .year_aligned_month_range import YearAlignedMonthRange
from .year_aligned import Month, QuarterYear, HalfYear, Year
from .util import union_month_ranges, intersect_month_ranges, year_align_month_range, split_month_range


# resolving circular deps. why do you make me do this python?
MonthRange.__month_type__ = Month
MonthRange.__aligned_types__ = (Month, QuarterYear, HalfYear, Year)
MonthRange.split = split_month_range
MonthRange.union = union_month_ranges
MonthRange.intersect = intersect_month_ranges
MonthRange.year_align = year_align_month_range
