"""Build tests operate on mock upstream sources, not on the user's APK."""
import tempfile
import unittest
from pathlib import Path
from offline_game.tools.build_game import AUTOLOAD, configure, build

class OfflineGameBuildTests(unittest.TestCase):
    def test_autoload_injection_is_idempotent(self):
        old = '[application]\nconfig/name="JRPG Demo"\nrun/main_scene="res://game.tscn"\n'
        new = configure(old)
        self.assertEqual(new.count(AUTOLOAD), 1)
        self.assertEqual(configure(new).count(AUTOLOAD), 1)

    def test_build_preserves_upstream_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            original = root / "third_party/godot-demo-projects/2d/role_playing_game"
            original.mkdir(parents=True)
            old = '[application]\nconfig/name="JRPG Demo"\nrun/main_scene="res://game.tscn"\n'
            (original / "project.godot").write_text(old)
            (original / "game.tscn").write_text("[gd_scene format=3]\n")
            (root / "third_party/godot-demo-projects/LICENSE.md").write_text("MIT")
            addon = root / "offline_game/overlay/addons/offline_mode"
            addon.mkdir(parents=True)
            (addon / "offline_manager.gd").write_text("extends Node")
            result = build(root)
            created = root / "offline_game/build/solo_jrpg"
            self.assertTrue(Path(result["project"]).is_file())
            self.assertTrue((created / "game.tscn").is_file())
            self.assertTrue((created / "UPSTREAM_LICENSE.md").is_file())
            self.assertIn(AUTOLOAD, (created / "project.godot").read_text())
            self.assertEqual((original / "project.godot").read_text(), old)
            with self.assertRaises(FileExistsError):
                build(root)
            self.assertTrue(build(root, force=True)["project"])

    def test_output_safety(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(ValueError):
                build(root, out=root)
            with self.assertRaises(ValueError):
                build(root, out=root / "third_party/godot-demo-projects")

if __name__ == "__main__":
    unittest.main()
