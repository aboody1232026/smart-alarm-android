[app]

# الاسم والإصدار
title = Smart Alarm Pro
package.name = smartalarm
package.domain = org.smartalarm

# الملف الرئيسي
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# الإصدار
version = 1.0.0

# المتطلبات
requirements = python3,kivy,schedule,PyP100,greeclimate,android,jnius,requests,cryptography

# الأذونات
android.permissions = INTERNET,ACCESS_NETWORK_STATE,CHANGE_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,WAKE_LOCK,KEEP_SCREEN_ON,MODIFY_AUDIO_SETTINGS

# ميزات Android
android.features = android.hardware.wifi

# ABI
android.archs = arm64-v8a,armeabi-v7a

# الأيقونة والشاشة الترحيبية
#android.icon = data/icon.png
#android.presplash = data/presplash.png

# التقديم
orientation = portrait

# إصدار SDK
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# جافا
android.gradle_dependencies = 

# متطلبات Python الإضافية
p4a.source_dir = 

# نسخة Python
android.python_for_android_branch = develop

# Build
log_level = 2
warn_on_root = 1
