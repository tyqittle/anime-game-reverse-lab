import unittest
from erlab.formats import identify_bytes

class TestFormats(unittest.TestCase):
    def test_png(self):
        self.assertEqual(identify_bytes(b"\x89PNG\r\n\x1a\n" + b"a"*100)["format"], "PNG image")

    def test_unityfs(self):
        self.assertEqual(identify_bytes(b"UnityFS\x00" + b"a"*20)["format"], "UnityFS asset bundle")

    def test_mp4(self):
        self.assertIn("MP4", identify_bytes(b"\x00\x00\x00\x18ftypisom")["format"])

    def test_unknown_not_guessed_by_extension(self):
        self.assertEqual(identify_bytes(b"123abc", ".png")["format"], "unknown")

    def test_riff_wave(self):
        self.assertEqual(identify_bytes(b"RIFF\x08\x00\x00\x00WAVEabc")["format"], "WAV audio")
