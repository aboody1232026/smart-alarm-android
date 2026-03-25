@echo off
REM Smart Alarm Android Build Script - Windows
REM This script builds the APK locally using Buildozer

setlocal enabledelayedexpansion

cls
echo.
echo ====================================================
echo    Smart Alarm Android - Local APK Builder
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if buildozer is installed
pip show buildozer >nul 2>&1
if errorlevel 1 (
    echo WARNING: buildozer not installed
    echo Installing buildozer...
    pip install buildozer cython
)

echo ✓ buildozer ready
echo.

REM Get build target
set TARGET=%1
if "!TARGET!"=="" set TARGET=debug

if "!TARGET!" neq "debug" if "!TARGET!" neq "release" (
    echo ERROR: Invalid target. Use 'debug' or 'release'
    exit /b 1
)

echo.
echo Building APK ^(target: !TARGET!^)...
echo.

REM Build
buildozer -v android !TARGET!

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    echo Check the output above for details
    exit /b 1
)

echo.
echo ====================================================
echo ✓ BUILD SUCCESSFUL
echo ====================================================

REM Check for APK
if exist "bin\smartalarm-1.0.0-!TARGET!.apk" (
    echo.
    echo APK Location:
    echo bin\smartalarm-1.0.0-!TARGET!.apk
    echo.
    dir /b "bin\smartalarm-1.0.0-!TARGET!.apk"
) else (
    echo.
    echo WARNING: APK not found at expected location
    echo Searching for any APK files...
    dir /s "*.apk" 2>nul || echo No APK files found
)

echo.
pause
