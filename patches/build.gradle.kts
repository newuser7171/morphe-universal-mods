group = "com.newuser7171.morphe"

patches {
    // TODO: Update this section with your project details.
    about {
        name = "Universal Mods"
        description = "Modular Android app and offline-game patches with compatibility-aware targeting"
        source = "https://github.com/newuser7171/morphe-universal-mods"
        author = "newuser7171"
        contact = "na"
        website = "https://github.com/newuser7171/morphe-universal-mods"
        license = "GPLv3"
    }
}

// Separate configuration so gson is available at runtime for the
// generatePatchesList task but never bundled into the APK.
val patchListGeneratorClasspath = configurations.create("patchListGeneratorClasspath")

dependencies {
    compileOnly(libs.gson)
    patchListGeneratorClasspath(libs.gson)
}

tasks {
    register<JavaExec>("generatePatchesList") {
        description = "Build patch with patch list"

        dependsOn(build)

        classpath = sourceSets["main"].runtimeClasspath + patchListGeneratorClasspath
        mainClass.set("util.PatchListGeneratorKt")
    }

    // Used by gradle-semantic-release-plugin.
    publish {
        dependsOn("generatePatchesList")
    }
}
