import tempfile
import unittest
from pathlib import Path

from tools.application_validation import latest, open_ledger, record


class ApplicationValidationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "validation" / "checks.sqlite3"
        self.db = open_ledger(self.path)
        self.addCleanup(self.db.close)
        self.key = "example/R-123"
        self.clean = {"files": ["statement.txt"], "findings": []}
        self.error = {"files": ["statement.txt"], "findings": [{
            "file": "statement.txt", "location": "para 2", "error": "Incorrect start year",
            "evidence": "Super CV: 2023", "correction": "Change 2022 to 2023",
        }]}

    def test_fifth_recheck_can_pass(self):
        for revision in range(5):
            state = record(self.db, self.key, revision, self.error)
            self.assertEqual((state["status"], state["corrections"]), ("amend", revision + 1))
        result = record(self.db, self.key, 5, self.clean)
        self.assertEqual((result["status"], result["corrections"]), ("passed", 5))
        # A later application document gets a fresh inspection and correction budget.
        next_document = record(self.db, self.key, 6, self.error)
        self.assertEqual(next_document["corrections"], 1)

    def test_sixth_failed_inspection_cancels_only_this_application(self):
        for revision in range(6):
            state = record(self.db, self.key, revision, self.error)
        self.assertEqual((state["status"], state["corrections"]), ("cancelled", 5))
        another_session = open_ledger(self.path)
        self.addCleanup(another_session.close)
        self.assertEqual(latest(another_session, self.key)["report"], self.error)
        with self.assertRaisesRegex(ValueError, "cancelled"):
            record(another_session, self.key, 6, self.clean)
        self.assertEqual(record(another_session, "example/R-124", 0, self.clean)["status"], "passed")

    def test_incomplete_or_stale_inspection_never_advances_state(self):
        for report in (dict(self.clean, blocked="Missing posting"), {"files": []}, {"files": ["cv"], "findings": [{}]}):
            with self.assertRaises(ValueError):
                record(self.db, self.key, 0, report)
        self.assertEqual(latest(self.db, self.key)["status"], "unchecked")
        record(self.db, self.key, 0, self.error)
        with self.assertRaisesRegex(ValueError, "Stale"):
            record(self.db, self.key, 0, self.clean)
        self.assertEqual(latest(self.db, self.key)["revision"], 1)
