#!/usr/bin/env python3
"""Inspect Hill Climb Racing APK asset structure without changing the APK."""
import argparse
import json
import sys
import zipfile

TARGETS = (
    "assets/garage/garage_physics.json",
    "assets/vehicles/projectcar_model.json",
    "assets/vehicles/modifier_props.json",
)

def inspect(path):
    with zipfile.ZipFile(path) as apk:
        names = set(apk.namelist())
        report = {"apk": str(path), "assets": {}, "has_arm64_game_library": "lib/arm64-v8a/libgame.so" in names}
        for name in TARGETS:
            if name not in names:
                report["assets"][name] = {"present": False}
                continue
            data = json.loads(apk.read(name))
            report["assets"][name] = {
                "present": True,
                "top_level_keys": sorted(data.keys()),
                "body_count": len(data.get("body", [])) if isinstance(data.get("body"), list) else None,
                "joint_count": len(data.get("joint", [])) if isinstance(data.get("joint"), list) else None,
            }
        return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("apk")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.apk), indent=2))
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f"APK inspection failed: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
