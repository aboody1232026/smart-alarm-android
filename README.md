# Smart Alarm Pro - Android Edition

تطبيق منبّه ذكي لنظام Android مع التحكم بأجهزة Tapo P100 و Gree AC

**Smart Alarm Pro for Android - Control your smart devices on alarm trigger**

## ✨ Features

- ⏰ **Smart Alarm Clock** - Set alarms with custom actions
- 🔌 **Tapo P100 Control** - Automatically turn on/off your smart plug
- ❄️ **Gree AC Control** - Set your air conditioner to specific temperature
- 🔊 **Sound Generation** - Multiple alarm tones and alert sounds
- 📱 **Android Native UI** - Beautiful Kivy-based interface
- 🌙 **Schedule Support** - Advanced scheduling options
- 📊 **Activity Logging** - Track all actions

## 🚀 Quick Start

### For Users (Using Pre-built APK)

1. Download the latest APK from [Releases](https://github.com/aboody1232026/smart-alarm-android/releases)
2. Transfer to your Android device
3. Enable "Unknown Sources" in Settings > Security
4. Install and open the app

### For Developers (Building Locally)

#### Prerequisites
- Python 3.11+
- Android SDK
- Android NDK 25b or higher
- Java Development Kit (JDK 11+)

#### Setup

```bash
# Clone the repository
git clone https://github.com/aboody1232026/smart-alarm-android.git
cd smart-alarm-android

# Install dependencies
pip install -r requirements.txt
pip install buildozer cython

# (Windows) Install additional build tools if needed
# See BUILD_GUIDE.md for detailed instructions
```

#### Build APK

```bash
# Debug build (suitable for testing)
buildozer -v android debug

# Release build (for production)
buildozer -v android release
```

The first build takes 15-30 minutes. Subsequent builds are faster.

APK location: `bin/smartalarm-1.0.0-debug.apk`

## 📁 Project Structure

```
.
├── main.py                      # Entry point for the app
├── tapos_android.py             # Main Kivy app with UI and logic
├── buildozer.spec               # Android build configuration
├── requirements.txt             # Python dependencies
├── alarm_config.json            # User settings storage
├── build.sh                     # Linux/Mac build script
├── build.bat                    # Windows build script
├── BUILD_GUIDE.md              # Detailed build instructions
├── fallback_devices.py         # Mock device classes for testing
└── .github/workflows/
    ├── build-apk.yml           # GitHub Actions build workflow
    └── build-minimal.yml       # Alternative minimal build
```

## ⚙️ Configuration

### buildozer.spec

Key settings for Android build:
- **Android API:** 31 (with minapi 21 for compatibility)
- **Architecture:** arm64-v8a
- **Permissions:** WiFi control, Network access, Wake lock
- **Orientation:** Portrait

### alarm_config.json

User preferences stored as JSON:
```json
{
  "tapo_ip": "192.168.1.100",
  "tapo_email": "user@example.com",
  "gree_ip": "192.168.1.101",
  "alarms": []
}
```

## 🔧 Device Setup

### Tapo P100 Smart Plug

1. Set up in Tapo app
2. Note the IP address (e.g., 192.168.1.100)
3. In Smart Alarm Pro, go to "🔌 Tapo" tab
4. Enter credentials and IP address
5. Tap "Connect"

### Gree AC Air Conditioner

1. Ensure connected to WiFi
2. Find IP from your router
3. Find MAC address from device settings or router
4. In Smart Alarm Pro, go to "❄️ Gree" tab
5. Enter IP and MAC address
6. Tap "Connect"

## 📱 Using the App

### Setting an Alarm

1. Go to "⏰ المنبّه" (Alarm) tab
2. Select time using spinners
3. Choose devices to activate:
   - Toggle Tapo on/off
   - Set Gree temperature
4. Enable the alarm

### Managing Devices

**Tapo Tab:**
- Test connection
- Manual on/off control
- Device info

**Gree Tab:**
- Test connection
- Set temperature
- Power control
- Mode selection

### Logs

View all app activity in the "📝 السجل" (Logs) tab

## 🔌 Technical Details

### Architecture

- **UI Framework:** Kivy (Python cross-platform mobile)
- **Build System:** Buildozer (Python to APK compiler)
- **Device Control:** PyP100 (Tapo), greeclimate (Gree)
- **Scheduling:** schedule (Python task scheduler)

### Android Build Pipeline

1. Checkout code
2. Setup Android SDK/NDK
3. Install Python and dependencies
4. Compile with Cython
5. Build using Buildozer → Python-for-Android
6. Package into APK
7. Optional: Sign and release

### Performance

- First build: 15-30 minutes (downloads SDK/NDK)
- Subsequent builds: 5-10 minutes
- APK size: ~100-150 MB (debug)

## 🐛 Troubleshooting

### Build Fails on First Attempt

This is normal - Buildozer needs to download:
- Android SDK (~500 MB)
- Android NDK (~800 MB)
- Various build tools

Solution: Let it complete, or check:
```bash
buildozer -v android debug 2>&1 | tee build.log
```

### Device Connection Issues

- Ensure devices are on same WiFi network
- Check firewall settings
- Verify IP addresses are correct
- Try restarting both the device and app

### App Crashes

Enable verbose logging:
```bash
adb logcat | grep smartalarm
```

## 📦 GitHub Actions Build

The project includes automated CI/CD:

1. **Push to main** → Automatic build starts
2. **Build completes** → APK available in Actions tab
3. **Download artifact** → Deploy to devices

Manual trigger:
```bash
git push origin main
# Then check: https://github.com/aboody1232026/smart-alarm-android/actions
```

## 📝 License

[Specify your license here]

## 👥 Contributing

[Contribution guidelines]

## 📞 Support

- Check BUILD_GUIDE.md for detailed instructions
- Review GitHub Issues for known problems
- Check build logs in GitHub Actions for errors

---

**حقوق التأليف © 2024 - تطبيق منبّه ذكي**

Made with ❤️ for Android
