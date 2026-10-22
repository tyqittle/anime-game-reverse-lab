"""Synthetic APK tests. No copyrighted APK, login or production traffic."""
import tempfile
import unittest
import zipfile
from pathlib import Path
from erlab.apk_audit import inspect, report

class APKScanTests(unittest.TestCase):
    def test_detect_hints_without_leaking_url_queries(self):
        with tempfile.TemporaryDirectory() as d:
            apk = Path(d) / "test.apk"
            with zipfile.ZipFile(apk, "w") as z:
                z.writestr("AndroidManifest.xml", "fixture")
                z.writestr("lib/arm64-v8a/libunity.so", "fixture")
                z.writestr("classes.dex", b"Lokhttp3/Call; https://api.example.org/secret?token=DO_NOT_SHARE")
            result = inspect(apk)
            self.assertIn("Unity", result["engine_hints_not_verified"])
            self.assertEqual(result["candidate_http_hosts_not_verified"], ["api.example.org"])
            self.assertIn("okhttp", result["network_sdk_string_hints"])
            self.assertNotIn("DO_NOT_SHARE", str(result))
            self.assertNotIn("secret", report(result))
            self.assertEqual(result["ssl_pinning"], "unknown")

    def test_unknown_is_not_misclassified(self):
        with tempfile.TemporaryDirectory() as d:
            apk = Path(d) / "blank.apk"
            with zipfile.ZipFile(apk, "w") as z:
                z.writestr("assets/dummy", b"x")
            self.assertEqual(inspect(apk)["engine_hints_not_verified"], {})

    def test_reject_non_zip(self):
        with tempfile.TemporaryDirectory() as d:
            apk = Path(d) / "bad.apk"
            apk.write_bytes(b"not an APK")
            with self.assertRaises(ValueError):
                inspect(apk)

if __name__ == "__main__":
    unittest.main()
