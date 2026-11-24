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


# Premium App Drawer UI implementation based on the approved Sagarmatha concept.
import re

main_file = root / "app/src/main/java/np/sagarmatha/launcher/MainActivity.kt"
source = main_file.read_text()
drawer_start = source.find("    private fun showDrawer(initialQuery: String) {")
drawer_end = source.find("    private fun showWidgetManager() {", drawer_start)
if drawer_start < 0 or drawer_end < 0:
    raise SystemExit("Could not safely locate showDrawer() boundaries")

new_drawer = r'''    private fun showDrawer(initialQuery: String) {
        showingDrawer = true
        handler.removeCallbacks(clockTick)
        window.statusBarColor = Color.rgb(4, 20, 48)
        window.navigationBarColor = Color.rgb(4, 20, 48)

        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(16), 0, dp(16), dp(8))
            background = GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                intArrayOf(Color.rgb(3, 18, 48), Color.rgb(5, 39, 91), Color.rgb(9, 27, 66))
            )
            setOnApplyWindowInsetsListener { view, insets ->
                view.setPadding(dp(16), insets.systemWindowInsetTop, dp(16), dp(8) + insets.systemWindowInsetBottom)
                insets
            }
        }

        // Hero header: offline Himalayan artwork drawn in Canvas.
        val hero = FrameLayout(this)
        val mountainArt = object : View(this) {
            private val sky = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG)
            private val ridge = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG)
            private val snow = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG)
            override fun onDraw(canvas: android.graphics.Canvas) {
                super.onDraw(canvas)
                val w = width.toFloat()
                val h = height.toFloat()
                if (w <= 0f || h <= 0f) return
                sky.shader = android.graphics.LinearGradient(
                    0f, 0f, w, h,
                    intArrayOf(Color.rgb(7, 30, 76), Color.rgb(20, 61, 139), Color.rgb(5, 22, 55)),
                    null, android.graphics.Shader.TileMode.CLAMP
                )
                canvas.drawRect(0f, 0f, w, h, sky)
                sky.shader = android.graphics.RadialGradient(
                    w * .76f, h * .48f, w * .42f,
                    intArrayOf(Color.argb(150, 255, 180, 104), Color.argb(35, 87, 135, 255), Color.TRANSPARENT),
                    null, android.graphics.Shader.TileMode.CLAMP
                )
                canvas.drawCircle(w * .76f, h * .48f, w * .42f, sky)
                sky.shader = null
                fun peak(points: List<Pair<Float, Float>>, color: Int, paint: android.graphics.Paint) {
                    val path = android.graphics.Path()
                    path.moveTo(points.first().first * w, points.first().second * h)
                    points.drop(1).forEach { path.lineTo(it.first * w, it.second * h) }
                    path.lineTo(w, h); path.lineTo(0f, h); path.close()
                    paint.color = color
                    canvas.drawPath(path, paint)
                }
                peak(listOf(0f to .88f, .23f to .42f, .34f to .67f, .55f to .22f, .68f to .57f, .83f to .38f, 1f to .76f),
                    Color.rgb(35, 72, 126), ridge)
                peak(listOf(.23f to .42f, .30f to .52f, .34f to .67f, .55f to .22f, .62f to .45f, .55f to .37f, .50f to .46f, .46f to .36f),
                    Color.rgb(223, 235, 246), snow)
                peak(listOf(0f to .91f, .31f to .62f, .46f to .84f, .70f to .46f, .83f to .72f, 1f to .55f),
                    Color.rgb(9, 36, 79), ridge)
                peak(listOf(.31f to .62f, .38f to .70f, .46f to .84f, .70f to .46f, .75f to .61f, .70f to .57f, .66f to .64f),
                    Color.rgb(173, 203, 229), snow)
            }
        }
        hero.addView(mountainArt, FrameLayout.LayoutParams(-1, -1))
        val heroContent = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(2), dp(6), dp(2), dp(8))
        }
        val brandRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        brandRow.addView(TextView(this).apply {
            text = "🇳🇵"
            textSize = 23f
            gravity = Gravity.CENTER
        }, LinearLayout.LayoutParams(dp(42), dp(42)))
        brandRow.addView(TextView(this).apply {
            text = "SAGARMATHA"
            textSize = 15f
            letterSpacing = .18f
            setTextColor(Color.rgb(255, 190, 68))
            typeface = Typeface.create("sans-serif", Typeface.BOLD)
            gravity = Gravity.CENTER_VERTICAL
        }, LinearLayout.LayoutParams(0, dp(42), 1f))
        val close = TextView(this).apply {
            text = "×"
            textSize = 32f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
            background = rounded(Color.argb(55, 255, 255, 255), 28)
            setOnClickListener { renderHome() }
        }
        brandRow.addView(close, LinearLayout.LayoutParams(dp(42), dp(42)))
        heroContent.addView(brandRow)
        heroContent.addView(TextView(this).apply {
            text = if (nepaliMode) "तपाईंका एपहरू" else "Your apps"
            textSize = 25f
            setTextColor(Color.WHITE)
            typeface = Typeface.create("sans-serif", Typeface.BOLD)
            setPadding(dp(8), dp(5), 0, 0)
            setShadowLayer(dp(3).toFloat(), 0f, dp(2).toFloat(), Color.BLACK)
        })
        hero.addView(heroContent, FrameLayout.LayoutParams(-1, -1))
        root.addView(hero, LinearLayout.LayoutParams(-1, dp(126)))

        // Search field.
        val searchRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            background = GradientDrawable().apply {
                setColor(Color.argb(62, 160, 190, 255))
                cornerRadius = dp(30).toFloat()
                setStroke(dp(1), Color.argb(100, 190, 211, 255))
            }
            setPadding(dp(15), 0, dp(15), 0)
        }
        searchRow.addView(TextView(this).apply {
            text = "⌕"; textSize = 31f; setTextColor(Color.WHITE); gravity = Gravity.CENTER
        }, LinearLayout.LayoutParams(dp(42), dp(50)))
        val search = EditText(this).apply {
            hint = if (nepaliMode) "एप खोज्नुहोस्" else "Search apps"
            setHintTextColor(Color.argb(185, 238, 243, 255))
            setTextColor(Color.WHITE)
            textSize = 16f
            setSingleLine(true)
            background = null
            setPadding(dp(6), 0, dp(6), 0)
            setText(initialQuery)
            imeOptions = android.view.inputmethod.EditorInfo.IME_ACTION_SEARCH
        }
        searchRow.addView(search, LinearLayout.LayoutParams(0, dp(52), 1f))
        root.addView(searchRow, LinearLayout.LayoutParams(-1, dp(52)).apply { topMargin = dp(7) })

        val categoryScroll = HorizontalScrollView(this).apply {
            isHorizontalScrollBarEnabled = false
            overScrollMode = View.OVER_SCROLL_NEVER
        }
        val categoryRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, dp(12), 0, dp(10))
        }
        categoryScroll.addView(categoryRow)
        root.addView(categoryScroll, LinearLayout.LayoutParams(-1, dp(57)))

        val categoryItems = listOf(
            Triple("All", if (nepaliMode) "सबै" else "All", "▦"),
            Triple("Communication", if (nepaliMode) "सञ्चार" else "Communication", "◌"),
            Triple("Entertainment", if (nepaliMode) "मनोरञ्जन" else "Entertainment", "▷"),
            Triple("Tools", if (nepaliMode) "उपकरण" else "Tools", "▤"),
            Triple("Finance", if (nepaliMode) "वित्त" else "Finance", "▤")
        )
        var activeCategory = "All"
        var populateDrawerGrid: () -> Unit = {}
        val chipViews = linkedMapOf<String, TextView>()
        fun updateChipStyles() {
            chipViews.forEach { (key, chip) ->
                val selected = key == activeCategory
                chip.background = rounded(
                    if (selected) Color.rgb(255, 184, 48) else Color.argb(48, 170, 198, 255),
                    24
                )
                chip.setTextColor(if (selected) Color.rgb(25, 34, 57) else Color.WHITE)
                chip.alpha = if (selected) 1f else .92f
            }
        }
        categoryItems.forEach { (key, label, glyph) ->
            val chip = TextView(this).apply {
                text = if (key == "All") label else "$glyph  $label"
                textSize = 13f
                typeface = Typeface.create("sans-serif-medium", Typeface.NORMAL)
                gravity = Gravity.CENTER
                setPadding(dp(16), dp(9), dp(16), dp(9))
                setOnClickListener {
                    activeCategory = key
                    updateChipStyles()
                    populateDrawerGrid()
                }
            }
            chipViews[key] = chip
            categoryRow.addView(chip, LinearLayout.LayoutParams(-2, dp(40)).apply {
                rightMargin = dp(8)
            })
        }
        updateChipStyles()

        val contentRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.TOP
        }
        val gridScroll = ScrollView(this).apply {
            isFillViewport = false
            isVerticalScrollBarEnabled = false
            overScrollMode = View.OVER_SCROLL_NEVER
        }
        val grid = GridLayout(this).apply {
            columnCount = 4
            setPadding(0, dp(5), 0, dp(10))
            useDefaultMargins = false
        }
        gridScroll.addView(grid)
        // Fill available drawer height; zero height made every app tile invisible.
        contentRow.addView(gridScroll, LinearLayout.LayoutParams(0, -1, 1f))
        val alphabet = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(dp(3), dp(2), 0, dp(2))
        }
        val letters = ('A'..'Z').map { it.toString() } + "#"
        letters.forEach { letter ->
            val item = TextView(this).apply {
                text = letter
                textSize = 10f
                gravity = Gravity.CENTER
                setTextColor(Color.argb(220, 235, 241, 255))
                setOnClickListener {
                    val filtered = filteredDrawerApps(search.text.toString(), activeCategory)
                    val target = filtered.indexOfFirst {
                        if (letter == "#") it.label.firstOrNull()?.isLetter() == false
                        else it.label.trim().startsWith(letter, true)
                    }
                    if (target >= 0) {
                        gridScroll.post {
                            grid.getChildAt(target)?.let { tile -> gridScroll.smoothScrollTo(0, tile.top) }
                        }
                    }
                }
            }
            alphabet.addView(item, LinearLayout.LayoutParams(dp(20), dp(20)))
        }
        contentRow.addView(alphabet, LinearLayout.LayoutParams(dp(22), -1))
        root.addView(contentRow, LinearLayout.LayoutParams(-1, 0, 1f))

        val dots = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(0, dp(7), 0, dp(5))
        }
        repeat(3) { index ->
            val dot = View(this).apply {
                background = rounded(if (index == 0) Color.rgb(255, 184, 48) else Color.argb(105, 220, 230, 250), 20)
            }
            dots.addView(dot, LinearLayout.LayoutParams(dp(if (index == 0) 11 else 9), dp(9)).apply {
                leftMargin = dp(4); rightMargin = dp(4)
            })
        }
        root.addView(dots, LinearLayout.LayoutParams(-1, dp(23)))

        populateDrawerGrid = {
            grid.removeAllViews()
            val matches = filteredDrawerApps(search.text.toString(), activeCategory)
            if (matches.isEmpty()) {
                grid.addView(TextView(this).apply {
                    text = if (nepaliMode) "एप भेटिएन" else "No apps found"
                    textSize = 14f; setTextColor(Color.WHITE); gravity = Gravity.CENTER
                }, GridLayout.LayoutParams().apply { width = -1; height = dp(100); columnSpec = GridLayout.spec(0, 4) })
            } else {
            matches.forEach { app ->
                val tile = LinearLayout(this).apply {
                    orientation = LinearLayout.VERTICAL
                    gravity = Gravity.CENTER
                    setPadding(dp(2), dp(7), dp(2), dp(5))
                    setOnClickListener { launch(app) }
                    setOnLongClickListener {
                        if (!favorites.contains(app.packageName) && favorites.size < 5) {
                            favorites.add(app.packageName)
                            savePreferences()
                            Toast.makeText(this@MainActivity, if (nepaliMode) "डकमा थपियो" else "Added to dock", Toast.LENGTH_SHORT).show()
                        }
                        true
                    }
                }
                val icon = ImageView(this).apply {
                    setImageDrawable(app.icon)
                    scaleType = ImageView.ScaleType.FIT_CENTER
                    background = rounded(Color.argb(18, 255, 255, 255), 18)
                    setPadding(dp(2), dp(2), dp(2), dp(2))
                }
                tile.addView(icon, LinearLayout.LayoutParams(dp(56), dp(56)))
                tile.addView(TextView(this).apply {
                    text = app.label
                    textSize = 11.5f
                    setTextColor(Color.WHITE)
                    gravity = Gravity.CENTER
                    maxLines = 1
                    ellipsize = android.text.TextUtils.TruncateAt.END
                    setPadding(0, dp(5), 0, 0)
                }, LinearLayout.LayoutParams(-1, dp(23)))
                grid.addView(tile, GridLayout.LayoutParams().apply {
                    width = 0
                    height = dp(99)
                    columnSpec = GridLayout.spec(GridLayout.UNDEFINED, 1f)
                })
            }
            }
        }

        // Keep the grid population function accessible to the category/search controls.
        populateDrawerGrid()
        search.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) { populateDrawerGrid() }
            override fun afterTextChanged(s: Editable?) {}
        })
        setContentView(root)
    }

    private fun filteredDrawerApps(query: String, category: String): List<LaunchApp> {
        val q = query.trim()
        return appList.filter { app ->
            val queryMatch = q.isBlank() || app.label.contains(q, true) || app.packageName.contains(q, true)
            val categoryMatch = category == "All" || drawerCategory(app) == category
            queryMatch && categoryMatch
        }
    }

    private fun drawerCategory(app: LaunchApp): String {
        val key = (app.label + " " + app.packageName).lowercase(Locale.ROOT)
        return when {
            listOf("phone", "message", "whatsapp", "telegram", "messenger", "gmail", "mail", "teams", "chat", "facebook", "contacts", "truecaller").any { key.contains(it) } -> "Communication"
            listOf("youtube", "music", "spotify", "netflix", "game", "ball", "video", "tiktok", "photos", "gallery", "recorder").any { key.contains(it) } -> "Entertainment"
            listOf("bank", "esewa", "khalti", "wallet", "pay", "finance", "binance", "karobar", "money").any { key.contains(it) } -> "Finance"
            else -> "Tools"
        }
    }

'''
source = source[:drawer_start] + new_drawer + source[drawer_end:]

