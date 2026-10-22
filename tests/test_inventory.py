import json
import tempfile
import unittest
from pathlib import Path
from erlab.inventory import scan_directory, summarize, diff_scans, write_json, load_json
from erlab.cli import main, list_games, profiles_dir

class TestInventory(unittest.TestCase):
    def test_scan_summary_diff(self):
        with tempfile.TemporaryDirectory() as base:
            root = Path(base) / "input"
            root.mkdir()
            (root / "a.png").write_bytes(b"\x89PNG\r\n\x1a\nhello")
            (root / "b.png").write_bytes(b"\x89PNG\r\n\x1a\nhello")
            first = scan_directory(root)
            stats = summarize(first)
            self.assertEqual(stats["total_files"], 2)
            self.assertEqual(stats["duplicate_sha256_groups"], 1)
            (root / "b.png").write_bytes(b"other")
            (root / "c.txt").write_bytes(b"text")
            second = scan_directory(root)
            diff = diff_scans(first, second)
            self.assertEqual(diff["added"], ["c.txt"])
            self.assertEqual(diff["modified"], ["b.png"])
            self.assertEqual(diff["unchanged_count"], 1)
            report = Path(base) / "report.json"
            write_json(first, report)
            self.assertEqual(load_json(report)["schema_version"], 1)

    def test_symlink_file_skipped(self):
        with tempfile.TemporaryDirectory() as base:
            root = Path(base) / "input"
            root.mkdir()
            other = Path(base) / "secret.txt"
            other.write_text("local secret")
            link = root / "linked.txt"
            try:
                link.symlink_to(other)
            except (NotImplementedError, OSError):
                self.skipTest("Symlinks unavailable")
            self.assertEqual(scan_directory(root)["files"], [])

    def test_out_inside_scan_rejected(self):
        with tempfile.TemporaryDirectory() as base:
            self.assertEqual(main(["scan", base, "--out", str(Path(base) / "inside.json")]), 2)

    def test_games_registry(self):
        records = list_games(profiles_dir())
        ids = {x["id"] for x in records}
        self.assertIn("genshin-impact", ids)
        self.assertIn("wuthering-waves", ids)
