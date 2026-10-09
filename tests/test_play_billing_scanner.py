import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.inspect_play_billing import inspect, scan_apk_bytes


def make_zip(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        for name, data in files.items():
            z.writestr(name, data)
    return buffer.getvalue()


class BillingScannerTests(unittest.TestCase):
    def test_detects_billing_client(self):
        apk = make_zip({"classes.dex": b"com/android/billingclient/api/BillingClient"})
        result = scan_apk_bytes(apk, "base.apk")
        self.assertTrue(result["billing_integration_detected"])
        self.assertTrue(result["markers"]["billing_client"])

    def test_does_not_claim_billing_without_marker(self):
        apk = make_zip({"classes.dex": b"some other dex content"})
        self.assertFalse(scan_apk_bytes(apk, "base.apk")["billing_integration_detected"])

    def test_apks_split_scan(self):
        base = make_zip({"classes.dex": b"com/android/billingclient/api/Purchase"})
        config = make_zip({"classes.dex": b"other"})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.apks"
            path.write_bytes(make_zip({"base.apk": base, "split_config.apk": config}))
            result = inspect(path)
            self.assertEqual(len(result["results"]), 2)
            self.assertTrue(result["results"][0]["billing_integration_detected"])
            self.assertFalse(result["results"][1]["billing_integration_detected"])


if __name__ == "__main__":
    unittest.main()