# Add a small helper for the approved category/app drawer filtering behavior.
if "private fun filteredDrawerApps(" not in source or "private fun drawerCategory(" not in source:
    raise SystemExit("Premium drawer filter helpers missing")
if "val appDrawerButton" in source:
    footer_start = source.find("        val footer = LinearLayout(this).apply {")
    footer_end_marker = "        root.addView(footer, LinearLayout.LayoutParams(-1, dp(48)))"
    footer_end = source.find(footer_end_marker, footer_start)
    if footer_start >= 0 and footer_end >= 0:
        footer_end += len(footer_end_marker)
        source = source[:footer_start] + source[footer_end:]

# Ensure this visual rebuild gets its own Android update version.
app_gradle = root / "app/build.gradle.kts"
gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\s*=\s*\d+", "versionCode = 9", gradle_text, count=1)
gradle_text = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.7.0"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
main_file.write_text(source)
print("Premium Sagarmatha App Drawer implemented; version 1.7.0.")



# Phase 1 architecture foundation: separate installed-app discovery from Activity UI.
repository_file = root / "app/src/main/java/np/sagarmatha/launcher/LauncherAppRepository.kt"
repository_file.write_text("""package np.sagarmatha.launcher

import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build

/**
 * Single source of truth for installed, launchable applications.
 * Keeps package discovery out of MainActivity and explicitly retains Sagarmatha itself.
 */
class LauncherAppRepository(private val context: Context) {
    fun loadApps(): List<LaunchApp> {
        val pm = context.packageManager
        val launcherIntent = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
        val resolved = if (Build.VERSION.SDK_INT >= 33) {
            pm.queryIntentActivities(
                launcherIntent,
                PackageManager.ResolveInfoFlags.of(PackageManager.MATCH_ALL.toLong())
            )
        } else {
            @Suppress("DEPRECATION")
            pm.queryIntentActivities(launcherIntent, PackageManager.MATCH_ALL)
        }

        val apps = resolved.mapNotNull { resolveInfo ->
            val activity = resolveInfo.activityInfo ?: return@mapNotNull null
            runCatching {
                LaunchApp(
                    resolveInfo.loadLabel(pm).toString(),
                    activity.packageName,
                    resolveInfo.loadIcon(pm)
                )
            }.getOrNull()
        }.distinctBy { it.packageName }.toMutableList()

        // Some OEM package managers omit the active HOME package from launcher queries.
        if (apps.none { it.packageName == context.packageName }) {
            runCatching {
                val ownInfo = pm.getApplicationInfo(context.packageName, 0)
                apps.add(
                    LaunchApp(
                        pm.getApplicationLabel(ownInfo).toString(),
                        context.packageName,
                        pm.getApplicationIcon(ownInfo)
                    )
                )
            }
        }
        return apps.sortedWith(compareBy(String.CASE_INSENSITIVE_ORDER) { it.label.trim() })
    }
}
""")

