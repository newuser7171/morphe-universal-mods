import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "build_hillclimb_splits.py"
spec = importlib.util.spec_from_file_location("hillclimb_splits", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SplitPhysicsTests(unittest.TestCase):
    def test_grip_and_torque(self):
        sample = {
            "body": [
                {"name": "frontWheel", "fixture": [{"friction": 0.5}]},
                {"name": "rearWheel", "fixture": [{"friction": 0.5}]}
            ],
            "joint": [
                {"name": "frontSpring", "enableMotor": True, "maxMotorTorque": 500},
                {"name": "rearSpring", "enableMotor": True, "maxMotorTorque": 500}
            ]
        }
        result, wheels, motors = mod.patch_model(json.dumps(sample).encode(), 4, 2)
        parsed = json.loads(result)
        self.assertEqual((wheels, motors), (2, 2))
        self.assertEqual([x["fixture"][0]["friction"] for x in parsed["body"]], [2.0, 2.0])
        self.assertEqual([x["maxMotorTorque"] for x in parsed["joint"]], [1000, 1000])

    def test_fails_closed_on_unknown_layout(self):
        with self.assertRaises(ValueError):
            mod.patch_model(b'{"body":[],"joint":[]}', 4, 2)

if __name__ == "__main__":
    unittest.main()
