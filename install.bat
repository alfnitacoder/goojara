@echo off
echo ========================================
echo 🎬 GOOJARA MASTER - Installation Script
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo 📥 Please install Python 3.7+ from: https://python.org
    echo 📋 Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Show Python version
echo ✅ Python found:
python --version
echo.

:: Check Python version (3.7+)
python -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3.7+ is required
    echo 📥 Please upgrade Python from: https://python.org
    echo.
    pause
    exit /b 1
)

:: Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo 📥 Please install pip or upgrade Python
    echo.
    pause
    exit /b 1
)

echo ✅ pip found:
python -m pip --version
echo.

:: Install/upgrade pip
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip
echo.

:: Install required packages
echo 📦 Installing required packages...
echo.

if exist requirements.txt (
    echo 📋 Installing from requirements.txt...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install packages from requirements.txt
        echo 🔄 Trying manual installation...
        python -m pip install requests beautifulsoup4 lxml selenium
    )
) else (
    echo 📋 Installing packages manually...
    python -m pip install requests beautifulsoup4 lxml selenium
)

if %errorlevel% neq 0 (
    echo ❌ Failed to install required packages
    echo.
    echo 🔧 Troubleshooting tips:
    echo    - Try running as Administrator
    echo    - Check your internet connection
    echo    - Try: python -m pip install --user requests beautifulsoup4 lxml selenium
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ All packages installed successfully!
echo.

:: Check if Chrome/Chromium is available for Selenium
echo 🔍 Checking for Chrome/Chromium browser...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Chrome found in registry
) else (
    reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Chrome found in registry (32-bit)
    ) else (
        echo ⚠️  Chrome not found in registry
        echo 💡 Selenium will attempt to find Chrome automatically
    )
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo 🚀 To start GOOJARA MASTER:
echo    python goojara_master.py
echo.
echo 📖 For help and usage:
echo    python goojara_master.py
echo    Then choose option 10 (Show Help)
echo.
echo ========================================
echo 🎬 Ready to build your movie collection!
echo ========================================
echo.
pause
