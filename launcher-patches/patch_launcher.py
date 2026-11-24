from pathlib import Path
root=Path("android-project")
main=root/"app/src/main/java/np/sagarmatha/launcher/MainActivity.kt"
s=main.read_text()
s=s.replace("import android.graphics.Color\n","import android.graphics.Color\nimport android.graphics.BitmapFactory\nimport android.graphics.drawable.BitmapDrawable\nimport android.net.Uri\n")
s=s.replace("    private var wallpaperIndex = 0\n","    private var wallpaperIndex = 0\n    private var customWallpaperUri = \"\"\n    private val requestWallpaperImage = 4103\n")
s=s.replace("background = NepalWallpaperDrawable(theme.background, theme.secondary, wallpaperTint(), wallpaperIndex)","background = homeBackground()")
s=s.replace("        top.addView(widgetShortcut)\n        root.addView(top)","""        top.addView(widgetShortcut)
        val settingsShortcut = TextView(this).apply {
            text = "⚙"; textSize = 22f; setTextColor(theme.accent); gravity = Gravity.CENTER
            setPadding(dp(10), 0, dp(2), 0); setOnClickListener { showSettingsScreen() }
        }
        top.addView(settingsShortcut)
        root.addView(top)""")
s=s.replace("x > .78f -> showDataSettings()","x > .78f -> showSettingsScreen()")
s=s.replace('        wallpaperIndex = prefs.getInt("wallpaper_index", 0).coerceIn(wallpapers.indices)\n','        wallpaperIndex = prefs.getInt("wallpaper_index", 0).coerceIn(wallpapers.indices)\n        customWallpaperUri = prefs.getString("custom_wallpaper_uri", "") ?: ""\n')
s=s.replace('            .putInt("wallpaper_index", wallpaperIndex)\n','            .putInt("wallpaper_index", wallpaperIndex)\n            .putString("custom_wallpaper_uri", customWallpaperUri)\n')
s=s.replace('''        addChoiceSection(if (nepaliMode) "वालपेपर" else "WALLPAPER", wallpapers, wallpaperIndex) { wallpaperIndex = it; savePreferences(); showAppearance() }''','''        addChoiceSection(if (nepaliMode) "वालपेपर" else "BUILT-IN WALLPAPERS", wallpapers, wallpaperIndex) {
            wallpaperIndex = it; customWallpaperUri = ""; savePreferences(); showAppearance()
        }
        root.addView(actionRow(if (nepaliMode) "फोटोबाट वालपेपर छान्नुहोस्" else "Choose wallpaper from photos") { chooseWallpaperImage() },
            LinearLayout.LayoutParams(-1, dp(52)).apply { topMargin = dp(8) })''')
s=s.replace('''        root.addView(folderButton, LinearLayout.LayoutParams(-1, dp(42)).apply { topMargin = dp(8) })
        val scroll = ScrollView(this);''','''        root.addView(folderButton, LinearLayout.LayoutParams(-1, dp(42)).apply { topMargin = dp(8) })
        root.addView(actionRow(if (nepaliMode) "डक व्यवस्थापन" else "Manage dock apps") { showDockManager() },
            LinearLayout.LayoutParams(-1, dp(42)).apply { topMargin = dp(7) })
        val scroll = ScrollView(this);''')
s=s.replace('''                            wallpaperIndex = (wallpaperIndex + if (dx < 0) 1 else wallpapers.size - 1) % wallpapers.size
                            renderHome(); true''','''                            wallpaperIndex = (wallpaperIndex + if (dx < 0) 1 else wallpapers.size - 1) % wallpapers.size
                            customWallpaperUri = ""; savePreferences(); renderHome(); true''')
s=s.replace('''        if (requestCode == requestPickWidget) {''','''        if (requestCode == requestWallpaperImage) {
            if (resultCode == RESULT_OK && data?.data != null) {
                val uri = data.data!!
                runCatching { contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION) }
                customWallpaperUri = uri.toString(); savePreferences()
            }
            if (showingDrawer) showAppearance() else renderHome()
        } else if (requestCode == requestPickWidget) {''')
