import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("maintain", SCRIPTS / "maintain-links.py")
maintain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maintain)

BADGE = "![Stars](https://img.shields.io/github/stars/{}?style=social)"
LINES = [
    "## Tools",
    "",
    "- [kept](https://github.com/a/kept) - Stays. " + BADGE.format("a/kept"),
    "- [moved](https://github.com/old/name) - Renamed. ([demo](https://github.com/old/name/blob/main/d.gif)) " + BADGE.format("old/name"),
    "- [gone](https://github.com/b/gone) - Deleted. " + BADGE.format("b/gone"),
    "- [sub](https://github.com/c/dots/tree/main/tool) - In a subdirectory.",
    "- [unknown](https://github.com/d/flaky) - Lookup errored. " + BADGE.format("d/flaky"),
    "- [site](https://example.com) - Elsewhere.",
]
CURRENT = {"a/kept": "a/kept", "old/name": "new/place", "b/gone": None, "c/dots": "c/dots"}


class MaintainTests(unittest.TestCase):
    def test_renames_update_every_github_url_and_deletions_are_removed(self):
        lines, renamed, removed, held = maintain.repair(list(LINES), CURRENT, max_removals=3)
        moved = next(l for l in lines if l.startswith("- [moved]"))
        self.assertIn("(https://github.com/new/place)", moved)
        self.assertIn("github.com/new/place/blob/main/d.gif", moved)
        self.assertTrue(moved.endswith(BADGE.format("new/place")), moved)
        self.assertNotIn("old/name", moved)
        self.assertFalse(any(l.startswith("- [gone]") for l in lines))
        self.assertEqual((renamed, removed, held), (["moved: old/name -> new/place"], ["gone"], []))
        self.assertIn(LINES[6], lines, "entries whose lookup errored are untouched")
        self.assertIn(LINES[5], lines)

    def test_safety_limit_holds_mass_deletions(self):
        current = {"a/kept": None, "old/name": None, "b/gone": None}
        lines, _, removed, held = maintain.repair(list(LINES), current, max_removals=2)
        self.assertEqual(removed, [])
        self.assertEqual(held, ["kept", "moved", "gone"])
        self.assertEqual(len(lines), len(LINES))

    def test_lookup_separates_not_found_from_errors(self):
        class Result:
            stdout = ('{"data": {"r0": {"nameWithOwner": "new/place"}, "r1": null, "r2": null},'
                      ' "errors": [{"type": "NOT_FOUND", "path": ["r1"]}, {"type": "RATE_LIMITED", "path": ["r2"]}]}')
            stderr = ""
        with patch.object(maintain.subprocess, "run", return_value=Result()):
            self.assertEqual(maintain.lookup(["old/name", "b/gone", "d/flaky"]),
                             {"old/name": "new/place", "b/gone": None})


if __name__ == "__main__":
    unittest.main()
