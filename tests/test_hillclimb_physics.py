import importlib.util
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "modify_hillclimb_physics.py"
spec = importlib.util.spec_from_file_location("hillclimb_physics", SCRIPT)
physics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(physics)

class PhysicsTests(unittest.TestCase):
    def test_friction_multiplier(self):
        original = {"body": [{"fixture": [{"friction": 0.4}, {"friction": 2.0}]}]}
        changed, count = physics.modify(json.dumps(original).encode(), 1.5)
        result = json.loads(changed)
        self.assertEqual(count, 2)
        self.assertEqual([x["friction"] for x in result["body"][0]["fixture"]], [0.6, 3.0])
        self.assertEqual(original["body"][0]["fixture"][0]["friction"], 0.4)

    def test_refuses_unknown_structure(self):
        with self.assertRaises(ValueError):
            physics.modify(b'{"unexpected":true}', 1.5)

    def test_refuses_no_friction(self):
        with self.assertRaises(ValueError):
            physics.modify(b'{"body":[{"fixture":[{"density":1}]}]}', 1.5)

    def test_clamps_friction(self):
        changed, _ = physics.modify(b'{"body":[{"fixture":[{"friction":9}]}]}', 2)
        self.assertEqual(json.loads(changed)["body"][0]["fixture"][0]["friction"], 10.0)

if __name__ == "__main__":
    unittest.main()