methods = r'''
    private fun actionRow(label: String, action: () -> Unit): TextView = TextView(this).apply {
        text = label + "   ›"; textSize = 14f; setTextColor(theme.text); gravity = Gravity.CENTER_VERTICAL
        background = panel(); setPadding(dp(16), dp(10), dp(16), dp(10)); setOnClickListener { action() }
    }

    private fun showSettingsScreen() {
        showingDrawer = true; handler.removeCallbacks(clockTick)
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL; setPadding(dp(20), dp(18), dp(20), dp(16))
            background = GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, intArrayOf(theme.background, theme.secondary))
        }
        val header = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        header.addView(TextView(this).apply {
            text = if (nepaliMode) "सेटिङहरू" else "Launcher settings"
            textSize = 24f; setTextColor(theme.text); typeface = Typeface.DEFAULT_BOLD
        }, LinearLayout.LayoutParams(0, dp(54), 1f))
        header.addView(TextView(this).apply {
            text = "✕"; textSize = 22f; setTextColor(theme.text); gravity = Gravity.CENTER
            setOnClickListener { renderHome() }
        }, LinearLayout.LayoutParams(dp(44), dp(48)))
        root.addView(header)
        val scroll = ScrollView(this)
        val list = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        fun add(label: String, action: () -> Unit) {
            list.addView(actionRow(label, action), LinearLayout.LayoutParams(-1, dp(56)).apply { bottomMargin = dp(9) })
        }
        list.addView(TextView(this).apply {
            text = if (nepaliMode) "होम स्क्रिन अनुकूलन" else "PERSONALIZE YOUR HOME SCREEN"
            textSize = 11f; setTextColor(theme.accent); setPadding(0, dp(15), 0, dp(9))
        })
        add(if (nepaliMode) "वालपेपर र थिम" else "Wallpaper & appearance") { showAppearance() }
        add(if (nepaliMode) "फोटोबाट वालपेपर छान्नुहोस्" else "Choose photo wallpaper") { chooseWallpaperImage() }
        add(if (nepaliMode) "विजेट थप्नुहोस् / हटाउनुहोस्" else "Add / remove widgets") { showWidgetManager() }
        add(if (nepaliMode) "डकका एपहरू व्यवस्थापन" else "Manage dock apps") { showDockManager() }
        list.addView(TextView(this).apply {
            text = if (nepaliMode) "एप र भाषा" else "APPS & LANGUAGE"
            textSize = 11f; setTextColor(theme.accent); setPadding(0, dp(15), 0, dp(9))
        })
        add(if (nepaliMode) "सबै एपहरू" else "All apps") { showDrawer("") }
        add(if (nepaliMode) "भाषा बदल्नुहोस्" else "Switch language") {
            nepaliMode = !nepaliMode; savePreferences(); showSettingsScreen()
        }
        list.addView(TextView(this).apply {
            text = if (nepaliMode) "सेवा सेटिङ" else "SERVICES"
            textSize = 11f; setTextColor(theme.accent); setPadding(0, dp(15), 0, dp(9))
        })
        add(if (nepaliMode) "मौसम र समाचार" else "Weather & news") { showDataSettings() }
        scroll.addView(list); root.addView(scroll, LinearLayout.LayoutParams(-1, 0, 1f))
        setContentView(root)
    }

    private fun showDockManager() {
        showingDrawer = true; handler.removeCallbacks(clockTick)
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL; setPadding(dp(18), dp(18), dp(18), dp(14))
            background = GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, intArrayOf(theme.background, theme.secondary))
        }
        val header = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        header.addView(TextView(this).apply {
            text = if (nepaliMode) "डक व्यवस्थापन" else "Dock manager"
            textSize = 23f; setTextColor(theme.text); typeface = Typeface.DEFAULT_BOLD
        }, LinearLayout.LayoutParams(0, dp(50), 1f))
        header.addView(TextView(this).apply {
            text = "✕"; textSize = 22f; setTextColor(theme.text); gravity = Gravity.CENTER
            setOnClickListener { renderHome() }
        }, LinearLayout.LayoutParams(dp(42), dp(48)))
        root.addView(header)
        root.addView(actionRow(if (nepaliMode) "＋ एप थप्नुहोस्" else "＋ Add app") { showDockAppPicker() },
            LinearLayout.LayoutParams(-1, dp(52)).apply { bottomMargin = dp(12) })
        val scroll = ScrollView(this)
        val list = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        favorites.toList().forEachIndexed { index, pkg ->
            val app = appList.firstOrNull { it.packageName == pkg } ?: return@forEachIndexed
            val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL; background = panel(); setPadding(dp(8), dp(6), dp(6), dp(6)) }
            row.addView(ImageView(this).apply { setImageDrawable(app.icon) }, LinearLayout.LayoutParams(dp(38), dp(38)))
            row.addView(TextView(this).apply { text = app.label; textSize = 13f; setTextColor(theme.text); gravity = Gravity.CENTER_VERTICAL; setPadding(dp(8),0,0,0) }, LinearLayout.LayoutParams(0,dp(46),1f))
            row.addView(smallAction("↑") { if(index>0){favorites.removeAt(index);favorites.add(index-1,pkg);savePreferences();showDockManager()} })
            row.addView(smallAction("↓") { if(index< favorites.lastIndex){favorites.removeAt(index);favorites.add(index+1,pkg);savePreferences();showDockManager()} })
            row.addView(smallAction("×") { favorites.remove(pkg);savePreferences();showDockManager() })
            list.addView(row, LinearLayout.LayoutParams(-1, dp(60)).apply { bottomMargin = dp(8) })
        }
        scroll.addView(list); root.addView(scroll, LinearLayout.LayoutParams(-1,0,1f)); setContentView(root)
    }

    private fun showDockAppPicker() {
        val choices = appList.filter { !favorites.contains(it.packageName) }
        if (choices.isEmpty()) return
        AlertDialog.Builder(this)
            .setTitle(if (nepaliMode) "डकमा थप्ने एप" else "Add an app to dock")
            .setItems(choices.map { it.label }.toTypedArray()) { _, which ->
                if (favorites.size >= 5) favorites.removeAt(favorites.lastIndex)
                favorites.add(choices[which].packageName); savePreferences(); showDockManager()
            }.setNegativeButton(if (nepaliMode) "रद्द" else "Cancel", null).show()
    }

    private fun chooseWallpaperImage() {
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE); type = "image/*"
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)
        }
        @Suppress("DEPRECATION")
        startActivityForResult(intent, requestWallpaperImage)
    }

    private fun homeBackground(): android.graphics.drawable.Drawable {
        if (customWallpaperUri.isNotBlank()) runCatching {
            val stream = contentResolver.openInputStream(Uri.parse(customWallpaperUri))
            val bitmap = stream?.use { BitmapFactory.decodeStream(it) }
            if (bitmap != null) return BitmapDrawable(resources, bitmap)
        }
        return NepalWallpaperDrawable(theme.background, theme.secondary, wallpaperTint(), wallpaperIndex)
    }
'''
s=s.replace('    private fun showAppearance() {',methods+'\n    private fun showAppearance() {')
main.write_text(s)

