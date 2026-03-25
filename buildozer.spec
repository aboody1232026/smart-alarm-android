[app]

# الاسم والإصدار
title = Smart Alarm Pro
package.name = smartalarm
package.domain = org.smartalarm

# الملف الرئيسي
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# استبعاد الملفات غير الضرورية
source.exclude_exts = apk,exe,md,rst,txt
source.exclude_dirs = tests,bin,build,.github,__pycache__,.buildozer,.git,.venv,venv

# الإصدار
version = 1.0.0

# المتطلبات - المكتبات الأساسية (بسيطة للبناء الأول)
requirements = python3,kivy,schedule,requests

# الأذونات
android.permissions = INTERNET,ACCESS_NETWORK_STATE,CHANGE_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,WAKE_LOCK,KEEP_SCREEN_ON

# ميزات Android
android.features = android.hardware.wifi

# ABI
android.archs = arm64-v8a

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

# البناء
log_level = 2
warn_on_root = 1

# Buildozer settings for stability
android.release_artifact = apk
fullscreen = 1
android.allow_backup = True
