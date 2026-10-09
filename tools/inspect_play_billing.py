#!/usr/bin/env python3
"""Inspect APK/APKS files for Google Play Billing integration indicators.

This is a read-only compatibility preflight, not a purchase bypass.
"""
import argparse
import json
import zipfile
from pathlib import Path

MARKERS = {
    "billing_client": b"com/android/billingclient/api/BillingClient",
    "billing_result": b"com/android/billingclient/api/BillingResult",
    "purchases_updated": b"com/android/billingclient/api/PurchasesUpdatedListener",
    "purchase": b"com/android/billingclient/api/Purchase",
    "legacy_aidl": b"com/android/vending/billing/IInAppBillingService",
}
BILLING_PERMISSION = b"com.android.vending.BILLING"


def scan_apk_bytes(data: bytes, label: str) -> dict:
    import io
    found = {key: False for key in MARKERS}
    dex_files = 0
    permission = False
    with zipfile.ZipFile(io.BytesIO(data)) as apk:
        for item in apk.infolist():
            if item.filename.startswith("classes") and item.filename.endswith(".dex"):
                dex_files += 1
                payload = apk.read(item)
                for key, marker in MARKERS.items():
                    found[key] |= marker in payload
            elif item.filename == "AndroidManifest.xml":
                permission = BILLING_PERMISSION in apk.read(item)
    return {
        "apk": label,
        "dex_files": dex_files,
        "markers": found,
        "billing_permission_visible": permission,
        "billing_integration_detected": any(found.values()),
    }


def inspect(path: Path) -> dict:
    results = []
    with zipfile.ZipFile(path) as archive:
        if path.suffix.lower() == ".apks":
            for entry in archive.infolist():
                if entry.filename.lower().endswith(".apk"):
                    results.append(scan_apk_bytes(archive.read(entry), entry.filename))
        else:
            results.append(scan_apk_bytes(path.read_bytes(), path.name))
    return {
        "file": str(path),
        "results": results,
        "note": "Static indicators only; obfuscation, native code and server validation may hide billing integrations. No purchases are modified.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path, help="APK or APKS bundle to inspect")
    args = parser.parse_args()
    print(json.dumps(inspect(args.apk), indent=2))


if __name__ == "__main__":
    main()