manifest=root/"app/src/main/AndroidManifest.xml"
m=manifest.read_text().replace('''        android:label="Sagarmatha Launcher"
        android:theme="@style/AppTheme"''','''        android:label="Sagarmatha Launcher"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:theme="@style/AppTheme"''')
manifest.write_text(m)
styles=root/"app/src/main/res/values/styles.xml"
st=styles.read_text().replace('''        <item name="android:windowBackground">#10243A</item>''','''        <item name="android:windowBackground">#10243A</item>
        <item name="android:windowSplashScreenBackground">#10243A</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/ic_sagarmatha_foreground</item>
        <item name="android:windowSplashScreenIconBackgroundColor">#173653</item>''')
styles.write_text(st)
print("Launcher settings, photo wallpaper, dock management and icon metadata patched.")

# Register the HOME activity as a regular launcher app too.
# Do not search the whole manifest for CATEGORY_LAUNCHER: it may already
# occur inside <queries>, which does not register an app-drawer activity.
import re
manifest = root / "app/src/main/AndroidManifest.xml"
manifest_text = manifest.read_text()
main_home_pattern = re.compile(
    r'(<intent-filter>\s*<action android:name="android.intent.action.MAIN"\s*/>\s*'
    r'<category android:name="android.intent.category.HOME"\s*/>)'
)
if not re.search(
    r'<intent-filter>\s*<action android:name="android.intent.action.MAIN"\s*/>\s*'
    r'<category android:name="android.intent.category.HOME"\s*/>\s*'
    r'<category android:name="android.intent.category.LAUNCHER"\s*/>',
    manifest_text
):
    manifest_text, count = main_home_pattern.subn(
        r'\1\n            <category android:name="android.intent.category.LAUNCHER" />',
        manifest_text,
        count=1
    )
    if count != 1:
        raise SystemExit("Could not locate the HOME activity MAIN intent-filter")
