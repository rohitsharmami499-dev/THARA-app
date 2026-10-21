[app]
title = Jungle Friends
package.name = junglefriends
package.domain = org.thara
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = images/*.png,*.png
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
