# Contributing

Thanks for considering a contribution!

## Ground rules

- Keep changes focused and explain the problem they solve.
- Do not commit secrets, personal access tokens, or private activity exports.
- Do not create fake activity data or automated commits to manipulate contribution graphs.
- Add or update tests for behavior changes.
- Keep the CLI dependency-free unless a dependency is clearly justified.

## Setup

Python 3.10+ is required.

~~~bash
git clone https://github.com/Hariharans1971/activity-generator-demo.git
cd activity-generator-demo
python -m unittest discover -s tests -v
~~~

## Workflow

1. Open or comment on an issue to discuss a substantial change.
2. Create a branch such as feat/date-filter or fix/csv-validation.
3. Implement the smallest useful change.
4. Add tests for normal and edge cases.
5. Run the test suite and try the CLI against both sample files.
6. Open a pull request with a clear summary, test evidence, and trade-offs.

## First issues to consider

- Add optional date-range filters.
- Add JSON output for scripts that consume summaries.
- Improve handling of timestamps while preserving date-only inputs.
- Add richer sample reports.
- Add CI across supported Python versions.

A contribution is most useful when it solves a real problem and can be reviewed.
