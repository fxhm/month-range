from .MonthRange import MonthRange
from .YearAlignedMonthRange import YearAlignedMonthRange
from .month_number import MonthNumber
from .Month import Month
from .QuarterYear import QuarterYear
from .HalfYear import HalfYear
from .Year import Year
from .util import union_month_ranges, intersect_month_ranges, simplify_month_range, split_month_range


# resolving circular deps. why do you make me do this python?
MonthRange.__month_type__ = Month
MonthRange.__sub_types__ = (Month, QuarterYear, HalfYear, Year)
MonthRange.split = split_month_range
MonthRange.union = union_month_ranges
MonthRange.intersect = intersect_month_ranges
MonthRange.simplify = simplify_month_range
