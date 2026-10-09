# Hill Climb Racing 1.72.2 — Grip and motor torque experiment

The source APKS bundle must contain base.apk and the ARM64, English, and XXHDPI split APKs.

Two candidate vehicle models:
- assets/vehicles/badcar_model.json
- assets/vehicles/boringcar_model.json

For both models:
- Multiply friction by 4 on frontWheel and rearWheel fixtures, capped at 10.
- Multiply maxMotorTorque by 2 on frontSpring and rearSpring joints when enableMotor is true.
- Keep all other fields unchanged.

Observed original maxMotorTorque: 500 on each of four powered wheel joints.
Experimental replacement: 1000.

These are serialized Box2D joint torque limits. They are not verified engine-power or acceleration parameters; the game can override them at runtime. Gameplay effect requires testing.

When rebuilding the APKS archive, preserve all four components and remove obsolete META-INF signature metadata from modified base.apk. Sign every split with the same certificate before installing. A different certificate cannot update the Play Store-signed app in place. Do not uninstall before backing up progress.
