# 🚀 دليل بناء APK لـ Smart Alarm Pro

## المتطلبات

### 1. تثبيت Python والأدوات المطلوبة

```bash
# تثبيت Python 3.11+ من:
# https://www.python.org/downloads/

# تثبيت Buildozer و المتطلبات
pip install buildozer cython

# تثبيت Java Development Kit (JDK)
# من: https://www.oracle.com/java/technologies/downloads/

# تثبيت Android SDK
# من: https://developer.android.com/studio
```

### 2. متطلبات Linux/WSL (للـ Buildozer)

إذا كنت على Windows، استخدم WSL2:

```bash
# في WSL2
sudo apt-get update
sudo apt-get install -y \
    openjdk-11-jdk \
    ant \
    git \
    python3-dev \
    python3-pip \
    libffi-dev \
    libssl-dev \
    libopenjp2-7 \
    libtiff5 \
    libjasper1 \
    libilmbase23 \
    libopenexr23
```

### 3. إعداد Buildozer

```bash
# الذهاب إلى مجلد المشروع
cd perfect

# عرض الإعدادات الحالية
buildozer android debug --help

# تكوين الأذونات والإعدادات (تم التحضير مسبقاً في buildozer.spec)
```

## خطوات البناء

### الطريقة الأولى: بناء مباشر (أسهل)

```bash
# بناء APK للتطوير (Debug)
buildozer android debug

# سيستغرق الأمر 10-20 دقيقة في أول مرة
# ستجد APK في: bin/smartalarm-1.0.0-debug.apk
```

### الطريقة الثانية: بناء محسّن (Production)

```bash
# بناء APK للإنتاج (Release)
buildozer android release

# سيستغرق وقتاً أطول
# ستجد APK في: bin/smartalarm-1.0.0-release.apk
```

## حل مشاكل البناء الشائعة

### المشكلة: "Could not find Java"

```bash
# تعيين مسار Java
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# أو عدّل buildozer.spec:
# android.java_dir = /path/to/java
```

### المشكلة: "Could not find gradle"

```bash
# تطبيق النظيف والمحاولة مجدداً
buildozer android clean
buildozer android debug
```

### المشكلة: أخطاء في المكتبات

```bash
# تحديث buildozer و p4a
pip install --upgrade buildozer
pip install --upgrade python-for-android

# إعادة بناء
buildozer android clean
buildozer android debug
```

## الخطوات بعد البناء الناجح

### 1. نقل APK إلى الجهاز

```bash
# إذا كان الجهاز متصلاً عبر USB
adb install bin/smartalarm-1.0.0-debug.apk

# أو نسخ يدويّاً إلى هاتفك
# وanimate اضغط على الملف لتثبيته
```

### 2. منح الأذونات للتطبيق

عند فتح التطبيق أول مرة:
- اضغط "السماح" عندما يطلب الأذونات
- تأكد من تفعيل WiFi
- تأكد من السماح بالوصول للشبكة

### 3. استخدام التطبيق

- أدخل بيانات Tapo P100 (IP، البريد، كلمة المرور)
- أدخل بيانات Gree AC (IP، MAC)
- ضبط وقت المنبّه
- اختبر الاتصالات قبل النوم

## ملاحظات مهمة

### ⚠️ استهلاك البطارية

التطبيق يحتفظ الجهاز مستيقظ ليعمل المنبّه. قد تستهلك البطارية بسرعة.

الحلول:
- شغّل التطبيق طوال الليل (أثناء الشحن)
- تأكد من أن الجهاز متصل بالشاحن
- زد مدة الغفوة إذا لزم الأمر

### 🔌 الاتصال بالشبكة

يجب أن يكون الجهاز على نفس الشبكة (WiFi) مع:
- مقبس Tapo P100
- مكيف Gree AC

### 🔐 الأمان

- لا تشارك بيانات Tapo Cloud مع أحد
- احذف بيانات الاعتماد من التطبيق إذا أعطيت الهاتف لشخص آخر
- استخدم كلمات مرور قوية

## تطوير وتطبيق تحديثات

### تحديث التطبيق

```bash
# عدّل الملفات حسب الحاجة
# ثم أعد البناء

buildozer android clean
buildozer android debug

# نقل النسخة الجديدة
adb install -r bin/smartalarm-1.0.0-debug.apk
```

## الدعم والمساعدة

**المشاكل الشائعة:**

1. **التطبيق يتوقف عند الفتح**
   - تأكد من تثبيت Kivy بشكل صحيح
   - شغّل `logcat` لرؤية الأخطاء

2. **عدم الاتصال بـ Tapo/Gree**
   - تأكد من صحة بيانات IP والـ MAC
   - اختبر الاتصال من جهاز آخر على نفس الشبكة
   - أعد تشغيل الأجهزة

3. **عدم تشغيل المنبّه**
   - تأكد من أن التطبيق مفتوح
   - تأكد من عدم إيقاف الصوت في الجهاز
   - جرّب اختبار المنبّه أولاً

## الملفات المهمة

- **tapos_android.py** - الكود الرئيسي للتطبيق
- **buildozer.spec** - إعدادات البناء
- **requirements.txt** - المكتبات المطلوبة
- **alarm_config.json** - ملف حفظ الإعدادات (يُنشأ تلقائياً)

## النسخ التالية

سيتم إضافة ميزات جديدة:
- ✅ دعم إذعانات متعددة
- ✅ تنبيهات بصرية بالإضافة للصوتية
- ✅ نسخة احتياطية سحابية للبيانات
- ✅ دعم أجهزة ذكية أخرى (Philips Hue, Tuya, إلخ)

---

**تم إنشاؤها:** $(date)
**الإصدار:** 1.0.0
**المطور:** Smart Alarm Team
