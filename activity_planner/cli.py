"""Command-line interface for GitHub Activity Planner."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analysis import summarize_activity
from .loader import ActivityDataError, load_activity
from .report import render_markdown, render_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="activity-planner",
        description="Analyze local GitHub activity snapshots and create a report.",
    )
    parser.add_argument("--input", required=True, help="Path to a .json or .csv activity file")
    parser.add_argument(
        "--format",
        choices=("text", "markdown"),
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument("--output", help="Optional output file; defaults to the terminal")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        records = load_activity(args.input)
        summary = summarize_activity(records)
        rendered = render_markdown(summary) if args.format == "markdown" else render_text(summary)
        if args.output:
            destination = Path(args.output)
            destination.write_text(rendered + "\n", encoding="utf-8")
            print(f"Report written to {destination}")
        else:
            print(rendered)
        return 0
    except (ActivityDataError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
