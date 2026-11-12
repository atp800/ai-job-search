import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.draft_stem import draft_stem


class VacancyFilesTests(unittest.TestCase):
    def test_two_requisitions_keep_independent_drafts(self):
        with TemporaryDirectory() as tmp:
            for key in ("acme/R-123", "acme/R123"):
                stem = draft_stem("Acme", "Bioinformatics Analyst", key)
                with (Path(tmp) / f"main_{stem}.tex").open("x") as draft:
                    draft.write(key)
            for key in ("acme/R-123", "acme/R123"):
                stem = draft_stem("Acme", "Bioinformatics Analyst", key)
                self.assertEqual((Path(tmp) / f"main_{stem}.tex").read_text(), key)

    def test_archive_consumers_use_shared_identity_rules(self):
        commands = Path(__file__).resolve().parents[1] / ".claude/commands"
        for name in ("outcome", "interview", "html-report", "notion-sync", "outlook-sync"):
            with self.subTest(name=name):
                self.assertIn("_match-vacancy.md", (commands / f"{name}.md").read_text(encoding="utf-8"))
        rules = (commands / "_match-vacancy.md").read_text(encoding="utf-8")
        self.assertIn("Only an ID-less legacy row can use its suffixless folder", rules)
