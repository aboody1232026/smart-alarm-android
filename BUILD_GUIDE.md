# Smart Alarm Pro for Android - Build & Deployment Guide

## 📋 Current Status

Your Android APK is being built automatically via GitHub Actions. The build process will:

1. ✅ Set up Android SDK/NDK environment
2. ✅ Install Python dependencies (Kivy, schedule, etc.)
3. ✅ Compile Python code to Android bytecode
4. ✅ Package everything into an APK file
5. ✅ Upload the APK as a release artifact

## 🔨 Build Status

**Repository:** https://github.com/aboody1232026/smart-alarm-android

**Latest Workflow:** Check here for real-time build status:
https://github.com/aboody1232026/smart-alarm-android/actions

## 📱 Installation on Android Device

Once the APK is built and downloaded:

1. **Transfer to Device:**
   - Download the APK from GitHub Actions artifacts
   - Connect your Android phone to your computer
   - Copy the APK file to your device

2. **Enable Installation from Unknown Sources:**
   - Go to Settings > Security
   - Enable "Allow installation from unknown sources"

3. **Install:**
   - Open the APK file
   - Tap "Install"
   - Grant necessary permissions (Network access, WiFi control, etc.)

4. **Launch:**
   - Tap "Open" after installation
   - Or find the app in your app drawer

## ⚙️ Device Setup

### For Tapo P100 Smart Plug:

1. Open the Tapo app and set up your P100 plug
2. Note the device IP address (usually shown in Tapo app)
3. In Smart Alarm Pro:
   - Go to "🔌 Tapo" tab
   - Enter IP address
   - Enter your Tapo account email
   - Enter your Tapo account password
   - Tap "Connect"

### For Gree AC Air Conditioner:

1. Ensure your Gree AC is connected to WiFi
2. Get the MAC address from your router or Gree app
3. In Smart Alarm Pro:
   - Go to "❄️ Gree" tab
   - Enter the IP address of your AC unit
   - Enter the MAC address
   - Tap "Connect"

## ⚠️ Known Issues

### PyP100 and greeclimate libraries

These libraries control your Tapo P100 and Gree AC. They may take longer to compile for Android (first build can take 20-30 minutes).

If the build fails with errors about PyP100 or greeclimate:

**Option 1 (Recommended):** Wait for GitHub Actions to complete - it will retry automatically

**Option 2:** Remove these from `requirements.txt` temporarily to test basic alarm functionality:
```
# Temporarily comment out:
# PyP100>=0.0.1
# greeclimate>=1.0.0
```

Then re-enable them once basic build works.

## 🐛 Troubleshooting

### Build takes too long
- First build downloads Android SDK/NDK (500+ MB) - this is normal
- Subsequent builds are faster

### APK won't install
- Ensure "Unknown Sources" is enabled
- Check that your Android version is compatible (API 21+)
- Try uninstalling any previous version first

### App crashes on startup
- Check Android logcat for error messages: `adb logcat`
- Report any error messages to the developer

### Device connection fails
- Verify device is on same WiFi network as phone
- Check firewall isn't blocking connections
- Try restarting the device

## 📞 Support

For detailed error messages from the build:
1. Go to https://github.com/aboody1232026/smart-alarm-android/actions
2. Click on the failed workflow run
3. Scroll down to see the error in "Build APK (Debug)" step
4. Copy-paste the error here for support

## 📦 Build Artifacts

- **Debug APK:** smartalarm-1.0.0-debug.apk (~100-150 MB)
- **Release APK:** Not configured yet (can be added later)

Debug APK is suitable for testing and personal use.

## 🔄 Rebuilding

To trigger a new build:

1. Push changes to the repository
2. GitHub Actions will automatically build
3. Download the APK from the Actions tab

Or build locally:
```powershell
# Windows
.\build.bat debug

# Or manually
buildozer -v android debug
```

This takes 15-30 minutes on first attempt.
