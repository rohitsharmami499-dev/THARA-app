[app]

# (str) Title of your application
title = Jungle Friends

# (str) Package name
package.name = junglefriends

# (str) Package domain
package.domain = org.thara

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = images/*.png,*.png

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android build tools version to use (Stable version)
android.build_tools_version = 33.0.2

# (bool) Automatically accept SDK licenses
android.accept_sdk_licenses = True

# (list) List of architectures to build for
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