if 'android:icon="@mipmap/ic_launcher"' not in manifest_text:
    manifest_text = manifest_text.replace(
        'android:label="Sagarmatha Launcher"',
        'android:label="Sagarmatha Launcher"\n        android:icon="@mipmap/ic_launcher"\n        android:roundIcon="@mipmap/ic_launcher_round"'
    )
manifest.write_text(manifest_text)

# Increment app version so Android treats this as a newer install/update.
app_gradle = root / "app/build.gradle.kts"
gradle_text = app_gradle.read_text()
gradle_text = gradle_text.replace("versionCode = 5", "versionCode = 7")
gradle_text = gradle_text.replace('versionName = "1.5.0"', 'versionName = "1.6.2"')
app_gradle.write_text(gradle_text)

print("Added LAUNCHER intent category and incremented app version to 1.6.2.")


# Correct edge-to-edge system bar spacing on Android 15+ and older Android.
# Keep launcher branding and controls below the notification/status bar.
main_file = root / "app/src/main/java/np/sagarmatha/launcher/MainActivity.kt"
source = main_file.read_text()
old_padding = "            setPadding(dp(20), dp(16), dp(20), dp(12))"
new_padding = """            setPadding(dp(20), dp(16), dp(20), dp(12))
            setOnApplyWindowInsetsListener { view, insets ->
                view.setPadding(
                    dp(20),
                    dp(16) + insets.systemWindowInsetTop,
                    dp(20),
                    dp(12) + insets.systemWindowInsetBottom
                )
                insets
            }"""
if new_padding not in source:
    if old_padding not in source:
        raise SystemExit("Home root padding anchor not found; refusing to patch status bar layout")
    source = source.replace(old_padding, new_padding, 1)

# Remove the text navigation footer and replace it with one clear app-drawer button.
footer_start = source.find('        val bottom = TextView(this).apply {')
footer_end_marker = '        root.addView(bottom)'
footer_end = source.find(footer_end_marker, footer_start)
if footer_start < 0 or footer_end < 0:
    raise SystemExit("Home footer anchor not found; refusing to patch app drawer shortcut")
footer_end += len(footer_end_marker)
footer = """        val footer = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(0, dp(7), 0, dp(2))
        }
        val appDrawerButton = TextView(this).apply {
            text = "▦"
            textSize = 27f
            setTextColor(theme.text)
            gravity = Gravity.CENTER
            contentDescription = if (nepaliMode) "एप ड्रअर खोल्नुहोस्" else "Open app drawer"
            background = rounded(Color.argb(58, 255, 255, 255), 18)
            setOnClickListener { showDrawer("") }
        }
        footer.addView(appDrawerButton, LinearLayout.LayoutParams(dp(54), dp(42)))
        root.addView(footer, LinearLayout.LayoutParams(-1, dp(48)))"""
source = source[:footer_start] + footer + source[footer_end:]

# Keep system status/navigation bars coordinated with the active launcher theme.
source = source.replace(
    '        window.navigationBarColor = theme.background\n',
    '        window.navigationBarColor = theme.background\n        window.statusBarColor = theme.background\n'
)
main_file.write_text(source)

