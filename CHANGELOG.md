# Changelog

All notable changes to this project are documented here.

## 1.0.0 — 2026-10-22

First public release of GitHub Activity Planner.

### Added
- JSON and CSV import with input validation and actionable error messages.
- Activity summaries by day, repository, and event type.
- Longest gap calculation and project-focused next-step suggestions.
- Text and Markdown report output.
- Example activity datasets.
- Unit tests for loading, aggregation, suggestions, and report formatting.
- GitHub Actions workflow to run tests on Python 3.10 through 3.13.
- Contributor instructions, MIT license, and a good-first-issue starting point.

### Design decision
The application analyzes activity data supplied by the user. It does not create commits or make changes to GitHub repositories to artificially increase contribution counts.
