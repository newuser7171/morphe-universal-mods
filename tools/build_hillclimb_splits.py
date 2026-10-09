#!/usr/bin/env python3
"""Build a configurable unsigned Hill Climb Racing 1.72.2 APKS package."""
import argparse
import io
import json
import math
import zipfile
from pathlib import Path

MODELS = ("assets/vehicles/badcar_model.json", "assets/vehicles/boringcar_model.json")
WHEELS = {"frontWheel", "rearWheel"}
MOTORS = {"frontSpring", "rearSpring"}
SPLITS = {"base.apk", "split_config.arm64_v8a.apk", "split_config.en.apk", "split_config.xxhdpi.apk"}

def patch_model(data, grip, torque):
    doc = json.loads(data)
    friction_count = torque_count = 0
    for body in doc["body"]:
        if body.get("name") not in WHEELS:
            continue
        for fixture in body.get("fixture", []):
            old = fixture.get("friction")
            if isinstance(old, (int, float)) and not isinstance(old, bool):
                fixture["friction"] = round(min(10, max(0, old * grip)), 6)
                friction_count += 1
    for joint in doc["joint"]:
        if joint.get("name") in MOTORS and joint.get("enableMotor") is True:
            old = joint.get("maxMotorTorque")
            if isinstance(old, (int, float)) and not isinstance(old, bool):
                joint["maxMotorTorque"] = round(old * torque, 6)
                torque_count += 1
    if friction_count != 2 or torque_count != 2:
        raise ValueError(f"Unexpected model structure: {friction_count} wheel fixtures, {torque_count} motors")
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode(), friction_count, torque_count

def build(source, output, grip, torque):
    if source.resolve() == output.resolve() or output.exists():
        raise ValueError("Output must be new and different from input")
    with zipfile.ZipFile(source) as bundle:
        missing = SPLITS - set(bundle.namelist())
        if missing:
            raise ValueError(f"Missing required APK splits: {sorted(missing)}")
        with zipfile.ZipFile(io.BytesIO(bundle.read("base.apk"))) as base:
            replacements = {}
            counts = {}
            for name in MODELS:
                replacements[name], f, t = patch_model(base.read(name), grip, torque)
                counts[name] = {"wheel_friction_fields": f, "motor_torque_fields": t}
            patched_base = io.BytesIO()
            with zipfile.ZipFile(patched_base, "w") as target:
                for entry in base.infolist():
                    upper = entry.filename.upper()
                    if upper.startswith("META-INF/") and upper.endswith((".RSA", ".DSA", ".EC", ".SF", "MANIFEST.MF")):
                        continue
                    target.writestr(entry, replacements.get(entry.filename, base.read(entry.filename)))
        with zipfile.ZipFile(output, "w") as out:
            for entry in bundle.infolist():
                out.writestr(entry, patched_base.getvalue() if entry.filename == "base.apk" else bundle.read(entry.filename))
    with zipfile.ZipFile(output) as out:
        if out.testzip() is not None:
            raise ValueError("Output APKS archive failed integrity verification")
        with zipfile.ZipFile(io.BytesIO(out.read("base.apk"))) as base:
            if base.testzip() is not None:
                raise ValueError("Modified base APK failed integrity verification")
            for name, expected in replacements.items():
                if base.read(name) != expected:
                    raise ValueError(f"Modified model mismatch: {name}")
    return counts

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_apks", type=Path)
    parser.add_argument("output_apks", type=Path)
    parser.add_argument("--grip", type=float, default=4.0)
    parser.add_argument("--torque", type=float, default=2.0)
    args = parser.parse_args()
    if not all(math.isfinite(x) for x in (args.grip, args.torque)) or not (0.5 <= args.grip <= 8 and 0.5 <= args.torque <= 5):
        parser.error("grip must be 0.5–8 and torque 0.5–5")
    print(json.dumps(build(args.input_apks, args.output_apks, args.grip, args.torque), indent=2))
    print("Unsigned APKS created; sign every split with the same certificate.")

if __name__ == "__main__":
    main()
