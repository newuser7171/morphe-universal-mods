package app.template.patches.shared

/**
 * Maps a compatibility scan to an explicit, reviewable patch plan.
 * Never applies a patch based only on a heuristic match.
 */
object PatchPlanner {
    enum class Module {
        BILLING_DIAGNOSTICS,
        ALTERNATIVE_BILLING_DIAGNOSTICS,
        FEATURE_FLAG_INSPECTION,
        OFFLINE_SAVE_INSPECTION
    }

    data class Plan(
        val suggested: Set<Module>,
        val requiresManualReview: Boolean,
        val warnings: List<String>
    )

    fun plan(report: CompatibilityScanner.Report): Plan {
        val suggestions = buildSet {
            if (CompatibilityScanner.Signal.GOOGLE_PLAY_BILLING in report.signals) {
                add(Module.BILLING_DIAGNOSTICS)
            }
            if (CompatibilityScanner.Signal.ALTERNATIVE_BILLING in report.signals) {
                add(Module.ALTERNATIVE_BILLING_DIAGNOSTICS)
            }
            if (CompatibilityScanner.Signal.LOCAL_FEATURE_FLAGS in report.signals) {
                add(Module.FEATURE_FLAG_INSPECTION)
            }
            if (CompatibilityScanner.Signal.LOCAL_GAME_STATE in report.signals) {
                add(Module.OFFLINE_SAVE_INSPECTION)
            }
        }
        return Plan(
            suggested = suggestions,
            requiresManualReview = true,
            warnings = report.warnings + if (
                CompatibilityScanner.Signal.REMOTE_ENTITLEMENTS in report.signals
            ) listOf("Remote entitlements cannot be inferred from local APK content.") else emptyList()
        )
    }
}
