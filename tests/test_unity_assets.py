"""Adapter tests with mocked external parser; no proprietary game samples."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from erlab import unity_assets


class TestUnityAssets(unittest.TestCase):
    def test_sanitize(self):
        self.assertEqual(unity_assets._name('../../evil/portrait'), 'portrait')
        self.assertEqual(unity_assets._name('..\\..\\evil.png'), 'evil.png')
        self.assertEqual(unity_assets._name('???'), '___')

    def test_inspect(self):
        objs = [SimpleNamespace(type=SimpleNamespace(name=t), path_id=i) for i, t in enumerate(['Texture2D', 'Mesh', 'Sprite'])]
        with patch.object(unity_assets, '_objects', return_value=iter(objs)):
            result = unity_assets.inspect(Path('mock.bundle'), {'Texture2D', 'Sprite'})
        self.assertEqual(result['counts'], {'Texture2D': 1, 'Sprite': 1})
        self.assertFalse(result['truncated'])

    def test_inspect_limit(self):
        objs = [SimpleNamespace(type=SimpleNamespace(name='Sprite'), path_id=i) for i in range(3)]
        with patch.object(unity_assets, '_objects', return_value=iter(objs)):
            result = unity_assets.inspect(Path('mock.bundle'), limit=2)
        self.assertEqual(len(result['objects']), 2)
        self.assertTrue(result['truncated'])

    def test_export_text(self):
        obj = SimpleNamespace(type=SimpleNamespace(name='TextAsset'), path_id=42,
                              parse_as_object=lambda: SimpleNamespace(m_Name='../hello', m_Script='你好'))
        with tempfile.TemporaryDirectory() as td:
            with patch.object(unity_assets, '_objects', return_value=iter([obj])):
                result = unity_assets.export(Path('fixture.bundle'), Path(td))
            self.assertEqual(len(result['exported']), 1)
            f = Path(result['exported'][0])
            self.assertEqual(f.read_text(encoding='utf-8'), '你好')
            self.assertTrue(f.resolve().is_relative_to(Path(td).resolve()))

    def test_reject_unsupported_and_bad_limit(self):
        with self.assertRaises(ValueError):
            unity_assets.export(Path('none'), Path('out'), types={'MonoBehaviour'})
        with self.assertRaises(ValueError):
            unity_assets.inspect(Path('none'), limit=0)

    def test_missing_file(self):
        with self.assertRaises(ValueError):
            list(unity_assets._objects(Path('definitely-missing.bundle')))


if __name__ == '__main__':
    unittest.main()
