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
            shadowLayer = dp(3).toFloat(), 0f, dp(2).toFloat(), Color.BLACK
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
        contentRow.addView(gridScroll, LinearLayout.LayoutParams(0, 0, 1f))
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
                        if (letter == "#") !it.label.firstOrNull().orEmpty().uppercase().firstOrNull().orEmpty().first().isLetter()
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

        fun populateDrawerGrid() {
            grid.removeAllViews()
            val matches = filteredDrawerApps(search.text.toString(), activeCategory)
            if (matches.isEmpty()) {
                grid.addView(TextView(this).apply {
                    text = if (nepaliMode) "एप भेटिएन" else "No apps found"
                    textSize = 14f; setTextColor(Color.WHITE); gravity = Gravity.CENTER
                }, GridLayout.LayoutParams().apply { width = -1; height = dp(100); columnSpec = GridLayout.spec(0, 4) })
                return
            }
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
    source = re.sub(
        r'        val footer = LinearLayout\\(this\\)\\.apply \\{.*?        root\\.addView\\(footer, LinearLayout\\.LayoutParams\\(-1, dp\\(48\\)\\)\\)\\n?',
        '',
        source,
        count=1,
        flags=re.S
    )

# Ensure this visual rebuild gets its own Android update version.
app_gradle = root / "app/build.gradle.kts"
gradle_text = app_gradle.read_text()
gradle_text = re.sub(r"versionCode\\s*=\\s*\\d+", "versionCode = 9", gradle_text, count=1)
gradle_text = re.sub(r'versionName\\s*=\\s*"[^"]+"', 'versionName = "1.7.0"', gradle_text, count=1)
app_gradle.write_text(gradle_text)
main_file.write_text(source)
print("Premium Sagarmatha App Drawer implemented; version 1.7.0.")
