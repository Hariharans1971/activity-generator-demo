"""Input loading and validation for activity records."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any


class ActivityDataError(ValueError):
    """Raised when an input activity file is invalid."""


def _normalize_record(record: dict[str, Any], line_number: int) -> dict[str, Any]:
    required = {"date", "repository", "type", "count"}
    missing = required.difference(record)
    if missing:
        raise ActivityDataError(
            f"Record {line_number} is missing required fields: {', '.join(sorted(missing))}"
        )

    raw_date = str(record["date"]).strip()
    try:
        parsed_date = date.fromisoformat(raw_date)
    except (TypeError, ValueError) as exc:
        raise ActivityDataError(
            f"Record {line_number} has invalid date {raw_date!r}; expected YYYY-MM-DD"
        ) from exc

    repository = str(record["repository"]).strip()
    event_type = str(record["type"]).strip().lower()
    if not repository:
        raise ActivityDataError(f"Record {line_number} has an empty repository name")
    if not event_type:
        raise ActivityDataError(f"Record {line_number} has an empty event type")

    raw_count = record["count"]
    try:
        count = int(raw_count)
        if str(raw_count).strip() != str(count):
            raise ValueError
    except (TypeError, ValueError) as exc:
        raise ActivityDataError(
            f"Record {line_number} has invalid count {raw_count!r}; expected an integer"
        ) from exc

    if count < 0:
        raise ActivityDataError(f"Record {line_number} count cannot be negative")

    return {
        "date": parsed_date.isoformat(),
        "repository": repository,
        "type": event_type,
        "count": count,
    }


def load_activity(path: str | Path) -> list[dict[str, Any]]:
    """Load and validate records from a JSON or CSV file."""
    source = Path(path)
    if not source.exists():
        raise ActivityDataError(f"Input file does not exist: {source}")
    if not source.is_file():
        raise ActivityDataError(f"Input path is not a file: {source}")

    suffix = source.suffix.lower()
    try:
        if suffix == ".json":
            with source.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            if isinstance(payload, dict):
                payload = payload.get("events")
            if not isinstance(payload, list):
                raise ActivityDataError(
                    "JSON input must be a list of records or an object with an 'events' list"
                )
            raw_records = payload
        elif suffix == ".csv":
            with source.open("r", encoding="utf-8-sig", newline="") as handle:
                raw_records = list(csv.DictReader(handle))
        else:
            raise ActivityDataError(
                f"Unsupported input format {suffix!r}; use .json or .csv"
            )
    except json.JSONDecodeError as exc:
        raise ActivityDataError(
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ActivityDataError("Input must be UTF-8 encoded text") from exc

    normalized: list[dict[str, Any]] = []
    for index, record in enumerate(raw_records, start=1):
        if not isinstance(record, dict):
            raise ActivityDataError(f"Record {index} must be an object")
        normalized.append(_normalize_record(record, index))

    return normalized
