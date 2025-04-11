from .MonthRange import MonthRange
from .Month import Month
from .QuarterYear import QuarterYear
from .HalfYear import HalfYear
from .Year import Year
from .util import union_month_ranges, intersect_month_ranges, simplify_month_range


# resolving circular deps. why do you make me do this python?
MonthRange.__sub_types__ = (Month, QuarterYear, HalfYear, Year)
MonthRange.__union_func__ = union_month_ranges
MonthRange.__intersect_func__ = intersect_month_ranges
MonthRange.__simplify_func__ = simplify_month_range
