package app.template.patches.shared

import app.morphe.patcher.patch.ApkFileType
import app.morphe.patcher.patch.AppTarget
import app.morphe.patcher.patch.Compatibility

/**
 * Version-specific target definition. Fingerprints must be verified against
 * an APK before any modifying patch is enabled.
 */
object HillClimbTarget {
    val COMPATIBILITY = Compatibility(
        name = "Hill Climb Racing",
        packageName = "com.fingersoft.hillclimb",
        apkFileType = ApkFileType.APK,
        appIconColor = 0xE8A62B,
        targets = listOf(AppTarget(version = "1.72.2"))
    )
}
