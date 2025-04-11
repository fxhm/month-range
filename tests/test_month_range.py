# # Now the actual tests for MonthRange
# from month_range import Month, MonthRange
#
#
# class TestMonthRange:
#     def test_init_with_month_objects(self):
#         """Test initialization with Month objects."""
#         first = Month(2025, 1)
#         last = Month(2025, 12)
#         month_range = MonthRange(first, last)
#
#         assert month_range.first_month == first
#         assert month_range.last_month == last
#
#     def test_init_with_strings(self):
#         """Test initialization with string representations."""
#         month_range = MonthRange("2023-01", "2023-12")
#
#         assert month_range.first_month.year == 2023
#         assert month_range.first_month.month == 1
#         assert month_range.last_month.year == 2023
#         assert month_range.last_month.month == 12
#
#     def test_init_with_integers(self):
#         """Test initialization with integer representations (YYYYMM)."""
#         month_range = MonthRange(202301, 202312)
#
#         assert month_range.first_month.year == 2023
#         assert month_range.first_month.month == 1
#         assert month_range.last_month.year == 2023
#         assert month_range.last_month.month == 12
#
#     def test_init_swaps_if_first_greater_than_last(self):
#         """Test that the constructor swaps months if first > last."""
#         month_range = MonthRange("2023-12", "2023-01")
#
#         assert month_range.first_month.year == 2023
#         assert month_range.first_month.month == 1
#         assert month_range.last_month.year == 2023
#         assert month_range.last_month.month == 12
#
#     def test_month_count_same_year(self):
#         """Test month_count property when months are in the same year."""
#         month_range = MonthRange("2023-03", "2023-08")
#         assert month_range.month_count == 6
#
#     def test_month_count_different_years(self):
#         """Test month_count property when months span multiple years."""
#         month_range = MonthRange("2022-10", "2024-02")
#         assert month_range.month_count == 17  # 3 + 12 + 2
#
#     def test_months_property(self):
#         """Test that the months property returns all months in the range."""
#         month_range = MonthRange("2023-10", "2024-02")
#         months = month_range.months
#
#         assert len(months) == 5
#         assert months[0].year == 2023 and months[0].month == 10
#         assert months[1].year == 2023 and months[1].month == 11
#         assert months[2].year == 2023 and months[2].month == 12
#         assert months[3].year == 2024 and months[3].month == 1
#         assert months[4].year == 2024 and months[4].month == 2
#
#     def test_split_method(self):
#         """Test that split method returns individual months."""
#         month_range = MonthRange("2023-10", "2023-12")
#         split_months = month_range.split()
#
#         assert len(split_months) == 3
#         assert isinstance(split_months[0], Month)
#         assert split_months[0].year == 2023 and split_months[0].month == 10
#         assert split_months[1].year == 2023 and split_months[1].month == 11
#         assert split_months[2].year == 2023 and split_months[2].month == 12
#
#     def test_next_method(self):
#         """Test next method moves the range forward."""
#         month_range = MonthRange("2023-01", "2023-03")
#         next_range = month_range.next()
#
#         assert next_range.first_month.year == 2023
#         assert next_range.first_month.month == 4
#         assert next_range.last_month.year == 2023
#         assert next_range.last_month.month == 6
#
#     def test_next_method_with_offset(self):
#         """Test next method with a specific offset."""
#         month_range = MonthRange("2023-01", "2023-03")
#         next_range = month_range.next(2)
#
#         assert next_range.first_month.year == 2023
#         assert next_range.first_month.month == 7
#         assert next_range.last_month.year == 2023
#         assert next_range.last_month.month == 9
#
#     def test_prev_method(self):
#         """Test prev method moves the range backward."""
#         month_range = MonthRange("2023-04", "2023-06")
#         prev_range = month_range.prev()
#
#         assert prev_range.first_month.year == 2023
#         assert prev_range.first_month.month == 1
#         assert prev_range.last_month.year == 2023
#         assert prev_range.last_month.month == 3
#
#     def test_simplify_single_month(self):
#         """Test simplify when range is a single month."""
#         month_range = MonthRange("2023-05", "2023-05")
#         simplified = month_range.simplify()
#
#         assert isinstance(simplified, Month)
#         assert simplified.year == 2023
#         assert simplified.month == 5
#
#     def test_simplify_quarter(self):
#         """Test simplify when range is a quarter."""
#         month_range = MonthRange("2023-04", "2023-06")
#         simplified = month_range.simplify()
#
#         assert isinstance(simplified, QuarterYear)
#         assert simplified._year == 2023
#         assert simplified._quarter == 2
#
#     def test_simplify_half_year(self):
#         """Test simplify when range is a half year."""
#         month_range = MonthRange("2023-01", "2023-06")
#         simplified = month_range.simplify()
#
#         assert isinstance(simplified, HalfYear)
#         assert simplified._year == 2023
#         assert simplified._half == 1
#
#     def test_simplify_full_year(self):
#         """Test simplify when range is a full year."""
#         month_range = MonthRange("2023-01", "2023-12")
#         simplified = month_range.simplify()
#
#         assert isinstance(simplified, Year)
#         assert simplified._year == 2023
#
#     def test_simplify_non_standard_range(self):
#         """Test simplify when range doesn't match standard patterns."""
#         month_range = MonthRange("2023-02", "2023-11")
#         simplified = month_range.simplify()
#
#         # Should return self since it's not a standard pattern
#         assert simplified is month_range
#
#     def test_overlaps_method_with_overlap(self):
#         """Test overlaps method when ranges overlap."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         assert range1.overlaps(range2)
#         assert range2.overlaps(range1)
#
#     def test_overlaps_method_no_overlap(self):
#         """Test overlaps method when ranges don't overlap."""
#         range1 = MonthRange("2023-01", "2023-03")
#         range2 = MonthRange("2023-04", "2023-06")
#
#         assert not range1.overlaps(range2)
#         assert not range2.overlaps(range1)
#
#     def test_follows_directly_method_true(self):
#         """Test follows_directly method when it should return True."""
#         range1 = MonthRange("2023-01", "2023-03")
#         range2 = MonthRange("2023-04", "2023-06")
#
#         assert range2.follows_directly(range1)
#
#     def test_follows_directly_method_false(self):
#         """Test follows_directly method when it should return False."""
#         range1 = MonthRange("2023-01", "2023-03")
#         range2 = MonthRange("2023-05", "2023-07")
#
#         assert not range2.follows_directly(range1)
#
#     def test_union_method(self):
#         """Test union method combines ranges."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         # Using our mock implementation, this just returns both ranges
#         result = range1.union(range2)
#         assert len(result) == 2
#
#     def test_intersect_method_with_overlap(self):
#         """Test intersect method when ranges overlap."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         result = range1.intersect(range2)
#         assert result is not None
#         assert result.first_month.year == 2023
#         assert result.first_month.month == 4
#         assert result.last_month.year == 2023
#         assert result.last_month.month == 6
#
#     def test_intersect_method_no_overlap(self):
#         """Test intersect method when ranges don't overlap."""
#         range1 = MonthRange("2023-01", "2023-03")
#         range2 = MonthRange("2023-04", "2023-06")
#
#         result = range1.intersect(range2)
#         assert result is None
#
#     def test_contains_operator(self):
#         """Test the __contains__ operator."""
#         range1 = MonthRange("2023-01", "2023-12")
#         range2 = MonthRange("2023-03", "2023-06")
#
#         assert range2 in range1
#         assert range1 not in range2
#
#     def test_equality_operator(self):
#         """Test the __eq__ operator."""
#         range1 = MonthRange("2023-01", "2023-12")
#         range2 = MonthRange("2023-01", "2023-12")
#         range3 = MonthRange("2023-02", "2023-12")
#
#         assert range1 == range2
#         assert range1 != range3
#
#     def test_less_than_operator(self):
#         """Test the __lt__ operator."""
#         range1 = MonthRange("2022-01", "2022-12")
#         range2 = MonthRange("2023-01", "2023-12")
#         range3 = MonthRange("2023-02", "2023-12")
#
#         assert range1 < range2
#         assert range2 < range3
#         assert not range3 < range2
#
#     def test_greater_than_operator(self):
#         """Test the __gt__ operator."""
#         range1 = MonthRange("2023-01", "2023-12")
#         range2 = MonthRange("2022-01", "2022-12")
#         range3 = MonthRange("2023-01", "2023-11")
#
#         assert range1 > range2
#         assert range1 > range3
#         assert not range3 > range1
#
#     def test_add_operator(self):
#         """Test the __add__ operator."""
#         month_range = MonthRange("2023-01", "2023-03")
#         next_range = month_range + 1
#
#         assert next_range.first_month.year == 2023
#         assert next_range.first_month.month == 4
#         assert next_range.last_month.year == 2023
#         assert next_range.last_month.month == 6
#
#     def test_sub_operator(self):
#         """Test the __sub__ operator."""
#         month_range = MonthRange("2023-04", "2023-06")
#         prev_range = month_range - 1
#
#         assert prev_range.first_month.year == 2023
#         assert prev_range.first_month.month == 1
#         assert prev_range.last_month.year == 2023
#         assert prev_range.last_month.month == 3
#
#     def test_or_operator(self):
#         """Test the __or__ operator."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         result = range1 | range2
#         assert len(result) == 2  # Using our mock union implementation
#
#     def test_and_operator(self):
#         """Test the __and__ operator."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         result = range1 & range2
#         assert result is not None
#         assert result.first_month.year == 2023
#         assert result.first_month.month == 4
#         assert result.last_month.year == 2023
#         assert result.last_month.month == 6
#
#     def test_len_operator(self):
#         """Test the __len__ operator."""
#         month_range = MonthRange("2023-01", "2023-06")
#         assert len(month_range) == 6# Now the actual tests for MonthRange
# from month_range import Month, MonthRange
#
#
# class TestMonthRange:
#     def test_init_with_month_objects(self):
#         """Test initialization with Month objects."""
#         first = Month(2025, 1)
#         last = Month(2025, 12)
#         month_range = MonthRange(first, last)
#
#         assert month_range.first_month == first
#         assert month_range.last_month == last
#
#     def test_init_with_strings(self):
#         """Test initialization with string representations."""
#         month_range = MonthRange("2023-01", "2023-12")
#
#         assert month_range.first_month.year == 2023
#         assert month_range.first_month.month == 1
#         assert month_range.last_month.year == 2023
#         assert month_range.last_month.month == 12
#
#     def test_init_with_integers(self):
#         """Test initialization with integer representations (YYYYMM)."""
#         month_range = MonthRange(202301, 202312)
#
#         assert month_range.first_month.year == 2023
#         assert month_range.first_month.month == 1
#         assert month_range.last_month.year == 2023
#         assert month_range.last_month.month == 12
#
#     def test_init_swaps_if_first_greater_than_last(self):
#         """Test that the constructor swaps months if first > last."""
#         month_range = MonthRange("2023-12", "2023-01")
#
#         assert month_range.first_month.year == 2023
#         assert month_range.first_month.month == 1
#         assert month_range.last_month.year == 2023
#         assert month_range.last_month.month == 12
#
#     def test_month_count_same_year(self):
#         """Test month_count property when months are in the same year."""
#         month_range = MonthRange("2023-03", "2023-08")
#         assert month_range.month_count == 6
#
#     def test_month_count_different_years(self):
#         """Test month_count property when months span multiple years."""
#         month_range = MonthRange("2022-10", "2024-02")
#         assert month_range.month_count == 17  # 3 + 12 + 2
#
#     def test_months_property(self):
#         """Test that the months property returns all months in the range."""
#         month_range = MonthRange("2023-10", "2024-02")
#         months = month_range.months
#
#         assert len(months) == 5
#         assert months[0].year == 2023 and months[0].month == 10
#         assert months[1].year == 2023 and months[1].month == 11
#         assert months[2].year == 2023 and months[2].month == 12
#         assert months[3].year == 2024 and months[3].month == 1
#         assert months[4].year == 2024 and months[4].month == 2
#
#     def test_split_method(self):
#         """Test that split method returns individual months."""
#         month_range = MonthRange("2023-10", "2023-12")
#         split_months = month_range.split()
#
#         assert len(split_months) == 3
#         assert isinstance(split_months[0], Month)
#         assert split_months[0].year == 2023 and split_months[0].month == 10
#         assert split_months[1].year == 2023 and split_months[1].month == 11
#         assert split_months[2].year == 2023 and split_months[2].month == 12
#
#     def test_next_method(self):
#         """Test next method moves the range forward."""
#         month_range = MonthRange("2023-01", "2023-03")
#         next_range = month_range.next()
#
#         assert next_range.first_month.year == 2023
#         assert next_range.first_month.month == 4
#         assert next_range.last_month.year == 2023
#         assert next_range.last_month.month == 6
#
#     def test_next_method_with_offset(self):
#         """Test next method with a specific offset."""
#         month_range = MonthRange("2023-01", "2023-03")
#         next_range = month_range.next(2)
#
#         assert next_range.first_month.year == 2023
#         assert next_range.first_month.month == 7
#         assert next_range.last_month.year == 2023
#         assert next_range.last_month.month == 9
#
#     def test_prev_method(self):
#         """Test prev method moves the range backward."""
#         month_range = MonthRange("2023-04", "2023-06")
#         prev_range = month_range.prev()
#
#         assert prev_range.first_month.year == 2023
#         assert prev_range.first_month.month == 1
#         assert prev_range.last_month.year == 2023
#         assert prev_range.last_month.month == 3
#
#     def test_simplify_single_month(self):
#         """Test simplify when range is a single month."""
#         month_range = MonthRange("2023-05", "2023-05")
#         simplified = month_range.simplify()
#
#         assert isinstance(simplified, Month)
#         assert simplified.year == 2023
#         assert simplified.month == 5
#
#     def test_simplify_quarter(self):
#         """Test simplify when range is a quarter."""
#         month_range = MonthRange("2023-04", "2023-06")
#         simplified = month_range.simplify()
#
#         assert isinstance(simplified, QuarterYear)
#         assert simplified._year == 2023
#         assert simplified._quarter == 2
#
#     def test_simplify_half_year(self):
#         """Test simplify when range is a half year."""
#         month_range = MonthRange("2023-01", "2023-06")
#         simplified = month_range.simplify()
#
#         assert isinstance(simplified, HalfYear)
#         assert simplified._year == 2023
#         assert simplified._half == 1
#
#     def test_simplify_full_year(self):
#         """Test simplify when range is a full year."""
#         month_range = MonthRange("2023-01", "2023-12")
#         simplified = month_range.simplify()
#
#         assert isinstance(simplified, Year)
#         assert simplified._year == 2023
#
#     def test_simplify_non_standard_range(self):
#         """Test simplify when range doesn't match standard patterns."""
#         month_range = MonthRange("2023-02", "2023-11")
#         simplified = month_range.simplify()
#
#         # Should return self since it's not a standard pattern
#         assert simplified is month_range
#
#     def test_overlaps_method_with_overlap(self):
#         """Test overlaps method when ranges overlap."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         assert range1.overlaps(range2)
#         assert range2.overlaps(range1)
#
#     def test_overlaps_method_no_overlap(self):
#         """Test overlaps method when ranges don't overlap."""
#         range1 = MonthRange("2023-01", "2023-03")
#         range2 = MonthRange("2023-04", "2023-06")
#
#         assert not range1.overlaps(range2)
#         assert not range2.overlaps(range1)
#
#     def test_follows_directly_method_true(self):
#         """Test follows_directly method when it should return True."""
#         range1 = MonthRange("2023-01", "2023-03")
#         range2 = MonthRange("2023-04", "2023-06")
#
#         assert range2.follows_directly(range1)
#
#     def test_follows_directly_method_false(self):
#         """Test follows_directly method when it should return False."""
#         range1 = MonthRange("2023-01", "2023-03")
#         range2 = MonthRange("2023-05", "2023-07")
#
#         assert not range2.follows_directly(range1)
#
#     def test_union_method(self):
#         """Test union method combines ranges."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         # Using our mock implementation, this just returns both ranges
#         result = range1.union(range2)
#         assert len(result) == 2
#
#     def test_intersect_method_with_overlap(self):
#         """Test intersect method when ranges overlap."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         result = range1.intersect(range2)
#         assert result is not None
#         assert result.first_month.year == 2023
#         assert result.first_month.month == 4
#         assert result.last_month.year == 2023
#         assert result.last_month.month == 6
#
#     def test_intersect_method_no_overlap(self):
#         """Test intersect method when ranges don't overlap."""
#         range1 = MonthRange("2023-01", "2023-03")
#         range2 = MonthRange("2023-04", "2023-06")
#
#         result = range1.intersect(range2)
#         assert result is None
#
#     def test_contains_operator(self):
#         """Test the __contains__ operator."""
#         range1 = MonthRange("2023-01", "2023-12")
#         range2 = MonthRange("2023-03", "2023-06")
#
#         assert range2 in range1
#         assert range1 not in range2
#
#     def test_equality_operator(self):
#         """Test the __eq__ operator."""
#         range1 = MonthRange("2023-01", "2023-12")
#         range2 = MonthRange("2023-01", "2023-12")
#         range3 = MonthRange("2023-02", "2023-12")
#
#         assert range1 == range2
#         assert range1 != range3
#
#     def test_less_than_operator(self):
#         """Test the __lt__ operator."""
#         range1 = MonthRange("2022-01", "2022-12")
#         range2 = MonthRange("2023-01", "2023-12")
#         range3 = MonthRange("2023-02", "2023-12")
#
#         assert range1 < range2
#         assert range2 < range3
#         assert not range3 < range2
#
#     def test_greater_than_operator(self):
#         """Test the __gt__ operator."""
#         range1 = MonthRange("2023-01", "2023-12")
#         range2 = MonthRange("2022-01", "2022-12")
#         range3 = MonthRange("2023-01", "2023-11")
#
#         assert range1 > range2
#         assert range1 > range3
#         assert not range3 > range1
#
#     def test_add_operator(self):
#         """Test the __add__ operator."""
#         month_range = MonthRange("2023-01", "2023-03")
#         next_range = month_range + 1
#
#         assert next_range.first_month.year == 2023
#         assert next_range.first_month.month == 4
#         assert next_range.last_month.year == 2023
#         assert next_range.last_month.month == 6
#
#     def test_sub_operator(self):
#         """Test the __sub__ operator."""
#         month_range = MonthRange("2023-04", "2023-06")
#         prev_range = month_range - 1
#
#         assert prev_range.first_month.year == 2023
#         assert prev_range.first_month.month == 1
#         assert prev_range.last_month.year == 2023
#         assert prev_range.last_month.month == 3
#
#     def test_or_operator(self):
#         """Test the __or__ operator."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         result = range1 | range2
#         assert len(result) == 2  # Using our mock union implementation
#
#     def test_and_operator(self):
#         """Test the __and__ operator."""
#         range1 = MonthRange("2023-01", "2023-06")
#         range2 = MonthRange("2023-04", "2023-09")
#
#         result = range1 & range2
#         assert result is not None
#         assert result.first_month.year == 2023
#         assert result.first_month.month == 4
#         assert result.last_month.year == 2023
#         assert result.last_month.month == 6
#
#     def test_len_operator(self):
#         """Test the __len__ operator."""
#         month_range = MonthRange("2023-01", "2023-06")
#         assert len(month_range) == 6
