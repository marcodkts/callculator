from datetime import datetime

from django.test import TestCase

from callculator.tools import call_cost_calculator


class CallCostCalculatorTest(TestCase):

    def test_call_within_rate_period(self):
        start = datetime(
            2024, 11, 13, 10, 0, 0
        )  # 10:00 AM within the rate period
        end = datetime(
            2024, 11, 13, 10, 30, 0
        )  # 10:30 AM within the rate period
        expected_cost = 0.36 + (30 * 0.09)  # 30 minutes charged
        self.assertAlmostEqual(
            call_cost_calculator(start, end), expected_cost, places=2
        )

    def test_call_outside_rate_period(self):
        start = datetime(
            2024, 11, 13, 23, 0, 0
        )  # 11:00 PM outside the rate period
        end = datetime(
            2024, 11, 13, 23, 30, 0
        )  # 11:30 PM outside the rate period
        expected_cost = 0.36  # Only initial cost, no payable minutes
        self.assertAlmostEqual(
            call_cost_calculator(start, end), expected_cost, places=2
        )

    def test_call_crossing_rate_periods(self):
        start = datetime(
            2024, 11, 13, 21, 50, 0
        )  # 9:50 PM within the rate period
        end = datetime(
            2024, 11, 13, 22, 10, 0
        )  # 10:10 PM crosses out of the rate period
        expected_minutes = (
            10  # Only the 10 minutes before 10:00 PM are charged
        )
        expected_cost = 0.36 + (expected_minutes * 0.09)
        self.assertAlmostEqual(
            call_cost_calculator(start, end), expected_cost, places=2
        )

    def test_call_with_exact_start_and_end_period(self):
        start = datetime(
            2024, 11, 13, 6, 0, 0
        )  # Exact start of the rate period
        end = datetime(2024, 11, 13, 22, 0, 0)  # Exact end of the rate period
        expected_minutes = 16 * 60  # Full 16 hours
        expected_cost = 0.36 + (expected_minutes * 0.09)
        self.assertAlmostEqual(
            call_cost_calculator(start, end), expected_cost, places=2
        )

    def test_short_call_with_partial_minute(self):
        start = datetime(
            2024, 11, 13, 10, 0, 30
        )  # 10:00:30 AM (30 seconds into a minute)
        end = datetime(
            2024, 11, 13, 10, 1, 15
        )  # 10:01:15 AM (45 seconds into the next minute)
        expected_minutes = 0  # No payable minutes
        expected_cost = 0.36 + (expected_minutes * 0.09)
        self.assertAlmostEqual(
            call_cost_calculator(start, end), expected_cost, places=2
        )
