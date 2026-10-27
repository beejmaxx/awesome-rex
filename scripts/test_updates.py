import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("scanner", SCRIPTS / "new-from-export.py")
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)
update_spec = importlib.util.spec_from_file_location("updater", SCRIPTS / "update-from-showcase.py")
updater = importlib.util.module_from_spec(update_spec)
update_spec.loader.exec_module(updater)


def export_file(path, messages):
    path.write_text(json.dumps({
        "guild": {"id": "1"}, "channel": {"id": "2"}, "messages": messages,
    }))


def message(repo, timestamp, **extra):
    return {
        "id": "3", "content": f"https://github.com/{repo}",
        "timestamp": timestamp, "author": {"name": "Contributor"}, **extra,
    }


class UpdateTests(unittest.TestCase):
    def test_keychain_lookup_keeps_value_in_memory(self):
        with patch.object(updater.sys, "platform", "darwin"), patch.object(updater.shutil, "which", return_value="/usr/bin/security"), patch.object(updater.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, stdout="not-a-real-token\n", stderr="")
            self.assertEqual(updater.saved_token(), "not-a-real-token")
            args, kwargs = run.call_args
            self.assertIn(updater.KEYCHAIN_SERVICE, args[0])
            self.assertNotIn("not-a-real-token", args[0])
            self.assertTrue(kwargs["capture_output"])
            run.return_value = subprocess.CompletedProcess([], 44, stdout="", stderr="not found")
            self.assertEqual(updater.saved_token(), "")
        with patch.object(updater.sys, "platform", "linux"), patch.object(updater.subprocess, "run") as run:
            self.assertEqual(updater.saved_token(), "")
            run.assert_not_called()

    def test_exact_readme_match_and_git_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            export_file(root / "export.json", [
                message("Owner/Tool", "2026-10-01T00:00:00Z"),
                message("other/known.git.", "2026-10-01T00:00:00Z"),
                message("user-attachments/assets", "2026-10-01T00:00:00Z"),
                message("beejmaxx/awesome-rex", "2026-10-01T00:00:00Z"),
            ])
            found = scanner.find_candidates(root, "https://github.com/owner/tool-extra https://github.com/OTHER/KNOWN")
            self.assertEqual([c["repository"] for c in found], ["Owner/Tool"])

    def test_earliest_mention_across_files_and_timezones(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            export_file(root / "a.json", [message("owner/tool", "2026-10-02T00:00:00Z")])
            export_file(root / "z.json", [message("Owner/Tool", "2026-10-02T01:00:00+08:00", author={"nickname": "Earlier"})])
            found = scanner.find_candidates(root, "")
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0]["author"], "Earlier")
            self.assertEqual(found[0]["messageUrl"], "https://discord.com/channels/1/2/3")

    def test_embeds_metadata_and_empty_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "run.json").write_text('{"candidateCount": 1}')
            export_file(root / "empty.json", [])
            export_file(root / "export.json", [message("ignored/value", "2026-10-01T00:00:00Z", content="", embeds=[{"url": "https://github.com/owner/embedded"}])])
            found = scanner.find_candidates(root, "")
            self.assertEqual([c["repository"] for c in found], ["owner/embedded"])

    def test_invalid_input_fails_instead_of_reporting_nothing_new(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "No DiscordChatExporter"):
                scanner.find_candidates(root, "")
            (root / "broken.json").write_text('{')
            with self.assertRaisesRegex(ValueError, "Cannot read"):
                scanner.find_candidates(root, "")

    def test_offline_update_produces_reports_without_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "export.json"
            export_file(source, [message("fixture-owner/fixture-project", "2026-10-01T00:00:00Z")])
            output = root / "reports"
            env = dict(os.environ)
            env.pop("DISCORD_TOKEN", None)
            result = subprocess.run([sys.executable, str(SCRIPTS / "update-from-showcase.py"), "--from-export", str(source), "--output-dir", str(output)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            candidates = json.loads((output / "candidates.json").read_text())
            self.assertEqual(candidates[0]["repository"], "fixture-owner/fixture-project")
            self.assertIn("discord.com/channels/1/2/3", (output / "candidates.txt").read_text())

    def test_exporter_handoff_and_failure_preserve_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stub = root / "discord-chat-exporter"
            stub.write_text(f"#!{sys.executable}\n" + '''import json, os, sys
from pathlib import Path
assert os.environ['DISCORD_TOKEN'] == 'not-a-real-token'
assert 'not-a-real-token' not in ' '.join(sys.argv)
assert '--token' not in sys.argv and '-t' not in sys.argv
assert sys.argv[sys.argv.index('--include-threads') + 1] == 'All'
assert '--after' not in sys.argv and '--before' in sys.argv
output = Path(sys.argv[sys.argv.index('--output') + 1])
output.mkdir(parents=True)
(output / 'export.json').write_text(json.dumps({'guild': {'id': '1'}, 'channel': {'id': '2'}, 'messages': []}))
sys.exit(int(os.environ.get('STUB_EXIT', '0')))
''')
            stub.chmod(0o700)
            env = dict(os.environ, PATH=str(root), DISCORD_TOKEN="not-a-real-token")
            for code in (0, 17):
                output = root / f"run-{code}"
                result = subprocess.run([sys.executable, str(SCRIPTS / "update-from-showcase.py"), "--output-dir", str(output)], env=dict(env, STUB_EXIT=str(code)), capture_output=True, text=True)
                self.assertEqual(result.returncode, 0 if code == 0 else 1, result.stderr)
                self.assertEqual((output / "candidates.json").exists(), code == 0)
                self.assertNotIn("not-a-real-token", result.stdout + result.stderr)
                self.assertNotIn("not-a-real-token", "".join(p.read_text() for p in output.rglob("*.json")))


if __name__ == "__main__":
    unittest.main()
