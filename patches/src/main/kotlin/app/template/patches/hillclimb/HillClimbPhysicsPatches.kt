package app.template.patches.hillclimb

import app.morphe.patcher.patch.ResourcePatchContext
import app.morphe.patcher.patch.floatSliderOption
import app.morphe.patcher.patch.rawResourcePatch
import app.template.patches.shared.HillClimbTarget
import com.google.gson.JsonParser
import com.google.gson.JsonPrimitive
import java.nio.charset.StandardCharsets

private val models = listOf(
    "assets/vehicles/badcar_model.json",
    "assets/vehicles/boringcar_model.json",
)

private fun ResourcePatchContext.updateModels(
    grip: Float? = null,
    torque: Float? = null,
) {
    for (path in models) {
        require(path in listApkEntries("assets/vehicles/")) {
            "Expected Hill Climb Racing 1.72.2 model is missing: $path"
        }
        val file = this[path]
        val root = JsonParser.parseString(file.readText(StandardCharsets.UTF_8)).asJsonObject
        var changed = 0
        if (grip != null) {
            for (body in root.getAsJsonArray("body")) {
                val obj = body.asJsonObject
                if (obj.get("name")?.asString !in setOf("frontWheel", "rearWheel")) continue
                for (fixture in obj.getAsJsonArray("fixture")) {
                    val item = fixture.asJsonObject
                    val original = item.get("friction") ?: continue
                    item.add("friction", JsonPrimitive((original.asDouble * grip).coerceIn(0.0, 10.0)))
                    changed++
                }
            }
        }
        if (torque != null) {
            for (joint in root.getAsJsonArray("joint")) {
                val obj = joint.asJsonObject
                if (obj.get("name")?.asString !in setOf("frontSpring", "rearSpring")) continue
                if (obj.get("enableMotor")?.asBoolean != true) continue
                val original = obj.get("maxMotorTorque") ?: continue
                obj.add("maxMotorTorque", JsonPrimitive(original.asDouble * torque))
                changed++
            }
        }
        require(changed == 2) { "Unexpected $path physics layout: found $changed expected fields, expected 2" }
        file.writeText(root.toString(), StandardCharsets.UTF_8)
    }
}

@Suppress("unused")
val hillClimbWheelGripPatch = rawResourcePatch(
    name = "Hill Climb Racing - Wheel Grip",
    description = "Adjust starter vehicle wheel friction (version 1.72.2).",
    default = false,
) {
    compatibleWith(HillClimbTarget.COMPATIBILITY)
    val multiplier = floatSliderOption(
        key = "wheel_grip_multiplier",
        min = 0.5f,
        max = 8f,
        default = 4f,
        step = 0.5f,
        title = "Wheel grip multiplier",
    )
    execute {
        updateModels(grip = requireNotNull(multiplier.value))
    }
}

@Suppress("unused")
val hillClimbMotorTorquePatch = rawResourcePatch(
    name = "Hill Climb Racing - Motor Torque",
    description = "Adjust starter vehicle wheel-joint torque limit (version 1.72.2).",
    default = false,
) {
    compatibleWith(HillClimbTarget.COMPATIBILITY)
    val multiplier = floatSliderOption(
        key = "motor_torque_multiplier",
        min = 0.5f,
        max = 5f,
        default = 2f,
        step = 0.5f,
        title = "Motor torque multiplier",
    )
    execute {
        updateModels(torque = requireNotNull(multiplier.value))
    }
}