source = main_file.read_text()
source, loader_count = re.subn(
    r"    private fun loadApps\(\): List<LaunchApp> \{.*?\n    \}\n",
    "    private fun loadApps(): List<LaunchApp> = LauncherAppRepository(this).loadApps()\n",
    source,
    count=1,
    flags=re.S
)
if loader_count != 1:
    raise SystemExit("Could not modularize loadApps(); expected exactly one existing function")
drawer_marker = "    private fun showDrawer(initialQuery: String) {"
if drawer_marker not in source:
    raise SystemExit("Could not find showDrawer() for app catalog refresh")
source = source.replace(
    drawer_marker,
    drawer_marker + "\n        // Refresh the catalog whenever the drawer opens so newly installed apps appear.",
    1
)
source = source.replace(
    "        // Refresh the catalog whenever the drawer opens so newly installed apps appear.\n",
    "        // Refresh the catalog whenever the drawer opens so newly installed apps appear.\n        appList = loadApps()\n",
    1
)
main_file.write_text(source)

app_gradle = root / "app/build.gradle.kts"
gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\\s*=\\s*\\d+", "versionCode = 10", gradle_text, count=1)
gradle_text = re.sub(r'versionName\\s*=\\s*"[^"]+"', 'versionName = "1.8.0"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
print("Sagarmatha Launcher Phase 1 architecture foundation applied; version 1.8.0.")


# Phase 1.1 reliability fix: enumerate launchable installed apps using Android package visibility.
manifest_file = root / "app/src/main/AndroidManifest.xml"
manifest_text = manifest_file.read_text()
query_permission = '    <uses-permission android:name="android.permission.QUERY_ALL_PACKAGES" />'
if "android.permission.QUERY_ALL_PACKAGES" not in manifest_text:
    manifest_text = manifest_text.replace(
        '    <uses-permission android:name="android.permission.INTERNET" />',
        '    <uses-permission android:name="android.permission.INTERNET" />\n' + query_permission,
        1
    )
manifest_file.write_text(manifest_text)

repository_file = root / "app/src/main/java/np/sagarmatha/launcher/LauncherAppRepository.kt"
repository_file.write_text("""package np.sagarmatha.launcher

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build

/**
 * Lists apps that Android can actually launch.
 * QUERY_ALL_PACKAGES is declared because discovering installed launchers is the core
 * function of this home-screen replacement.
 */
class LauncherAppRepository(private val context: Context) {
    fun loadApps(): List<LaunchApp> {
        val pm = context.packageManager
        val installed = if (Build.VERSION.SDK_INT >= 33) {
            pm.getInstalledApplications(PackageManager.ApplicationInfoFlags.of(0))
        } else {
            @Suppress("DEPRECATION")
            pm.getInstalledApplications(0)
        }

        val apps = installed.mapNotNull { info ->
            val launchIntent = runCatching { pm.getLaunchIntentForPackage(info.packageName) }.getOrNull()
                ?: return@mapNotNull null
            runCatching {
                LaunchApp(
                    pm.getApplicationLabel(info).toString(),
                    info.packageName,
                    pm.getApplicationIcon(info)
                )
            }.getOrNull()
        }.distinctBy { it.packageName }.toMutableList()

        // Ensure the launcher itself is available in its own app drawer.
        if (apps.none { it.packageName == context.packageName }) {
            runCatching {
                val ownInfo = pm.getApplicationInfo(context.packageName, 0)
                apps.add(
                    LaunchApp(
                        pm.getApplicationLabel(ownInfo).toString(),
                        context.packageName,
                        pm.getApplicationIcon(ownInfo)
                    )
                )
            }
        }
        return apps.sortedWith(compareBy(String.CASE_INSENSITIVE_ORDER) { it.label.trim() })
    }
}
""")

# Ensure version increments are applied to the generated Android project.
app_gradle = root / "app/build.gradle.kts"
gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\s*=\s*\d+", "versionCode = 11", gradle_text, count=1)
gradle_text = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.8.1"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
print("Phase 1.1: robust installed-app discovery, package visibility permission, version 1.8.1.")


# Phase 2: visible Home Screen refresh (premium hero panel + contextual shortcuts).
home_source = main_file.read_text()
hero_anchor = "        clockView = TextView(this).apply {"
hero_block = """        val heroPanel = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            background = GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                intArrayOf(Color.rgb(34, 72, 119), Color.rgb(22, 48, 83), Color.rgb(17, 39, 65))
            ).apply {
                cornerRadius = dp(26).toFloat()
                setStroke(dp(1), Color.argb(70, 255, 255, 255))
            }
            setPadding(dp(16), dp(12), dp(16), dp(12))
            elevation = dp(3).toFloat()
        }
"""
if hero_anchor not in home_source:
    raise SystemExit("Phase 2: clock anchor not found; no home UI changes applied")
if "val heroPanel = LinearLayout(this)" not in home_source:
    home_source = home_source.replace(hero_anchor, hero_block + hero_anchor, 1)
home_source = home_source.replace("        root.addView(clockView)\n", "        heroPanel.addView(clockView)\n", 1)
home_source = home_source.replace("        root.addView(dateView)\n", "        heroPanel.addView(dateView)\n", 1)
home_source = home_source.replace("        root.addView(tagline)\n", """        heroPanel.addView(tagline)
        root.addView(heroPanel, LinearLayout.LayoutParams(-1, -2).apply { bottomMargin = dp(12) })
""", 1)

search_anchor = "        root.addView(search, LinearLayout.LayoutParams(-1, dp(46)))"
quick_actions = """
        val quickActions = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(0, dp(10), 0, dp(4))
        }
        fun quickAction(label: String, symbol: String, action: () -> Unit) {
            val chip = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
                background = rounded(Color.argb(48, 255, 255, 255), 16)
                setPadding(dp(9), dp(8), dp(9), dp(8))
                isClickable = true
                isFocusable = true
                setOnClickListener { action() }
            }
            chip.addView(TextView(this).apply {
                text = symbol
                textSize = 18f
                gravity = Gravity.CENTER
                setTextColor(theme.accent)
            })
            chip.addView(TextView(this).apply {
                text = label
                textSize = 10f
                gravity = Gravity.CENTER
                setTextColor(theme.text)
                maxLines = 1
            })
            quickActions.addView(chip, LinearLayout.LayoutParams(0, dp(58), 1f).apply {
                leftMargin = dp(3); rightMargin = dp(3)
            })
        }
        quickAction(if (nepaliMode) "पात्रो" else "Calendar", "▦") { showDataSettings() }
        quickAction(if (nepaliMode) "विजेट" else "Widgets", "▤") { showWidgetManager() }
        quickAction(if (nepaliMode) "एपहरू" else "Apps", "⌕") { showDrawer("") }
        quickAction(if (nepaliMode) "सेटिङ" else "Settings", "⚙") { showSettingsScreen() }
        root.addView(quickActions, LinearLayout.LayoutParams(-1, dp(70)))
"""
if search_anchor not in home_source:
    raise SystemExit("Phase 2: search view anchor not found; no home UI changes applied")
if "val quickActions = LinearLayout(this)" not in home_source:
    home_source = home_source.replace(search_anchor, search_anchor + "\n" + quick_actions, 1)

home_source = home_source.replace(
    'text = if (nepaliMode) "नेपालका लागि स्मार्ट विजेटहरू" else "SMART NEPALI WIDGETS"',
    'text = if (nepaliMode) "तपाईंको दिन — एकै नजरमा" else "YOUR DAY AT A GLANCE"',
    1
)
main_file.write_text(home_source)

# Distinct visible release version for Phase 2.
gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\s*=\s*\d+", "versionCode = 12", gradle_text, count=1)
gradle_text = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.9.0"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
print("Phase 2: premium home hero panel, quick actions and refreshed home section heading; version 1.9.0.")


# Phase 2.1: practical, scroll-first Nepali home and functional settings control center.
home_method = r'''
    private fun renderHome() {
        showingDrawer = false
        handler.removeCallbacks(clockTick)
        window.statusBarColor = theme.background
        window.navigationBarColor = theme.background
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(8), dp(18), dp(8))
            background = homeBackground()
            setOnApplyWindowInsetsListener { view, insets ->
                view.setPadding(dp(18), dp(8) + insets.systemWindowInsetTop, dp(18), dp(8) + insets.systemWindowInsetBottom)
                insets
            }
        }

        val header = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        val brand = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; gravity = Gravity.CENTER_VERTICAL }
        brand.addView(TextView(this).apply {
            text = "🇳🇵  SAGARMATHA"; textSize = 14f; letterSpacing = .14f
            setTextColor(theme.accent); typeface = Typeface.DEFAULT_BOLD
        })
        brand.addView(TextView(this).apply {
            text = if (nepaliMode) "तपाईंको फोन, तपाईंको शैली" else "Your phone, your style"
            textSize = 10f; setTextColor(theme.muted)
        })
        header.addView(brand, LinearLayout.LayoutParams(0, dp(48), 1f))

        fun headerAction(glyph: String, description: String, action: () -> Unit): TextView =
            TextView(this).apply {
                text = glyph; contentDescription = description; textSize = 20f
                gravity = Gravity.CENTER; setTextColor(theme.accent)
                background = rounded(Color.argb(24, 255, 255, 255), 15)
                layoutParams = LinearLayout.LayoutParams(dp(42), dp(42)).apply { leftMargin = dp(7) }
                setOnClickListener { action() }
            }
        header.addView(headerAction(if (nepaliMode) "ने" else "EN", "Switch language") {
            nepaliMode = !nepaliMode; savePreferences(); renderHome()
        })
        header.addView(headerAction("▦", "Manage widgets") { showWidgetManager() })
        header.addView(headerAction("⚙", "Settings") { showSettingsScreen() })
        root.addView(header)

        val dateBlock = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL; gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(2), dp(12), dp(2), dp(12))
        }
        clockView = TextView(this).apply {
            text = SimpleDateFormat("h:mm", Locale.getDefault()).format(Date())
            textSize = 42f; setTextColor(theme.text)
            typeface = Typeface.create("sans-serif-light", Typeface.NORMAL)
        }
        dateBlock.addView(clockView)
        dateView = TextView(this).apply { textSize = 12f; setTextColor(theme.muted); setPadding(0, dp(2), 0, 0) }
        dateBlock.addView(dateView)
        updateDateText()
        root.addView(dateBlock)

        val search = EditText(this).apply {
            hint = if (nepaliMode) "एप वा केही खोज्नुहोस्" else "Search apps"
            setHintTextColor(Color.argb(170, theme.muted)); setTextColor(theme.text); textSize = 14f
            setSingleLine(true); setPadding(dp(16), 0, dp(14), 0)
            background = GradientDrawable().apply {
                setColor(Color.argb(34, 255, 255, 255)); cornerRadius = dp(18).toFloat()
                setStroke(dp(1), Color.argb(70, 225, 177, 91))
            }
            setCompoundDrawablesWithIntrinsicBounds(android.R.drawable.ic_menu_search, 0, 0, 0)
            compoundDrawablePadding = dp(10)
            setOnFocusChangeListener { _, focused -> if (focused) showDrawer("") }
            setOnEditorActionListener { _, _, _ -> showDrawer(text.toString()); true }
            setOnClickListener { showDrawer("") }
        }
        root.addView(search, LinearLayout.LayoutParams(-1, dp(50)).apply { bottomMargin = dp(12) })

        val contentScroll = ScrollView(this).apply { overScrollMode = View.OVER_SCROLL_NEVER }
        val content = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        val sectionHeader = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        sectionHeader.addView(TextView(this).apply {
            text = if (nepaliMode) "आजको झलक" else "TODAY AT A GLANCE"
            textSize = 11f; letterSpacing = .10f; setTextColor(theme.accent); typeface = Typeface.DEFAULT_BOLD
        }, LinearLayout.LayoutParams(0, dp(34), 1f))
        sectionHeader.addView(TextView(this).apply {
            text = if (nepaliMode) "सम्पादन" else "EDIT"
            textSize = 10f; setTextColor(theme.accent); setPadding(dp(10), dp(6), dp(10), dp(6))
            background = rounded(Color.argb(24, 255, 255, 255), 12)
            setOnClickListener { showSettingsScreen() }
        })
        content.addView(sectionHeader)

        val nepaliDate = runCatching { NepaliCalendarService.todayNepali(nepaliMode) }
            .getOrElse { if (nepaliMode) "नेपाली मिति उपलब्ध भएन" else "Nepali date unavailable" }
        val englishDate = runCatching { NepaliCalendarService.todayEnglish() }
            .getOrElse { SimpleDateFormat("EEEE, d MMMM yyyy", Locale.ENGLISH).format(Date()) }
        content.addView(widgetCard(if (nepaliMode) "आजको पात्रो" else "TODAY'S CALENDAR", nepaliDate, englishDate, "calendar"))
        content.addView(buildWeatherCard())
        content.addView(buildNewsCard())

        if (appFolders.isNotEmpty()) {
            content.addView(TextView(this).apply {
                text = if (nepaliMode) "मेरा फोल्डरहरू" else "MY FOLDERS"
                textSize = 11f; setTextColor(theme.accent); setPadding(dp(2), dp(8), 0, dp(7))
            })
            val folderRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
            appFolders.forEach { folder ->
                folderRow.addView(TextView(this).apply {
                    text = "▣  " + folder.name; textSize = 12f; setTextColor(theme.text)
                    background = panel(); setPadding(dp(12), dp(10), dp(12), dp(10))
                    setOnClickListener { openFolder(folder) }
                    setOnLongClickListener { confirmDeleteFolder(folder); true }
                }, LinearLayout.LayoutParams(-2, -2).apply { rightMargin = dp(8) })
            }
            content.addView(folderRow)
        }

        hostedWidgetIds.forEach { id ->
            val hosted = widgetViews[id] ?: createWidgetHostView(id)
            if (hosted != null) {
                (hosted.parent as? ViewGroup)?.removeView(hosted)
                val holder = LinearLayout(this).apply {
                    orientation = LinearLayout.VERTICAL; background = panel()
                    setPadding(dp(5), dp(5), dp(5), dp(5))
                }
                holder.addView(hosted, LinearLayout.LayoutParams(-1, dp(widgetHeightDp)))
                content.addView(holder, LinearLayout.LayoutParams(-1, -2).apply { topMargin = dp(8); bottomMargin = dp(4) })
            }
        }
        contentScroll.addView(content)
        root.addView(contentScroll, LinearLayout.LayoutParams(-1, 0, 1f))

        val dock = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER
            background = GradientDrawable().apply {
                setColor(Color.argb(38, 255, 255, 255)); cornerRadius = dp(22).toFloat()
                setStroke(dp(1), Color.argb(48, 255, 255, 255))
            }
            setPadding(dp(5), dp(5), dp(5), dp(5))
            setOnDragListener { _, event ->
                if (event.action == android.view.DragEvent.ACTION_DROP) {
                    val dragged = event.clipData?.getItemAt(0)?.text?.toString()
                    val targetIndex = ((event.x / width.coerceAtLeast(1)) * favorites.size)
                        .toInt().coerceIn(0, (favorites.size - 1).coerceAtLeast(0))
                    if (!dragged.isNullOrBlank() && favorites.contains(dragged)) {
                        favorites.remove(dragged); favorites.add(targetIndex.coerceAtMost(favorites.size), dragged)
                        savePreferences(); renderHome()
                    }
                    true
                } else event.action == android.view.DragEvent.ACTION_DRAG_STARTED
            }
        }
        favorites.mapNotNull { pkg -> appList.find { it.packageName == pkg } }.take(5).forEach { app ->
            val tile = appTile(app, true)
            tile.setOnLongClickListener {
                val clip = ClipData.newPlainText("favorite-package", app.packageName)
                tile.startDragAndDrop(clip, View.DragShadowBuilder(tile), null, 0)
                true
            }
            dock.addView(tile, LinearLayout.LayoutParams(0, dp(62), 1f))
        }
        root.addView(dock, LinearLayout.LayoutParams(-1, dp(70)).apply { topMargin = dp(10) })
        setContentView(root)
        handler.post(clockTick)
    }

'''
start_token = "    private fun renderHome() {"
end_token = "    private fun updateDateText() {"
start = source.find(start_token)
end = source.find(end_token, start)
if start < 0 or end < 0:
    raise SystemExit("Could not safely locate renderHome() boundaries")
source = source[:start] + home_method + source[end:]

bg_method = r'''
    private fun homeBackground(): android.graphics.drawable.Drawable {
        if (customWallpaperUri.isNotBlank()) runCatching {
            val stream = contentResolver.openInputStream(Uri.parse(customWallpaperUri))
            val bitmap = stream?.use { BitmapFactory.decodeStream(it) }
            if (bitmap != null) return BitmapDrawable(resources, bitmap)
        }
        val lower = when (wallpaperIndex) {
            1 -> Color.rgb(31, 56, 83)
            2 -> Color.rgb(24, 67, 59)
            3 -> Color.rgb(66, 56, 44)
            else -> theme.secondary
        }
        return GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, intArrayOf(theme.background, lower))
    }

'''
bg_start = source.find("    private fun homeBackground():")
bg_end = source.find("    private fun showAppearance()", bg_start)
if bg_start < 0 or bg_end < 0:
    raise SystemExit("Could not safely locate homeBackground() boundaries")
source = source[:bg_start] + bg_method + source[bg_end:]

settings_method = r'''
    private fun showSettingsScreen() {
        showingDrawer = true
        handler.removeCallbacks(clockTick)
        window.statusBarColor = theme.background
        window.navigationBarColor = theme.background
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(8), dp(18), dp(8))
            background = GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, intArrayOf(theme.background, theme.secondary))
            setOnApplyWindowInsetsListener { view, insets ->
                view.setPadding(dp(18), dp(8) + insets.systemWindowInsetTop, dp(18), dp(8) + insets.systemWindowInsetBottom)
                insets
            }
        }
        val header = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        header.addView(LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            addView(TextView(this@MainActivity).apply {
                text = if (nepaliMode) "सेटिङहरू" else "Settings"
                textSize = 25f; setTextColor(theme.text); typeface = Typeface.DEFAULT_BOLD
            })
            addView(TextView(this@MainActivity).apply {
                text = if (nepaliMode) "आफ्नो Launcher आफूअनुसार मिलाउनुहोस्" else "Make your launcher work your way"
                textSize = 11f; setTextColor(theme.muted)
            })
        }, LinearLayout.LayoutParams(0, dp(58), 1f))
        header.addView(TextView(this).apply {
            text = "✕"; textSize = 21f; setTextColor(theme.text); gravity = Gravity.CENTER
            background = rounded(Color.argb(28, 255, 255, 255), 14)
            setOnClickListener { renderHome() }
        }, LinearLayout.LayoutParams(dp(42), dp(42)))
        root.addView(header)

        val scroll = ScrollView(this).apply { overScrollMode = View.OVER_SCROLL_NEVER }
        val list = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        fun section(title: String) {
            list.addView(TextView(this).apply {
                text = title; textSize = 10f; letterSpacing = .12f; setTextColor(theme.accent)
                typeface = Typeface.DEFAULT_BOLD; setPadding(dp(3), dp(18), 0, dp(8))
            })
        }
        fun setting(title: String, subtitle: String, glyph: String, action: () -> Unit) {
            val row = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL
                background = GradientDrawable().apply {
                    setColor(Color.argb(28, 255, 255, 255)); cornerRadius = dp(17).toFloat()
                    setStroke(dp(1), Color.argb(35, 255, 255, 255))
                }
                setPadding(dp(12), dp(9), dp(12), dp(9))
                isClickable = true; isFocusable = true
                setOnClickListener { action() }
            }
            row.addView(TextView(this).apply {
                text = glyph; textSize = 21f; gravity = Gravity.CENTER; setTextColor(theme.accent)
                background = rounded(Color.argb(28, 225, 177, 91), 13)
            }, LinearLayout.LayoutParams(dp(42), dp(42)))
            val labels = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(12), 0, dp(4), 0) }
            labels.addView(TextView(this).apply {
                text = title; textSize = 13f; setTextColor(theme.text); typeface = Typeface.DEFAULT_BOLD
            })
            labels.addView(TextView(this).apply {
                text = subtitle; textSize = 10f; setTextColor(theme.muted); maxLines = 2
            })
            row.addView(labels, LinearLayout.LayoutParams(0, -2, 1f))
            row.addView(TextView(this).apply {
                text = "›"; textSize = 22f; setTextColor(theme.accent); gravity = Gravity.CENTER
            }, LinearLayout.LayoutParams(dp(22), dp(42)))
            list.addView(row, LinearLayout.LayoutParams(-1, -2).apply { bottomMargin = dp(8) })
        }

        section(if (nepaliMode) "देखावट" else "PERSONALIZATION")
        setting(if (nepaliMode) "थिम र वालपेपर" else "Theme & wallpaper",
            if (nepaliMode) "रङ, वालपेपर र आइकन शैली" else "Colors, wallpaper and icon style", "◐") { showAppearance() }

        section(if (nepaliMode) "होम स्क्रिन" else "HOME SCREEN")
        setting(if (nepaliMode) "डक व्यवस्थापन" else "Dock management",
            if (nepaliMode) "एप थप्नुहोस्, हटाउनुहोस् र क्रम मिलाउनुहोस्" else "Add, remove and reorder favorite apps", "▤") { showDockManager() }
        setting(if (nepaliMode) "विजेट व्यवस्थापन" else "Widget management",
            if (nepaliMode) "Android विजेट थप्नुहोस् र हटाउनुहोस्" else "Add and remove Android widgets", "▦") { showWidgetManager() }
        setting(if (nepaliMode) "फोल्डर व्यवस्थापन" else "Folder management",
            if (nepaliMode) "एप फोल्डर बनाउनुहोस् र मिलाउनुहोस्" else "Create and organize app folders", "▣") { showFolderManager() }

        section(if (nepaliMode) "एप र भाषा" else "APPS & LANGUAGE")
        setting(if (nepaliMode) "एप ड्रअर" else "App drawer",
            if (nepaliMode) "सबै एप, खोज र श्रेणी" else "All apps, search and categories", "⊞") { showDrawer("") }
        setting(if (nepaliMode) "भाषा" else "Language",
            if (nepaliMode) "हालको भाषा: नेपाली" else "Current language: English", "अ") {
            nepaliMode = !nepaliMode; savePreferences(); showSettingsScreen()
        }

        section(if (nepaliMode) "सेवाहरू" else "SERVICES")
        setting(if (nepaliMode) "मौसम र समाचार" else "Weather & news",
            if (nepaliMode) "मौसम स्थान र RSS समाचार फिड" else "Weather location and RSS news feed", "☼") { showDataSettings() }

        scroll.addView(list)
        root.addView(scroll, LinearLayout.LayoutParams(-1, 0, 1f))
        setContentView(root)
    }

'''
settings_start = source.find("    private fun showSettingsScreen() {")
settings_end = source.find("    private fun showDockManager()", settings_start)
if settings_start < 0 or settings_end < 0:
    raise SystemExit("Could not safely locate showSettingsScreen() boundaries")
source = source[:settings_start] + settings_method + source[settings_end:]

main_file.write_text(source)
gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\s*=\s*\d+", "versionCode = 13", gradle_text, count=1)
gradle_text = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "2.0.0"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
print("Sagarmatha Launcher v2.0.0: practical navy/gold home and settings UI applied.")


# Phase 2.1 compile correction: apply alpha to the existing theme color safely.
home_source = main_file.read_text()
home_source = home_source.replace(
    "setHintTextColor(Color.argb(170, theme.muted)); setTextColor(theme.text); textSize = 14f",
    "setHintTextColor(Color.argb(170, Color.red(theme.muted), Color.green(theme.muted), Color.blue(theme.muted))); setTextColor(theme.text); textSize = 14f"
)
main_file.write_text(home_source)
print("Fixed Color.argb overload in Home Screen search field.")


# Phase 2.2: user-controlled dock, built-in home cards, and centered Devanagari clock/date.
source = main_file.read_text()

# Persist visibility of the three built-in home cards.
source = source.replace(
    '    private var widgetHeightDp = 220\n',
    '''    private var widgetHeightDp = 220
    private var showCalendarCard = true
    private var showWeatherCard = true
    private var showNewsCard = true
''',
    1
)
source = source.replace(
    '        widgetHeightDp = prefs.getInt("widget_height", 220).coerceIn(120, 420)\n',
    '''        widgetHeightDp = prefs.getInt("widget_height", 220).coerceIn(120, 420)
        showCalendarCard = prefs.getBoolean("show_calendar_card", true)
        showWeatherCard = prefs.getBoolean("show_weather_card", true)
        showNewsCard = prefs.getBoolean("show_news_card", true)
''',
    1
)
source = source.replace(
    '            .putInt("widget_height", widgetHeightDp)\n',
    '''            .putInt("widget_height", widgetHeightDp)
            .putBoolean("show_calendar_card", showCalendarCard)
            .putBoolean("show_weather_card", showWeatherCard)
            .putBoolean("show_news_card", showNewsCard)
''',
    1
)

# Use Devanagari numerals for the live clock in Nepali mode.
source = source.replace(
    '            clockView?.text = SimpleDateFormat("h:mm", Locale.getDefault()).format(Date())',
    '            clockView?.text = formatHomeClock()',
    1
)
source = source.replace(
    '            text = SimpleDateFormat("h:mm", Locale.getDefault()).format(Date())',
    '            text = formatHomeClock()',
    1
)
source = source.replace(
    '            orientation = LinearLayout.VERTICAL; gravity = Gravity.CENTER_VERTICAL\n            setPadding(dp(2), dp(12), dp(2), dp(12))',
    '''            orientation = LinearLayout.VERTICAL
            gravity = if (nepaliMode) Gravity.CENTER else Gravity.CENTER_VERTICAL
            setPadding(dp(2), dp(12), dp(2), dp(12))''',
    1
)
source = source.replace(
    '            textSize = 42f; setTextColor(theme.text)\n            typeface = Typeface.create("sans-serif-light", Typeface.NORMAL)',
    '''            textSize = 42f; setTextColor(theme.text)
            gravity = if (nepaliMode) Gravity.CENTER else Gravity.START
            typeface = Typeface.create("sans-serif-light", Typeface.NORMAL)''',
    1
)
source = source.replace(
    '        dateView = TextView(this).apply { textSize = 12f; setTextColor(theme.muted); setPadding(0, dp(2), 0, 0) }\n        dateBlock.addView(dateView)',
    '''        dateView = TextView(this).apply {
            textSize = 12f; setTextColor(theme.muted); setPadding(0, dp(2), 0, 0)
            gravity = if (nepaliMode) Gravity.CENTER else Gravity.START
        }
        dateBlock.addView(dateView, LinearLayout.LayoutParams(-1, -2))''',
    1
)

# The Nepali home shows the Bikram Sambat date only, centered with Devanagari digits.
old_date = '''        dateView?.text = runCatching {
            val bs = NepaliCalendarService.todayNepali(nepaliMode)
            val ad = NepaliCalendarService.todayEnglish()
            if (nepaliMode) "$bs  •  $ad" else "$ad  •  $bs"
        }.getOrElse {
            SimpleDateFormat("EEEE, d MMMM yyyy", Locale.getDefault()).format(Date())
        }'''
new_date = '''        dateView?.text = runCatching {
            if (nepaliMode) {
                toDevanagariDigits(NepaliCalendarService.todayNepali(true))
            } else {
                NepaliCalendarService.todayEnglish()
            }
        }.getOrElse {
            val fallback = SimpleDateFormat("EEEE, d MMMM yyyy", Locale.ENGLISH).format(Date())
            if (nepaliMode) toDevanagariDigits(fallback) else fallback
        }'''
if old_date not in source:
    raise SystemExit("Date display block did not match; refusing partial date patch")
source = source.replace(old_date, new_date, 1)

helper_anchor = '    private fun updateDateText() {\n'
helpers = '''    private fun formatHomeClock(): String {
        val value = SimpleDateFormat("h:mm", Locale.ENGLISH).format(Date())
        return if (nepaliMode) toDevanagariDigits(value) else value
    }

'''
if helper_anchor not in source:
    raise SystemExit("Clock/date helper insertion point not found")
source = source.replace(helper_anchor, helpers + helper_anchor, 1)

# Show only enabled built-in home cards.
source = source.replace(
    """        content.addView(widgetCard(if (nepaliMode) "आजको पात्रो" else "TODAY'S CALENDAR", nepaliDate, englishDate, "calendar"))\n        content.addView(buildWeatherCard())\n        content.addView(buildNewsCard())""",
    '''        if (showCalendarCard) {
            content.addView(widgetCard(if (nepaliMode) "आजको पात्रो" else "TODAY'S CALENDAR", nepaliDate, englishDate, "calendar"))
        }
        if (showWeatherCard) content.addView(buildWeatherCard())
        if (showNewsCard) content.addView(buildNewsCard())''',
    1
)

# Let users configure built-in cards at the top of the widget manager.
widget_description_anchor = '        root.addView(description)\n\n        val add = TextView(this).apply {'
toggle_block = '''        root.addView(description)

        val builtInHeading = TextView(this).apply {
            text = if (nepaliMode) "होम स्क्रिनका कार्डहरू" else "HOME SCREEN CARDS"
            textSize = 10f; letterSpacing = .12f; setTextColor(theme.accent)
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, dp(10), 0, dp(7))
        }
        root.addView(builtInHeading)

        fun builtInToggle(title: String, checked: Boolean, onChange: (Boolean) -> Unit) {
            val row = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL
                background = panel(); setPadding(dp(12), dp(4), dp(12), dp(4))
            }
            row.addView(TextView(this).apply {
                text = title; textSize = 13f; setTextColor(theme.text)
            }, LinearLayout.LayoutParams(0, dp(46), 1f))
            row.addView(Switch(this).apply {
                isChecked = checked
                setOnCheckedChangeListener { _, value -> onChange(value) }
            })
            root.addView(row, LinearLayout.LayoutParams(-1, dp(54)).apply { bottomMargin = dp(6) })
        }
        builtInToggle(if (nepaliMode) "नेपाली पात्रो" else "Calendar", showCalendarCard) {
            showCalendarCard = it; savePreferences()
        }
        builtInToggle(if (nepaliMode) "मौसम" else "Weather", showWeatherCard) {
            showWeatherCard = it; savePreferences()
        }
        builtInToggle(if (nepaliMode) "नेपाली समाचार" else "Nepali news", showNewsCard) {
            showNewsCard = it; savePreferences()
        }

        val add = TextView(this).apply {'''
if widget_description_anchor not in source:
    raise SystemExit("Widget manager insertion point not found")
source = source.replace(widget_description_anchor, toggle_block, 1)

# Long-press a dock item to remove or replace it; long-press dock background to add.
source = source.replace(
    '''            val tile = appTile(app, true)
            tile.setOnLongClickListener {
                val clip = ClipData.newPlainText("favorite-package", app.packageName)
                tile.startDragAndDrop(clip, View.DragShadowBuilder(tile), null, 0)
                true
            }''',
    '''            val tile = appTile(app, true)
            tile.setOnLongClickListener {
                showDockSlotActions(app, favorites.indexOf(app.packageName))
                true
            }''',
    1
)
source = source.replace(
    '''            setPadding(dp(5), dp(5), dp(5), dp(5))
            setOnDragListener { _, event ->''',
    '''            setPadding(dp(5), dp(5), dp(5), dp(5))
            isLongClickable = true
            setOnLongClickListener {
                showDockAppPicker()
                true
            }
            setOnDragListener { _, event ->''',
    1
)

dock_methods_anchor = '    private fun showDockAppPicker() {\n'
dock_methods = '''    private fun showDockSlotActions(app: LaunchApp, index: Int) {
        val actions = if (nepaliMode) arrayOf("एप हटाउनुहोस्", "अर्को एपले बदल्नुहोस्", "रद्द गर्नुहोस्")
            else arrayOf("Remove app", "Replace with another app", "Cancel")
        AlertDialog.Builder(this)
            .setTitle(app.label)
            .setItems(actions) { _, which ->
                when (which) {
                    0 -> {
                        if (index in favorites.indices) favorites.removeAt(index)
                        savePreferences(); renderHome()
                    }
                    1 -> showDockReplacementPicker(index)
                }
            }
            .show()
    }

    private fun showDockReplacementPicker(index: Int) {
        val choices = appList.filter { !favorites.contains(it.packageName) }
        if (choices.isEmpty()) {
            Toast.makeText(this, if (nepaliMode) "बदल्न अर्को एप उपलब्ध छैन" else "No other apps available", Toast.LENGTH_SHORT).show()
            return
        }
        AlertDialog.Builder(this)
            .setTitle(if (nepaliMode) "एप बदल्नुहोस्" else "Replace dock app")
            .setItems(choices.map { it.label }.toTypedArray()) { _, which ->
                if (index in favorites.indices) {
                    favorites[index] = choices[which].packageName
                    savePreferences(); renderHome()
                }
            }
            .setNegativeButton(if (nepaliMode) "रद्द" else "Cancel", null)
            .show()
    }

'''
if dock_methods_anchor not in source:
    raise SystemExit("Dock action insertion point not found")
source = source.replace(dock_methods_anchor, dock_methods + dock_methods_anchor, 1)

main_file.write_text(source)

# Version 2.0.1 contains these user-facing controls and localization changes.
gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\\s*=\\s*\\d+", "versionCode = 14", gradle_text, count=1)
gradle_text = re.sub(r'versionName\\s*=\\s*"[^"]+"', 'versionName = "2.0.1"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
print("v2.0.1: long-press dock actions, built-in home widget toggles, centered Devanagari clock/date.")


# Phase 2.3: rebuild the home screen to match the approved Sagarmatha reference composition.
import base64 as _b64
_asset_dir = root / "app/src/main/res/drawable-nodpi"
_asset_dir.mkdir(parents=True, exist_ok=True)
_hero_b64 = """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"""
(_asset_dir / "sagarmatha_hero.jpg").write_bytes(_b64.b64decode(_hero_b64))

_source = main_file.read_text()
_home_start = _source.find("    private fun renderHome() {")
_home_end = _source.find("    private fun updateDateText() {", _home_start)
if _home_start < 0 or _home_end < 0:
    raise SystemExit("Cannot locate home screen method for approved visual redesign")

_new_home = r'''
    private fun renderHome() {
        showingDrawer = false
        handler.removeCallbacks(clockTick)
        window.statusBarColor = Color.rgb(3, 22, 49)
        window.navigationBarColor = Color.rgb(3, 22, 49)

        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(16), dp(4), dp(16), dp(8))
            background = GradientDrawable(
                GradientDrawable.Orientation.TOP_BOTTOM,
                intArrayOf(Color.rgb(3, 22, 49), Color.rgb(5, 35, 69), Color.rgb(3, 22, 49))
            )
            setOnApplyWindowInsetsListener { view, insets ->
                view.setPadding(dp(16), dp(4) + insets.systemWindowInsetTop, dp(16), dp(8) + insets.systemWindowInsetBottom)
                insets
            }
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        val brand = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_VERTICAL
        }
        brand.addView(TextView(this).apply {
            text = "🇳🇵  SAGARMATHA"
            textSize = 16f
            letterSpacing = .13f
            setTextColor(Color.rgb(255, 190, 65))
            typeface = Typeface.create("sans-serif", Typeface.BOLD)
        })
        brand.addView(TextView(this).apply {
            text = if (nepaliMode) "तपाईंको फोन, तपाईंको शैली" else "Your phone, your style"
            textSize = 10.5f
            setTextColor(Color.rgb(218, 228, 241))
        })
        header.addView(brand, LinearLayout.LayoutParams(0, dp(50), 1f))

        fun headerButton(label: String, description: String, action: () -> Unit): TextView =
            TextView(this).apply {
                text = label
                contentDescription = description
                textSize = 21f
                gravity = Gravity.CENTER
                setTextColor(Color.rgb(255, 193, 67))
                background = GradientDrawable().apply {
                    setColor(Color.argb(42, 112, 145, 184))
                    cornerRadius = dp(18).toFloat()
                }
                layoutParams = LinearLayout.LayoutParams(dp(43), dp(43)).apply { leftMargin = dp(7) }
                setOnClickListener { action() }
            }
        header.addView(headerButton(if (nepaliMode) "ने" else "EN", "Change language") {
            nepaliMode = !nepaliMode
            savePreferences()
            renderHome()
        })
        header.addView(headerButton("▦", "Widgets") { showWidgetManager() })
        header.addView(headerButton("⚙", "Settings") { showSettingsScreen() })
        root.addView(header)

        val scroll = ScrollView(this).apply {
            overScrollMode = View.OVER_SCROLL_NEVER
            clipToPadding = false
            setPadding(0, dp(3), 0, dp(8))
        }
        val content = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }

        // Hero: large centered Nepali clock, outlined Bikram Sambat date and the
        // same Everest mountain photograph extracted from the approved reference.
        val hero = FrameLayout(this).apply {
            layoutParams = LinearLayout.LayoutParams(-1, dp(222))
        }
        val mountain = ImageView(this).apply {
            setImageResource(R.drawable.sagarmatha_hero)
            scaleType = ImageView.ScaleType.CENTER_CROP
            alpha = .98f
        }
        hero.addView(mountain, FrameLayout.LayoutParams(-1, dp(112), Gravity.BOTTOM))
        val heroShade = View(this).apply {
            background = GradientDrawable(
                GradientDrawable.Orientation.TOP_BOTTOM,
                intArrayOf(Color.rgb(3, 22, 49), Color.argb(0, 3, 22, 49))
            )
        }
        hero.addView(heroShade, FrameLayout.LayoutParams(-1, dp(125), Gravity.TOP))

        val timeAndDate = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, dp(13), 0, 0)
        }
        clockView = TextView(this).apply {
            text = formatSagarmathaClock()
            textSize = 54f
            gravity = Gravity.CENTER
            setTextColor(Color.WHITE)
            typeface = Typeface.create("sans-serif-light", Typeface.NORMAL)
            includeFontPadding = false
        }
        timeAndDate.addView(clockView, LinearLayout.LayoutParams(-1, dp(78)))
        dateView = TextView(this).apply {
            textSize = 14f
            gravity = Gravity.CENTER
            setTextColor(Color.WHITE)
            setPadding(dp(15), dp(7), dp(15), dp(7))
            background = GradientDrawable().apply {
                setColor(Color.argb(24, 255, 255, 255))
                cornerRadius = dp(24).toFloat()
                setStroke(dp(1), Color.rgb(255, 190, 55))
            }
        }
        timeAndDate.addView(dateView, LinearLayout.LayoutParams(-2, -2).apply { topMargin = dp(3) })
        hero.addView(timeAndDate, FrameLayout.LayoutParams(-1, -2, Gravity.TOP))
        content.addView(hero)

        // Search field: full-width translucent rounded bar.
        val search = EditText(this).apply {
            hint = if (nepaliMode) "एप वा केही खोज्नुहोस्" else "Search apps"
            setHintTextColor(Color.rgb(207, 218, 232))
            setTextColor(Color.WHITE)
            textSize = 15f
            setSingleLine(true)
            setPadding(dp(18), 0, dp(16), 0)
            background = GradientDrawable().apply {
                setColor(Color.argb(62, 121, 153, 190))
                cornerRadius = dp(28).toFloat()
                setStroke(dp(1), Color.argb(105, 210, 224, 244))
            }
            setCompoundDrawablesWithIntrinsicBounds(android.R.drawable.ic_menu_search, 0, 0, 0)
            compoundDrawablePadding = dp(12)
            setOnFocusChangeListener { _, focused -> if (focused) showDrawer("") }
            setOnEditorActionListener { _, _, _ -> showDrawer(text.toString()); true }
            setOnClickListener { showDrawer("") }
        }
        content.addView(search, LinearLayout.LayoutParams(-1, dp(54)).apply {
            topMargin = dp(2); bottomMargin = dp(13)
        })

        // Four practical quick actions from the reference design.
        val quickActions = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            background = GradientDrawable().apply {
                setColor(Color.argb(25, 255, 255, 255))
                cornerRadius = dp(22).toFloat()
                setStroke(dp(1), Color.argb(80, 186, 208, 235))
            }
            setPadding(dp(5), dp(7), dp(5), dp(7))
        }
        fun quickAction(glyph: String, title: String, action: () -> Unit) {
            val item = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
                setPadding(dp(3), dp(2), dp(3), dp(2))
                isClickable = true
                setOnClickListener { action() }
            }
            item.addView(TextView(this).apply {
                text = glyph
                textSize = 25f
                gravity = Gravity.CENTER
                setTextColor(Color.rgb(255, 195, 68))
                background = GradientDrawable().apply {
                    setColor(Color.argb(55, 91, 129, 177))
                    cornerRadius = dp(17).toFloat()
                }
            }, LinearLayout.LayoutParams(dp(48), dp(48)))
            item.addView(TextView(this).apply {
                text = title
                textSize = 11f
                gravity = Gravity.CENTER
                setTextColor(Color.WHITE)
                setPadding(0, dp(5), 0, 0)
                maxLines = 1
            })
            quickActions.addView(item, LinearLayout.LayoutParams(0, -2, 1f))
        }
        quickAction("▦", if (nepaliMode) "पात्रो" else "Calendar") {
            runCatching {
                startActivity(Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_APP_CALENDAR))
            }
        }
        quickAction("☀", if (nepaliMode) "मौसम" else "Weather") { showDataSettings() }
        quickAction("▤", if (nepaliMode) "समाचार" else "News") { showDataSettings() }
        quickAction("⠿", if (nepaliMode) "एपहरू" else "Apps") { showDrawer("") }
        content.addView(quickActions, LinearLayout.LayoutParams(-1, dp(91)).apply {
            bottomMargin = dp(13)
        })

        // Two side-by-side information cards, matching the supplied reference.
        val bsDate = runCatching { NepaliCalendarService.todayNepali(nepaliMode) }
            .getOrElse { if (nepaliMode) "नेपाली मिति उपलब्ध भएन" else "Date unavailable" }
        val adDate = runCatching { NepaliCalendarService.todayEnglish() }
            .getOrElse { SimpleDateFormat("EEEE, d MMM yyyy", Locale.ENGLISH).format(Date()) }
        val infoRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        val calendarCard = widgetCard(
            if (nepaliMode) "▦  आजको पात्रो" else "▦  TODAY'S CALENDAR",
            if (nepaliMode) toDevanagariDigits(bsDate) else adDate,
            if (nepaliMode) "आजको तिथि" else "Today's date",
            "calendar"
        )
        calendarCard.layoutParams = LinearLayout.LayoutParams(0, dp(126), 1f).apply {
            rightMargin = dp(7); bottomMargin = 0
        }
        infoRow.addView(calendarCard)
        val weatherCard = buildWeatherCard()
        weatherCard.layoutParams = LinearLayout.LayoutParams(0, dp(126), 1f).apply {
            leftMargin = dp(7); bottomMargin = 0
        }
        infoRow.addView(weatherCard)
        if (showCalendarCard || showWeatherCard) {
            if (!showCalendarCard) infoRow.removeView(calendarCard)
            if (!showWeatherCard) infoRow.removeView(weatherCard)
            content.addView(infoRow, LinearLayout.LayoutParams(-1, dp(126)).apply { bottomMargin = dp(12) })
        }

        // News remains a live RSS card and retains its existing tap-to-configure action.
        if (showNewsCard) {
            val newsHeading = TextView(this).apply {
                text = if (nepaliMode) "▤  नेपाली समाचार" else "▤  NEPALI NEWS"
                textSize = 14f
                typeface = Typeface.DEFAULT_BOLD
                setTextColor(Color.rgb(255, 190, 55))
                setPadding(dp(14), dp(10), dp(14), dp(3))
            }
            val newsCard = buildNewsCard()
            newsCard.background = GradientDrawable().apply {
                setColor(Color.argb(34, 255, 255, 255))
                cornerRadius = dp(22).toFloat()
                setStroke(dp(1), Color.argb(78, 186, 208, 235))
            }
            newsCard.setPadding(dp(14), dp(8), dp(14), dp(12))
            val newsContainer = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                background = GradientDrawable().apply {
                    setColor(Color.argb(24, 255, 255, 255))
                    cornerRadius = dp(22).toFloat()
                    setStroke(dp(1), Color.argb(78, 186, 208, 235))
                }
            }
            newsContainer.addView(newsHeading)
            newsContainer.addView(newsCard)
            content.addView(newsContainer, LinearLayout.LayoutParams(-1, -2).apply {
                bottomMargin = dp(12)
            })
        }

        if (appFolders.isNotEmpty()) {
            val folderRow = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
            }
            appFolders.forEach { folder ->
                folderRow.addView(TextView(this).apply {
                    text = "▣  " + folder.name
                    textSize = 12f
                    setTextColor(Color.WHITE)
                    background = rounded(Color.argb(48, 255, 255, 255), 14)
                    setPadding(dp(12), dp(9), dp(12), dp(9))
                    setOnClickListener { openFolder(folder) }
                    setOnLongClickListener { confirmDeleteFolder(folder); true }
                }, LinearLayout.LayoutParams(-2, -2).apply { rightMargin = dp(7) })
            }
            content.addView(folderRow)
        }

        hostedWidgetIds.forEach { id ->
            val hosted = widgetViews[id] ?: createWidgetHostView(id)
            if (hosted != null) {
                (hosted.parent as? ViewGroup)?.removeView(hosted)
                val holder = LinearLayout(this).apply {
                    orientation = LinearLayout.VERTICAL
                    background = panel()
                    setPadding(dp(5), dp(5), dp(5), dp(5))
                }
                holder.addView(hosted, LinearLayout.LayoutParams(-1, dp(widgetHeightDp)))
                content.addView(holder, LinearLayout.LayoutParams(-1, -2).apply {
                    topMargin = dp(7); bottomMargin = dp(7)
                })
            }
        }

        scroll.addView(content)
        root.addView(scroll, LinearLayout.LayoutParams(-1, 0, 1f))

        // Five-slot premium dock pinned to the bottom edge.
        val dock = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            background = GradientDrawable().apply {
                setColor(Color.argb(47, 105, 139, 179))
                cornerRadius = dp(26).toFloat()
                setStroke(dp(1), Color.argb(95, 186, 208, 235))
            }
            setPadding(dp(5), dp(5), dp(5), dp(5))
            setOnLongClickListener {
                showDockAppPicker()
                true
            }
        }
        favorites.mapNotNull { pkg -> appList.find { it.packageName == pkg } }.take(5).forEach { app ->
            val tile = appTile(app, true)
            tile.setOnLongClickListener {
                showDockSlotActions(app, favorites.indexOf(app.packageName))
                true
            }
            dock.addView(tile, LinearLayout.LayoutParams(0, dp(67), 1f))
        }
        root.addView(dock, LinearLayout.LayoutParams(-1, dp(78)).apply { topMargin = dp(7) })
        setContentView(root)
        handler.post(clockTick)
    }

    private fun toDevanagariDigits(value: String): String =
        value.map { ch ->
            if (ch in '0'..'9') ('०'.code + (ch - '0')).toChar() else ch
        }.joinToString("")

    private fun formatSagarmathaClock(): String {
        val value = SimpleDateFormat("h:mm", Locale.ENGLISH).format(Date())
        return if (nepaliMode) toDevanagariDigits(value) else value
    }

    // Backward-compatible name used by the existing one-second clock ticker.
    private fun formatHomeClock(): String = formatSagarmathaClock()

'''
_source = _source[:_home_start] + _new_home + _source[_home_end:]

# Center the date pill and show the Bikram Sambat date in Devanagari in Nepali mode.
_date_start = _source.find("    private fun updateDateText() {")
_date_end = _source.find("    private fun buildWeatherCard()", _date_start)
if _date_start < 0 or _date_end < 0:
    raise SystemExit("Cannot locate date formatter for Nepali home clock")
_new_date = '''    private fun updateDateText() {
        dateView?.text = runCatching {
            if (nepaliMode) toDevanagariDigits(NepaliCalendarService.todayNepali(true))
            else NepaliCalendarService.todayEnglish()
        }.getOrElse {
            val fallback = SimpleDateFormat("EEEE, d MMMM yyyy", Locale.ENGLISH).format(Date())
            if (nepaliMode) toDevanagariDigits(fallback) else fallback
        }
    }

'''
_source = _source[:_date_start] + _new_date + _source[_date_end:]
_source = _source.replace(
    'clockView?.text = SimpleDateFormat("h:mm", Locale.getDefault()).format(Date())',
    'clockView?.text = formatSagarmathaClock()'
)
_source = _source.replace(
    'text = SimpleDateFormat("h:mm", Locale.getDefault()).format(Date())',
    'text = formatSagarmathaClock()'
)
main_file.write_text(_source)

gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\s*=\s*\d+", "versionCode = 15", gradle_text, count=1)
gradle_text = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "2.1.0"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
print("Sagarmatha Launcher v2.1.0: reference-matched Himalayan home screen and photo hero applied.")
