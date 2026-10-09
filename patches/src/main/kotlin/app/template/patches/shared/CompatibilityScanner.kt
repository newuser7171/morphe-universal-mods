package app.template.patches.shared

/**
 * Conservative compatibility classification for patch authors.
 * This module only reports signals; it never grants purchases or entitlements.
 */
object CompatibilityScanner {
    enum class Signal {
        GOOGLE_PLAY_BILLING,
        ALTERNATIVE_BILLING,
        LOCAL_FEATURE_FLAGS,
        LOCAL_GAME_STATE,
        REMOTE_ENTITLEMENTS
    }

    data class Report(
        val signals: Set<Signal>,
        val candidatePatches: List<String>,
        val warnings: List<String>
    )

    fun scan(
        dexDescriptors: Collection<String>,
        manifestText: String = "",
        resourceNames: Collection<String> = emptyList()
    ): Report {
        val descriptors = dexDescriptors.map { it.lowercase() }
        val resources = resourceNames.map { it.lowercase() }
        val manifest = manifestText.lowercase()
        val signals = mutableSetOf<Signal>()

        if (descriptors.any { it.contains("com/android/billingclient/") } ||
            manifest.contains("com.android.vending.billing")) {
            signals += Signal.GOOGLE_PLAY_BILLING
        }
        if (descriptors.any { it.contains("amazon/device/iap/") }) {
            signals += Signal.ALTERNATIVE_BILLING
        }
        if (resources.any { it.contains("feature_flag") || it.contains("experiment") }) {
            signals += Signal.LOCAL_FEATURE_FLAGS
        }
        if (resources.any { it.contains("save_game") || it.contains("player_progress") }) {
            signals += Signal.LOCAL_GAME_STATE
        }
        if (descriptors.any { it.contains("entitlement") || it.contains("subscriptionapi") }) {
            signals += Signal.REMOTE_ENTITLEMENTS
        }

        val candidates = buildList {
            if (Signal.LOCAL_FEATURE_FLAGS in signals) add("Feature flag inspection")
            if (Signal.LOCAL_GAME_STATE in signals) add("Offline game customization")
            if (Signal.GOOGLE_PLAY_BILLING in signals) add("Billing integration diagnostics")
            if (Signal.ALTERNATIVE_BILLING in signals) add("Alternative billing diagnostics")
        }
        val warnings = buildList {
            if (Signal.REMOTE_ENTITLEMENTS in signals) {
                add("Potential server-side entitlement validation; local patches may not apply.")
            }
            add("Heuristic results require manual validation before enabling a patch.")
        }
        return Report(signals, candidates, warnings)
    }
}
