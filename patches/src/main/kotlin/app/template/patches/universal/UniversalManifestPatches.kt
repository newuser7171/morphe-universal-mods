package app.template.patches.universal

import app.morphe.patcher.patch.resourcePatch
import app.morphe.patcher.patch.stringOption
import org.w3c.dom.Element

@Suppress("unused")
val universalEnableDebuggingPatch = resourcePatch(
    name = "Universal - Enable Debugging",
    description = "Sets android:debuggable on the application. May reduce security and performance.",
    default = false,
) {
    execute {
        document("AndroidManifest.xml").use { doc ->
            val apps = doc.getElementsByTagName("application")
            require(apps.length == 1) { "Expected exactly one application element" }
            (apps.item(0) as Element).setAttribute("android:debuggable", "true")
        }
    }
}

@Suppress("unused")
val universalCustomAppNamePatch = resourcePatch(
    name = "Universal - Custom App Name",
    description = "Sets a literal launcher application label. Launcher activity-specific labels may override it.",
    default = false,
) {
    val name = stringOption(
        key = "custom_app_name",
        default = "My App",
        title = "Custom app name",
        description = "Literal name to show in supported launchers.",
        required = true,
    ) { value -> value != null && value.isNotBlank() && value.length <= 80 }

    execute {
        document("AndroidManifest.xml").use { doc ->
            val apps = doc.getElementsByTagName("application")
            require(apps.length == 1) { "Expected exactly one application element" }
            (apps.item(0) as Element).setAttribute("android:label", requireNotNull(name.value))
        }
    }
}
