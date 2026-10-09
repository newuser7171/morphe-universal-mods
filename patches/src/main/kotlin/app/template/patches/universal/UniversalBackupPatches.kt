package app.template.patches.universal

import app.morphe.patcher.patch.resourcePatch
import org.w3c.dom.Element

@Suppress("unused")
val universalAllowBackupPatch = resourcePatch(
    name = "Universal - Allow Android Backup",
    description = "Sets android:allowBackup=true. Android backup rules and device policy may still prevent backups. Backups may contain sensitive app data.",
    default = false,
) {
    execute {
        document("AndroidManifest.xml").use { doc ->
            val apps = doc.getElementsByTagName("application")
            require(apps.length == 1) { "Expected exactly one application element" }
            (apps.item(0) as Element).setAttribute("android:allowBackup", "true")
        }
    }
}

@Suppress("unused")
val universalDisableBackupPatch = resourcePatch(
    name = "Universal - Disable Android Backup",
    description = "Sets android:allowBackup=false. Some device-to-device transfers may use separate rules.",
    default = false,
) {
    execute {
        document("AndroidManifest.xml").use { doc ->
            val apps = doc.getElementsByTagName("application")
            require(apps.length == 1) { "Expected exactly one application element" }
            (apps.item(0) as Element).setAttribute("android:allowBackup", "false")
        }
    }
}
