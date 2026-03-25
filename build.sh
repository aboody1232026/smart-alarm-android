#!/bin/bash
# 🚀 Smart Alarm Pro - Build Script for Android
# نص برمجي لبناء تطبيق Android بسهولة

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🚀 Smart Alarm Pro - Android APK Builder                  ║"
echo "║   بناء تطبيق Smart Alarm Pro على Android                   ║"
echo "╚════════════════════════════════════════════════════════════╝"

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# الدوال
print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# التحقق من المتطلبات
check_requirements() {
    print_info "فحص المتطلبات..."
    
    # Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 غير مثبت"
        exit 1
    fi
    print_success "Python3 متوفر"
    
    # buildozer
    if ! command -v buildozer &> /dev/null; then
        print_warning "buildozer غير مثبت"
        print_info "جاري التثبيت..."
        pip install buildozer cython
    fi
    print_success "buildozer متوفر"
    
    # Java
    if ! command -v java &> /dev/null; then
        print_error "Java Development Kit (JDK) غير مثبت"
        echo "  يُرجى تحميل JDK من: https://www.oracle.com/java/technologies/downloads/"
        exit 1
    fi
    print_success "Java متوفر"
}

# تنظيف البناء السابق
clean_build() {
    print_info "تنظيف البناء السابق..."
    if [ -d "bin" ]; then
        rm -rf bin
        print_success "تم تنظيف مجلد bin"
    fi
    if [ -d "build" ]; then
        rm -rf build
        print_success "تم تنظيف مجلد build"
    fi
}

# بناء APK
build_apk() {
    print_info "بدء بناء APK..."
    
    case "$1" in
        debug)
            print_info "بناء Debug APK..."
            buildozer android debug
            ;;
        release)
            print_info "بناء Release APK..."
            buildozer android release
            ;;
        *)
            print_error "خيار غير صحيح: $1"
            exit 1
            ;;
    esac
}

# إيجاد ملف APK
find_apk() {
    if [ -f "bin/smartalarm-1.0.0-debug.apk" ]; then
        print_success "تم العثور على APK: bin/smartalarm-1.0.0-debug.apk"
        echo "  الحجم: $(du -h bin/smartalarm-1.0.0-debug.apk | cut -f1)"
        return 0
    elif [ -f "bin/smartalarm-1.0.0-release.apk" ]; then
        print_success "تم العثور على APK: bin/smartalarm-1.0.0-release.apk"
        echo "  الحجم: $(du -h bin/smartalarm-1.0.0-release.apk | cut -f1)"
        return 0
    else
        print_error "لم يتم العثور على ملف APK"
        return 1
    fi
}

# التثبيت على الجهاز
install_apk() {
    print_info "محاولة التثبيت على الجهاز..."
    
    if ! command -v adb &> /dev/null; then
        print_warning "ADB غير مثبت"
        echo "  يُرجى تثبيت Android SDK أو استخدام adb يدويّاً"
        return 1
    fi
    
    # البحث عن APK
    if [ -f "bin/smartalarm-1.0.0-debug.apk" ]; then
        adb install -r bin/smartalarm-1.0.0-debug.apk
    elif [ -f "bin/smartalarm-1.0.0-release.apk" ]; then
        adb install -r bin/smartalarm-1.0.0-release.apk
    else
        print_error "لم يتم العثور على ملف APK للتثبيت"
        return 1
    fi
    
    print_success "تم التثبيت بنجاح!"
}

# القائمة الرئيسية
show_menu() {
    echo ""
    echo "اختر وضع البناء:"
    echo "  1) Debug Build (سريع - للتطوير)"
    echo "  2) Release Build (آمن - للإطلاق)"
    echo "  3) بناء + تثبيت على الجهاز"
    echo "  4) تنظيف وبدء من جديد"
    echo "  5) فحص ملface APK الموجودة"
    echo "  6) خروج"
    echo ""
    read -p "اختيارك (1-6): " choice
}

# السيناريو الرئيسي
main() {
    # فحص المتطلبات
    check_requirements
    
    # القائمة
    while true; do
        show_menu
        case $choice in
            1)
                build_apk "debug"
                find_apk
                ;;
            2)
                build_apk "release"
                find_apk
                ;;
            3)
                build_apk "debug"
                find_apk && install_apk
                ;;
            4)
                clean_build
                build_apk "debug"
                find_apk
                ;;
            5)
                find_apk
                ;;
            6)
                print_success "وداعاً! 👋"
                exit 0
                ;;
            *)
                print_error "اختيار غير صحيح"
                ;;
        esac
    done
}

# تشغيل البرنامج
main "$@"
