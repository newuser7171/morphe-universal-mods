#!/usr/bin/env python3
"""Create a Hill Climb Racing 1.72.2 physics experiment APK.

Only changes friction on fixtures inside a selected vehicle model JSON.
The output APK must be re-signed before installation.
"""
import argparse
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

ALLOWED = {
    "projectcar": "assets/vehicles/projectcar_model.json",
    "badcar": "assets/vehicles/badcar_model.json",
    "boringcar": "assets/vehicles/boringcar_model.json",
    "fastbike": "assets/vehicles/fastbike_model.json",
    "ufo": "assets/vehicles/ufo_model.json",
}

def modify(data: bytes, multiplier: float):
    doc = json.loads(data)
    if not isinstance(doc, dict) or not isinstance(doc.get("body"), list):
        raise ValueError("Unsupported vehicle model JSON structure")
    count = 0
    for body in doc["body"]:
        if not isinstance(body, dict):
            continue
        for fixture in body.get("fixture", []):
            if not isinstance(fixture, dict):
                continue
            old = fixture.get("friction")
            if isinstance(old, (int, float)) and not isinstance(old, bool):
                fixture["friction"] = round(max(0.0, min(float(old) * multiplier, 10.0)), 6)
                count += 1
    if not count:
        raise ValueError("No friction fields found; refusing unchanged output")
    return json.dumps(doc, separators=(",", ":"), ensure_ascii=False).encode("utf-8"), count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("apk", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--vehicle", choices=sorted(ALLOWED), default="projectcar")
    parser.add_argument("--friction-multiplier", type=float, default=1.25)
    args = parser.parse_args()
    if not math.isfinite(args.friction_multiplier) or not 0.1 <= args.friction_multiplier <= 3:
        parser.error("friction multiplier must be between 0.1 and 3")
    if args.apk.resolve() == args.output.resolve():
        parser.error("output must differ from input")
    target = ALLOWED[args.vehicle]
    with zipfile.ZipFile(args.apk) as source:
        original = source.read(target)
        replacement, count = modify(original, args.friction_multiplier)
        with zipfile.ZipFile(args.output, "w") as dest:
            for info in source.infolist():
                if info.filename.startswith("META-INF/") and info.filename.upper().endswith((".RSA", ".DSA", ".EC", ".SF")):
                    continue
                dest.writestr(info, replacement if info.filename == target else source.read(info.filename))
    print(json.dumps({
        "target": target,
        "fixtures_modified": count,
        "original_sha256": hashlib.sha256(original).hexdigest(),
        "modified_sha256": hashlib.sha256(replacement).hexdigest(),
        "output": str(args.output),
        "note": "Experimental APK; re-sign before installing. Gameplay effect unverified."
    }, indent=2))

if __name__ == "__main__":
    main()
