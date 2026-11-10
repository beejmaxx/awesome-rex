import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("stars", SCRIPTS / "update-stars.py")
stars = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stars)

README = """# List

- [one](https://github.com/Owner/One) - Does one thing.
- [two](https://github.com/owner/two/) - Does two things. ([demo](https://github.com/owner/two/blob/main/demo.gif)) (★ 3)
- [sub](https://github.com/owner/dotfiles/tree/main/tool) - Lives in a subdirectory.
- [site](https://example.com) - Not on GitHub.
- [gone](https://github.com/owner/gone) - Was deleted. (★ 9)
- [zero](https://github.com/owner/zero) - Brand new. (★ 1)
"""


class StarTests(unittest.TestCase):
    def test_format(self):
        self.assertEqual([stars.format_stars(n) for n in (0, 999, 1000, 1049, 1250, 9960, 12400)],
                         ["0", "999", "1k", "1k", "1.2k", "10k", "12k"])

    def test_only_direct_repository_links_are_counted(self):
        self.assertEqual(stars.repositories(README.splitlines()),
                         ["owner/gone", "owner/one", "owner/two", "owner/zero"])

    def test_apply_adds_replaces_keeps_and_drops_counts(self):
        counts = {"owner/one": 1250, "owner/two": 40, "owner/zero": 0}
        lines = stars.apply_stars(README.splitlines(), counts)
        self.assertEqual(lines[2], "- [one](https://github.com/Owner/One) - Does one thing. (★ 1.2k)")
        self.assertTrue(lines[3].endswith("([demo](https://github.com/owner/two/blob/main/demo.gif)) (★ 40)"))
        self.assertTrue(lines[4].endswith("subdirectory."))
        self.assertTrue(lines[6].endswith("Was deleted. (★ 9)"), "failed lookups keep the old count")
        self.assertTrue(lines[7].endswith("Brand new."), "zero stars shows no count")
        self.assertEqual(stars.apply_stars(lines, counts), lines, "reapplying is stable")

    def test_fetch_reads_partial_graphql_results(self):
        class Result:
            returncode = 1
            stdout = '{"data": {"r0": {"stargazerCount": 5}, "r1": null}, "errors": [{"type": "NOT_FOUND"}]}'
            stderr = "gh: Could not resolve to a Repository"
        with patch.object(stars.subprocess, "run", return_value=Result()) as run:
            self.assertEqual(stars.fetch_stars(["a/b", "c/d"]), {"a/b": 5})
        query = run.call_args.args[0][-1]
        self.assertIn('r0: repository(owner: "a", name: "b")', query)


if __name__ == "__main__":
    unittest.main()
