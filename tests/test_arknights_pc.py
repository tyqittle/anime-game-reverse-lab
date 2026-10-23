"""Regression tests for assembly and local art imports (no copyrighted images committed)."""
import json
import tempfile
import unittest
from pathlib import Path

from arknights_pc.tools.build import build, _safe_local, import_art


class ArknightsPCBuildTests(unittest.TestCase):
    def test_missing_upstream_fails_instead_of_faking_a_game(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                build(Path(td))

    def test_art_path_traversal_and_url_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            self.assertIsNone(_safe_local(p, "../../etc/passwd"))
            self.assertIsNone(_safe_local(p, "https://example.com/img.png"))

    def test_reuse_art_from_existing_gallery(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            gallery = p / "gallery"
            (gallery / "data").mkdir(parents=True)
            (gallery / "assets/portraits").mkdir(parents=True)
            (gallery / "assets/portraits/amiya.webp").write_bytes(b"sample")
            (gallery / "data/characters.json").write_text(json.dumps({
                "characters": [{"gameId": "arknights", "characterKey": "amiya", "name": "阿米娅",
                                "image": "./assets/portraits/amiya.webp"},
                               {"gameId": "genshin", "name": "not imported", "image": "./missing.png"}]
            }), encoding="utf-8")
            chibi = p / "q"
            chibi.mkdir()
            (chibi / "slot_0.png").write_bytes(b"chibi sample")
            output = p / "out"
            result = import_art(output, gallery, chibi)
            self.assertEqual(result["slots"][0]["name"], "阿米娅")
            self.assertIn("portrait", result["slots"][0])
            self.assertIn("chibi", result["slots"][0])
            self.assertTrue((output / "arknights/assets/portraits/slot_0.webp").is_file())
            self.assertFalse((output / "arknights/assets/chibi/slot_1.png").exists())

    def test_no_gallery_is_explicitly_placeholder(self):
        with tempfile.TemporaryDirectory() as td:
            data = import_art(Path(td), None, None)
            self.assertEqual(len(data["slots"]), 3)
            self.assertFalse(any("portrait" in s or "chibi" in s for s in data["slots"]))

    def test_preserve_upstream_and_generate_editable_project(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            upstream = root / "third_party/arknights-td-godot"
            (upstream / "scenes/maps").mkdir(parents=True)
            (upstream / "LICENSE.txt").write_text("MIT sample", encoding="utf-8")
            (upstream / "scenes/maps/map_template.tscn").write_text("map", encoding="utf-8")
            cfg = '[application]\nconfig/name="Outpost Assault"\nrun/main_scene="res://interfaces/UI/menu/menu.tscn"\n[autoload]\nGlobal="*res://assets/scripts/global.gd"\n'
            (upstream / "project.godot").write_text(cfg, encoding="utf-8")
            (upstream / "keep.txt").write_text("upstream unchanged", encoding="utf-8")
            overlay = root / "arknights_pc/overlay/arknights"
            overlay.mkdir(parents=True)
            (overlay / "launcher.tscn").write_text("scene", encoding="utf-8")
            result = build(root)
            self.assertIn("arknights_td", result["build"])
            generated = root / "arknights_pc/build/arknights_td"
            project = (generated / "project.godot").read_text(encoding="utf-8")
            self.assertIn("AKBridge=", project)
            self.assertIn("res://arknights/launcher.tscn", project)
            self.assertEqual((generated / "keep.txt").read_text(), "upstream unchanged")
            self.assertEqual((upstream / "keep.txt").read_text(), "upstream unchanged")
            with self.assertRaises(FileExistsError):
                build(root)
