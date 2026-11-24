# Sagarmatha Launcher

Android launcher project, Phase 5 (version 1.5.0).

## Project source

The Phase 5 Android Studio project archive is stored in two Base64 parts under `upload-parts/`. GitHub Actions joins and decodes these parts into the original ZIP, validates the archive, and extracts the Android project before building.

## Build APK

Open **Actions → Android APK Build** to view the build. The workflow runs `gradle assembleDebug` with JDK 17 and uploads the resulting debug APK as an Actions artifact.

The project has not been compiled or device-tested locally. Treat the first Actions run as the authoritative compile check.