# Increment the build version so this UI correction installs as a distinct update.
app_gradle = root / "app/build.gradle.kts"
gradle_text = app_gradle.read_text()
gradle_text = gradle_text.replace("versionCode = 5", "versionCode = 7")
gradle_text = gradle_text.replace('versionName = "1.5.0"', 'versionName = "1.6.2"')
app_gradle.write_text(gradle_text)

# Fail the preparation step if the old footer survived or the inset handler is missing.
check = main_file.read_text()
if 'val bottom = TextView(this).apply {' in check:
    raise SystemExit("Old text footer is still present")
if 'setOnApplyWindowInsetsListener' not in check or 'appDrawerButton' not in check:
    raise SystemExit("Status bar or app drawer footer patch did not apply")
print("System bar spacing and app drawer footer patch applied.")


# Gesture-first app drawer: remove the visible footer shortcut and use home gestures.
import re
main_file = root / "app/src/main/java/np/sagarmatha/launcher/MainActivity.kt"
source = main_file.read_text()

# Remove the footer grid button completely; the dock remains the final home-screen row.
source, footer_count = re.subn(
    r'        val footer = LinearLayout\(this\)\.apply \{.*?'
    r'        root\.addView\(footer, LinearLayout\.LayoutParams\(-1, dp\(48\)\)\)\n?',
    '',
    source,
    count=1,
    flags=re.S
)
if footer_count != 1:
    raise SystemExit("Expected app drawer footer button not found; refusing to continue")

# Track the start of a gesture at Activity level so child views cannot swallow it.
if "private var drawerGestureStartX" not in source:
    source = source.replace(
        "    private var touchY = 0f\n",
        "    private var touchY = 0f\n    private var drawerGestureStartX = 0f\n    private var drawerGestureStartY = 0f\n    private var drawerGestureStartedOnHome = false\n",
        1
    )

gesture_method = r'''
    override fun dispatchTouchEvent(event: MotionEvent): Boolean {
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                drawerGestureStartX = event.rawX
                drawerGestureStartY = event.rawY
                drawerGestureStartedOnHome = !showingDrawer
            }
            MotionEvent.ACTION_UP -> {
                if (drawerGestureStartedOnHome && !showingDrawer) {
                    val dx = event.rawX - drawerGestureStartX
                    val dy = event.rawY - drawerGestureStartY
                    val swipeRight = dx > dp(90) && dx > abs(dy) * 1.15f
                    // Keep the central widget column vertically scrollable.
                    // Swipe-up from the lower home/dock area opens the drawer.
                    val startsInDockZone = drawerGestureStartY >
                        resources.displayMetrics.heightPixels * 0.62f
                    val swipeUp = dy < -dp(100) && abs(dy) > abs(dx) * 1.15f &&
                        startsInDockZone
                    if (swipeRight || swipeUp) {
                        drawerGestureStartedOnHome = false
                        showDrawer("")
                        return true
                    }
                }
                drawerGestureStartedOnHome = false
            }
            MotionEvent.ACTION_CANCEL -> drawerGestureStartedOnHome = false
        }
        return super.dispatchTouchEvent(event)
    }

'''
if "override fun dispatchTouchEvent(event: MotionEvent)" not in source:
    anchor = "    private fun renderHome() {"
    if anchor not in source:
        raise SystemExit("Could not locate renderHome() to install drawer gesture handler")
    source = source.replace(anchor, gesture_method + anchor, 1)

# Remove the old footer text links if any survived, and verify the new gesture entry point.
if "val appDrawerButton" in source or "root.addView(footer" in source:
    raise SystemExit("Visible app drawer footer button still exists")
if "swipeRight" not in source or "startsInDockZone" not in source:
    raise SystemExit("Swipe gesture handler did not apply")
main_file.write_text(source)

# Bump the Android version for a clean update install.
app_gradle = root / "app/build.gradle.kts"
gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\s*=\s*\d+", "versionCode = 8", gradle_text, count=1)
gradle_text = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.6.3"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
print("Removed bottom app drawer shortcut; added swipe-right and dock-area swipe-up gestures; version 1.6.3.")
