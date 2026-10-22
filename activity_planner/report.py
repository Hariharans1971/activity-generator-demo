"""Formatting functions for activity summaries."""

from __future__ import annotations

from typing import Any

from .analysis import suggest_next_steps


def _table_lines(title: str, mapping: dict[str, int]) -> list[str]:
    lines = [f"### {title}", ""]
    if not mapping:
        lines.extend(["_No data available._", ""])
        return lines
    lines.extend(["| Name | Count |", "|---|---:|"])
    lines.extend(f"| {name} | {count} |" for name, count in mapping.items())
    lines.append("")
    return lines


def render_markdown(summary: dict[str, Any]) -> str:
    """Render a Markdown report from a summary dictionary."""
    first = summary.get("first_activity_date") or "N/A"
    last = summary.get("last_activity_date") or "N/A"
    lines = [
        "# GitHub Activity Report",
        "",
        "> Generated from a user-provided local activity file. This is not a live GitHub API report.",
        "",
        "## Overview",
        "",
        f"- Records: **{summary.get('record_count', 0)}**",
        f"- Activity units: **{summary.get('total_activity', 0)}**",
        f"- Active days: **{summary.get('active_days', 0)}**",
        f"- Date range: **{first}** to **{last}**",
        f"- Longest gap between active dates: **{summary.get('longest_gap_days', 0)} day(s)**",
        "",
    ]
    lines.extend(_table_lines("Repositories", summary.get("repositories", {})))
    lines.extend(_table_lines("Event types", summary.get("event_types", {})))
    lines.extend(["## Daily activity", ""])
    daily = summary.get("daily_activity", {})
    if daily:
        lines.extend(["| Date | Count |", "|---|---:|"])
        lines.extend(f"| {day} | {count} |" for day, count in daily.items())
    else:
        lines.append("_No activity records were supplied._")
    lines.extend(["", "## Suggested next steps", ""])
    lines.extend(
        f"{index}. {suggestion}"
        for index, suggestion in enumerate(suggest_next_steps(summary), 1)
    )
    lines.append("")
    return "\n".join(lines)


def render_text(summary: dict[str, Any]) -> str:
    """Render a concise terminal summary."""
    first = summary.get("first_activity_date") or "N/A"
    last = summary.get("last_activity_date") or "N/A"
    lines = [
        "GitHub Activity Planner",
        "=======================",
        f"Records: {summary.get('record_count', 0)}",
        f"Activity units: {summary.get('total_activity', 0)}",
        f"Active days: {summary.get('active_days', 0)}",
        f"Date range: {first} to {last}",
        f"Longest gap: {summary.get('longest_gap_days', 0)} day(s)",
        "",
        "Repositories:",
    ]
    lines.extend(
        f"  - {name}: {count}"
        for name, count in summary.get("repositories", {}).items()
    )
    lines.extend(["", "Suggested next steps:"])
    lines.extend(
        f"  {index}. {item}"
        for index, item in enumerate(suggest_next_steps(summary), 1)
    )
    return "\n".join(lines)
