# Sagarmatha Launcher

Android launcher project (Phase 5, version 1.5.0).

## Source upload required

Upload the project archive named exactly:

`Sagarmatha-Launcher-Phase5-Android-Studio-Project.zip`

to the repository root. The archive must contain `settings.gradle.kts` and `app/build.gradle.kts` at its root.

## Build APK

GitHub Actions workflow: **Android APK Build**.

After the ZIP is pushed to `main`, the workflow extracts the Android Studio project, runs `gradle assembleDebug`, and publishes the debug APK as an Actions artifact.

Note: The project has not yet been compiled or device-tested in this environment. The first GitHub Actions build will provide the actual compile result.
