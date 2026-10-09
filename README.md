# 👋🧩 Morphe Patches template

Template repository for Morphe Patches.

## ❓ About

Patches for apps I like.

<!-- TODO: Update this about section with a brief introduction/summary about this repo and what it offers. -->

### How to use these patches

Click here to add these patches to Morphe: https://morphe.software/add-source?github=newuser7171/morphe-universal-mods

## 🩹 Patches list

<!-- PATCHES_START EXPANDED -->
> **[v1.0.0-dev.6](https://github.com/newuser7171/morphe-universal-mods/releases/tag/v1.0.0-dev.6)**&nbsp;&nbsp;•&nbsp;&nbsp;`dev`&nbsp;&nbsp;•&nbsp;&nbsp;7 patches total
<details open>
<summary>📦 XYZ app&nbsp;&nbsp;•&nbsp;&nbsp;1 patch</summary>
<br>

**🎯 Supported versions:**

| 2.0.0 | 1.0.2 |
| :---: | :---: |

| 💊&nbsp;Patch | 📜&nbsp;Description | ⚙️&nbsp;Options |
|----------|----------------|-----------|
| [Example Patch](#example-patch) | Example patch to start with. |  |

</details>

<details open>
<summary>📦 Hill Climb Racing&nbsp;&nbsp;•&nbsp;&nbsp;2 patches</summary>
<br>

**🎯 Supported versions:**

| 1.72.2 |
| :---: |

| 💊&nbsp;Patch | 📜&nbsp;Description | ⚙️&nbsp;Options |
|----------|----------------|-----------|
| [Hill Climb Racing - Motor Torque](#hill-climb-racing-motor-torque) | Adjust starter vehicle wheel-joint torque limit (version 1.72.2). | • Motor torque multiplier |
| [Hill Climb Racing - Wheel Grip](#hill-climb-racing-wheel-grip) | Adjust starter vehicle wheel friction (version 1.72.2). | • Wheel grip multiplier |

</details>

<details open>
<summary>🌐 Universal&nbsp;&nbsp;•&nbsp;&nbsp;4 patches</summary>
<br>

| 💊&nbsp;Patch | 📜&nbsp;Description | ⚙️&nbsp;Options |
|----------|----------------|-----------|
| [Universal - Allow Android Backup](#universal-allow-android-backup) | Sets android:allowBackup=true. Android backup rules and device policy may still prevent backups. Backups may contain sensitive app data. |  |
| [Universal - Custom App Name](#universal-custom-app-name) | Sets a literal launcher application label. Launcher activity-specific labels may override it. | • Custom app name |
| [Universal - Disable Android Backup](#universal-disable-android-backup) | Sets android:allowBackup=false. Some device-to-device transfers may use separate rules. |  |
| [Universal - Enable Debugging](#universal-enable-debugging) | Sets android:debuggable on the application. May reduce security and performance. |  |

</details>

<!-- PATCHES_END -->

### 🛠️ Building locally

- Run `./gradlew buildAndroid`
- The built patches .mpp file is found in `patches/build/libs/patches-*.mpp`
- Patch the mpp file using [Morphe-Desktop](https://github.com/MorpheApp/morphe-desktop)
  like any other patch bundle.

See the [Morphe documentation](https://github.com/MorpheApp/morphe-documentation) for more information.

## 📜 License

UserXYZ Patches are licensed under the [GNU General Public License v3.0](LICENSE)
