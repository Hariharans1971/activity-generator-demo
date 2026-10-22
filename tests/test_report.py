"""Tests for report formatting."""

import unittest

from activity_planner.analysis import summarize_activity
from activity_planner.report import render_markdown, render_text


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.summary = summarize_activity([
            {"date": "2026-10-20", "repository": "sample-api", "type": "commit", "count": 2}
        ])

    def test_markdown_contains_summary_and_repository(self):
        report = render_markdown(self.summary)
        self.assertIn("# GitHub Activity Report", report)
        self.assertIn("sample-api", report)
        self.assertIn("Activity units", report)

    def test_text_output_contains_suggestions(self):
        report = render_text(self.summary)
        self.assertIn("GitHub Activity Planner", report)
        self.assertIn("Suggested next steps", report)


if __name__ == "__main__":
    unittest.main()
