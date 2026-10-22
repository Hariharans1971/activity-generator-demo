"""Tests for activity aggregation and recommendations."""

import unittest

from activity_planner.analysis import summarize_activity, suggest_next_steps


class AnalysisTests(unittest.TestCase):
    def test_aggregates_activity(self):
        records = [
            {"date": "2026-10-20", "repository": "api", "type": "commit", "count": 2},
            {"date": "2026-10-20", "repository": "api", "type": "issue", "count": 1},
            {"date": "2026-10-22", "repository": "web", "type": "commit", "count": 4},
        ]
        summary = summarize_activity(records)
        self.assertEqual(summary["total_activity"], 7)
        self.assertEqual(summary["active_days"], 2)
        self.assertEqual(summary["longest_gap_days"], 1)
        self.assertEqual(summary["repositories"]["api"], 3)
        self.assertEqual(summary["event_types"]["commit"], 6)

    def test_empty_data_returns_zero_summary(self):
        summary = summarize_activity([])
        self.assertEqual(summary["total_activity"], 0)
        self.assertEqual(summary["active_days"], 0)
        self.assertIsNone(summary["first_activity_date"])

    def test_suggestions_for_empty_data_are_actionable(self):
        suggestions = suggest_next_steps(summarize_activity([]))
        self.assertTrue(suggestions)
        self.assertIn("small", suggestions[0])


if __name__ == "__main__":
    unittest.main()
