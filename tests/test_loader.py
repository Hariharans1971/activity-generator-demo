"""Tests for the input loader."""

import json
import tempfile
import unittest
from pathlib import Path

from activity_planner.loader import ActivityDataError, load_activity


class LoaderTests(unittest.TestCase):
    def write_temp(self, suffix: str, content: str) -> Path:
        temporary = tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, encoding="utf-8", delete=False
        )
        temporary.write(content)
        temporary.close()
        path = Path(temporary.name)
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_loads_json_object_with_events(self):
        path = self.write_temp(
            ".json",
            json.dumps({"events": [{"date": "2026-10-20", "repository": "api", "type": "COMMIT", "count": 2}]}),
        )
        records = load_activity(path)
        self.assertEqual(records[0]["type"], "commit")
        self.assertEqual(records[0]["count"], 2)

    def test_loads_csv(self):
        path = self.write_temp(
            ".csv",
            "date,repository,type,count\n2026-10-20,api,commit,3\n",
        )
        self.assertEqual(load_activity(path)[0]["count"], 3)

    def test_rejects_invalid_date(self):
        path = self.write_temp(
            ".json",
            json.dumps([{"date": "yesterday", "repository": "api", "type": "commit", "count": 1}]),
        )
        with self.assertRaises(ActivityDataError):
            load_activity(path)

    def test_rejects_negative_count(self):
        path = self.write_temp(
            ".json",
            json.dumps([{"date": "2026-10-20", "repository": "api", "type": "commit", "count": -1}]),
        )
        with self.assertRaises(ActivityDataError):
            load_activity(path)

    def test_rejects_unsupported_extension(self):
        path = self.write_temp(".txt", "not supported")
        with self.assertRaises(ActivityDataError):
            load_activity(path)


if __name__ == "__main__":
    unittest.main()
