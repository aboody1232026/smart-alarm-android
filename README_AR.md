# 🚀 Smart Alarm Pro - تطبيق منبّه ذكي

> تطبيق منبّه احترافي يتحكم بـ Tapo P100 و Gree AC على Android

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Android](https://img.shields.io/badge/android-5.0%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ الميزات الرئيسية

- 🔔 **منبّه متقدم** - ضبط الوقت والتكرار
- 🔌 **تحكم Tapo P100** - تشغيل/إيقاف المقبس الذكي
- ❄️ **تحكم Gree AC** - التحكم بدرجة الحرارة والوضع والمروحة
- 🔊 **أصوات منبّه** - تنبيهات صوتية متعددة
- 📱 **تطبيق Android** - يعمل على الهاتف الذكي
- 🌙 **منع نوم الجهاز** - يبقى التطبيق مستيقظ
- 💾 **حفظ تلقائي** - تذكر الإعدادات دائماً

---

## 🎯 البدء السريع

### 1️⃣ المتطلبات
```bash
# تثبيت Python و Java و Android SDK
pip install buildozer cython
```

### 2️⃣ البناء
```bash
# خيار أ: استقل السكريبت (الأفضل)
bash build.sh

# خيار ب: بناء يدوي
buildozer android debug
```

### 3️⃣ تثبيت
```bash
adb install -r bin/smartalarm-1.0.0-debug.apk
```

### 4️⃣ استخدم!
- افتح التطبيق
- أدخل بيانات Tapo و Gree
- ضبط المنبّه
- استمتع 😴

---

## 📚 الأدلة

| الدليل | الغرض |
|--------|-------|
| 🚀 [QUICK_START_AR.md](QUICK_START_AR.md) | **ابدأ هنا!** 5 خطوات فقط |
| 📖 [BUILD_GUIDE_AR.md](BUILD_GUIDE_AR.md) | دليل بناء مفصل بالعربية |
| ✅ [BUILD_CHECKLIST.md](BUILD_CHECKLIST.md) | قائمة تحقق شاملة |
| 📊 [ANDROID_BUILD_SUMMARY.md](ANDROID_BUILD_SUMMARY.md) | ملخص شامل للمشروع |
| 🔄 [VERSION_COMPARISON.md](VERSION_COMPARISON.md) | مقارنة Desktop vs Android |
| ⏰ [DAILY_USAGE_GUIDE.md](DAILY_USAGE_GUIDE.md) | دليل الاستخدام اليومي |
| 📁 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | هيكل المشروع |

---

## 🖥️ النظام المدعوم

### المتطلبات على الكمبيوتر:
- Python 3.9+
- Java Development Kit (JDK)
- Android SDK
- Buildozer

### المتطلبات على الهاتف:
- Android 5.0+ (API 21+)
- 2GB RAM (الحد الأدنى)
- 200MB مساحة خالية
- WiFi (نفس الشبكة)

---

## 🎬 لقطات الشاشة

### تبويبات التطبيق:
- ⏰ **المنبّه** - ضبط وقت المنبّه والإجراءات
- 🔌 **Tapo P100** - الاتصال والتحكم
- ❄️ **Gree AC** - التحكم والإعدادات
- 📝 **السجل** - عرض الأحداث

---

## 💡 نصائح للاستخدام الأمثل

✅ **قبل البدء:**
- اختبر جميع الاتصالات
- تأكد من WiFi مستقرة
- شغّل مع الشاحن

✅ **أثناء الاستخدام:**
- اترك التطبيق مفتوح
- تأكد من الصوت مفعّل
- لا تغلق التطبيق

✅ **حل المشاكل:**
- أعد تشغيل الأجهزة الذكية
- تحقق من IP والـ MAC
- اسأل في الدعم

---

## 🔧 البناء المتقدم

### بناء Release (محسّن):
```bash
buildozer android release
```

### تنظيف وبدء من جديد:
```bash
buildozer android clean
buildozer android debug
```

### عرض السجلات:
```bash
adb logcat
```

---

## 🛡️ الأمان

- 🔐 البيانات تُحفظ محلياً فقط
- 🚫 عدم إرسال أي بيانات للخوادم
- ✅ استخدم كلمات مرور قوية
- 📵 لا تشارك البيانات مع أحد

لمزيد التفاصيل، اقرأ [SECURITY_AUDIT.md](SECURITY_AUDIT.md)

---

## 🐛 الأخطاء الشائعة وحلولها

| الخطأ | الحل |
|------|------|
| Java غير موجود | حمّل JDK من oracle.com |
| Buildozer لا يعمل | `pip install --upgrade buildozer` |
| لا اتصال بـ Tapo | تأكد من IP والبريد صحيحين |
| المنبّه لا ينبّه | تأكد من الصوت والتطبيق مفتوح |

---

## 📞 الدعم

### أين تجد المساعدة؟
- 📖 اقرأ الأدلة أعلاه
- 🔍 ابحث عن مشكلتك في BUILD_CHECKLIST
- 💬 اسأل في المنتديات
- 🐛 أبلغ عن أخطاء

---

## 🔄 التحديثات المستقبلية

### قادم قريباً:
- [ ] تنبيهات متعددة
- [ ] جدولة متقدمة
- [ ] تنبيهات بصرية
- [ ] دعم Google Home
- [ ] مزامنة سحابية

---

## 📊 إحصائيات

- **عدد الأسطر (كود):** ~800
- **المكتبات:** 5+
- **الملفات:** 6 ملفات رئيسية
- **الأدلة:** 11 دليل توثيق
- **حجم APK:** 15-20 MB

---

## 🎉 شكر وتقدير

تم تطوير هذا المشروع بـ ❤️ لتسهيل حياتك!

**أشكر:**
- فريق Kivy للواجهة الرسومية
- مطورو PyP100 و greeclimate
- المستخدمين على الملاحظات

---

## 📝 الترخيص

هذا المشروع مرخص تحت MIT License

---

## 🌍 اللغات المدعومة

- 🇸🇦 العربية - واجهة كاملة وأدلة
- 🇺🇸 English - الملفات الفنية

---

## 👨‍💻 المطور

**Smart Alarm Team**

- التطوير: Python + Kivy
- التوثيق: عربي+English
- الدعم: Community-driven

---

## 🔗 الروابط المهمة

- **Python:** https://www.python.org/
- **Kivy:** https://kivy.org/
- **Android Studio:** https://developer.android.com/studio
- **Buildozer:** https://buildozer.readthedocs.io/

---

## 💬 التواصل

- 📧 البريد: smartalarm@example.com
- 🐙 GitHub: [SmartAlarmPro](https://github.com/smartalarmpro)
- 💬 Discord: [المجتمع](https://discord.gg/smartalarm)

---

## 📅 معلومات الإصدار

- **الإصدار:** 1.0.0
- **تاريخ الإصدار:** 2024/03/25
- **الحالة:** مستقر ✅
- **آخر تحديث:** 2024/03/25

---

<div align="center">

### استمتع بنومك الهانئ مع Smart Alarm Pro! 😴💤

**إذا أعجبك المشروع، ⭐ النجم**

</div>

---

**تم التحديث:** 2024/03/25  
**الإصدار:** 1.0.0  
**المطور:** Smart Alarm Team 🎉
