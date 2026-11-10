import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("stars", SCRIPTS / "update-stars.py")
stars = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stars)

BADGE = "![Stars](https://img.shields.io/github/stars/{}?style=social)"
README = """# List

- [one](https://github.com/Owner/One) - Does one thing.
- [two](https://github.com/owner/two/) - Does two things. ([demo](https://github.com/owner/two/blob/main/demo.gif)) (★ 3)
- [sub](https://github.com/owner/dotfiles/tree/main/tool) - Lives in a subdirectory.
- [site](https://example.com) - Not on GitHub.
- [moved](https://github.com/new/name) - Was renamed. ![Stars](https://img.shields.io/github/stars/old/name?style=social)
"""


class StarTests(unittest.TestCase):
    def test_badges_added_fixed_and_old_text_removed(self):
        lines = stars.apply_badges(README.splitlines())
        self.assertEqual(lines[2], "- [one](https://github.com/Owner/One) - Does one thing. " + BADGE.format("Owner/One"))
        self.assertTrue(lines[3].endswith("demo.gif)) " + BADGE.format("owner/two")), lines[3])
        self.assertNotIn("★", lines[3])
        self.assertTrue(lines[4].endswith("subdirectory."))
        self.assertTrue(lines[5].endswith("Not on GitHub."))
        self.assertTrue(lines[6].endswith("Was renamed. " + BADGE.format("new/name")), lines[6])
        self.assertEqual(stars.apply_badges(lines), lines, "reapplying is stable")

    def test_only_direct_repository_links_are_counted(self):
        self.assertEqual(stars.repositories(README.splitlines()), ["new/name", "owner/one", "owner/two"])

    def test_format(self):
        self.assertEqual([stars.format_stars(n) for n in (0, 999, 1000, 1049, 1250, 9960, 12400)],
                         ["0", "999", "1k", "1k", "1.2k", "10k", "12k"])

    def test_fetch_reads_partial_graphql_results(self):
        class Result:
            returncode = 1
            stdout = '{"data": {"r0": {"stargazerCount": 5}, "r1": null}, "errors": [{"type": "NOT_FOUND"}]}'
            stderr = "gh: Could not resolve to a Repository"
        with patch.object(stars.subprocess, "run", return_value=Result()) as run:
            self.assertEqual(stars.fetch_stars(["a/b", "c/d"]), {"a/b": 5})
        self.assertIn('r0: repository(owner: "a", name: "b")', run.call_args.args[0][-1])


if __name__ == "__main__":
    unittest.main()
