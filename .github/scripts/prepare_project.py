from pathlib import Path

root = Path("android-project")
root_gradle = root / "build.gradle.kts"
app_gradle = root / "app/build.gradle.kts"
main_file = root / "app/src/main/java/np/sagarmatha/launcher/MainActivity.kt"
calendar_file = root / "app/src/main/java/np/sagarmatha/launcher/NepaliCalendarService.kt"

for required in (root_gradle, app_gradle, main_file, calendar_file):
    if not required.is_file():
        raise SystemExit(f"Missing expected project file: {required}")

# Use a mutually compatible Android/Kotlin toolchain and SDK level required by
# the published Nepali Date Picker 2.6.2 Android artifact.
rg = root_gradle.read_text()
rg = rg.replace('id("com.android.application") version "8.6.1"', 'id("com.android.application") version "8.13.2"')
rg = rg.replace('id("org.jetbrains.kotlin.android") version "2.0.21"', 'id("org.jetbrains.kotlin.android") version "2.3.0"')
if 'version "8.13.2"' not in rg or 'version "2.3.0"' not in rg:
    raise SystemExit("Could not apply the expected root Gradle plugin versions")
root_gradle.write_text(rg)

ag = app_gradle.read_text()
ag = ag.replace("compileSdk = 35", "compileSdk = 36")
ag = ag.replace(
    'implementation("io.github.shivathapaa:nepali-date-picker:2.6.2")',
    'implementation("io.github.shivathapaa:nepali-date-picker-android:2.6.2")'
)
old = '    kotlinOptions { jvmTarget = "17" }\n}'
new = '''}

kotlin {
    compilerOptions {
        jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
    }
}'''
if old in ag:
    ag = ag.replace(old, new, 1)
elif "compilerOptions" not in ag:
    raise SystemExit("Cannot find original Kotlin JVM target block in app Gradle file")
app_gradle.write_text(ag)

# Android EditText exposes setSingleLine(); the invalid widget-host extra is
# not part of the public AppWidgetManager API.
ms = main_file.read_text()
ms = ms.replace("singleLine = true", "setSingleLine(true)")
ms = ms.replace('            putExtra(AppWidgetManager.EXTRA_APPWIDGET_HOST_ID, widgetHostId)\n', "")
main_file.write_text(ms)

# v2.6.2 source confirms these package names and formatting overloads.
calendar_file.write_text("""package np.sagarmatha.launcher

import dev.shivathapaa.nepalidatepickerkmp.calendar_model.NepaliDateConverter
import dev.shivathapaa.nepalidatepickerkmp.data.NepaliDateFormatStyle
import dev.shivathapaa.nepalidatepickerkmp.data.NepaliDateLocale
import dev.shivathapaa.nepalidatepickerkmp.data.NepaliDatePickerLang

object NepaliCalendarService {
    fun todayNepali(nepali: Boolean): String {
        val locale = NepaliDateLocale(
            language = if (nepali) NepaliDatePickerLang.NEPALI else NepaliDatePickerLang.ENGLISH,
            dateFormat = NepaliDateFormatStyle.FULL
        )
        return NepaliDateConverter.formatNepaliDate(
            NepaliDateConverter.todayNepaliCalendar,
            locale
        )
    }

    fun todayEnglish(): String {
        val locale = NepaliDateLocale(
            language = NepaliDatePickerLang.ENGLISH,
            dateFormat = NepaliDateFormatStyle.FULL
        )
        return NepaliDateConverter.formatEnglishDate(
            NepaliDateConverter.todayEnglishCalendar,
            locale
        )
    }
}
""")

ms = main_file.read_text()
if "singleLine = true" in ms:
    raise SystemExit("Unfixed singleLine property remains")
if "EXTRA_APPWIDGET_HOST_ID" in ms:
    raise SystemExit("Unfixed EXTRA_APPWIDGET_HOST_ID remains")
if "NepaliDateConverter.todayEnglish()" in calendar_file.read_text():
    raise SystemExit("Invalid Nepali date converter call remains")

print("Source preparation passed all structural checks.")

# Apply maintained launcher feature patch after reconstructing the verified base ZIP.
from pathlib import Path as _Path
_feature_patch = _Path("launcher-patches/patch_launcher.py")
if not _feature_patch.is_file():
    raise SystemExit("Missing launcher feature patch")
exec(compile(_feature_patch.read_text(), str(_feature_patch), "exec"), {})

# Trigger rebuild after fixing v2.0.1 patch script quoting.
