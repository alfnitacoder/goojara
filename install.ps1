# GOOJARA MASTER - PowerShell Installation Script
# This script is safer and less likely to trigger antivirus warnings

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎬 GOOJARA MASTER - Installation Script" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found:" -ForegroundColor Green
        Write-Host $pythonVersion -ForegroundColor White
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Please install Python 3.7+ from: https://python.org" -ForegroundColor Yellow
    Write-Host "📋 Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check Python version (3.7+)
try {
    python -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python version check passed" -ForegroundColor Green
    } else {
        throw "Python version too old"
    }
} catch {
    Write-Host "❌ Python 3.7+ is required" -ForegroundColor Red
    Write-Host "📥 Please upgrade Python from: https://python.org" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is available
try {
    $pipVersion = python -m pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pip found:" -ForegroundColor Green
        Write-Host $pipVersion -ForegroundColor White
    } else {
        throw "pip not found"
    }
} catch {
    Write-Host "❌ pip is not available" -ForegroundColor Red
    Write-Host "📥 Please install pip or upgrade Python" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Install/upgrade pip
Write-Host "🔄 Upgrading pip..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip --quiet
    Write-Host "✅ pip upgraded successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  pip upgrade failed, continuing..." -ForegroundColor Yellow
}

Write-Host ""

# Install required packages
Write-Host "📦 Installing required packages..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "requirements.txt") {
    Write-Host "📋 Installing from requirements.txt..." -ForegroundColor Cyan
    try {
        python -m pip install -r requirements.txt --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Packages installed from requirements.txt" -ForegroundColor Green
        } else {
            throw "Failed to install from requirements.txt"
        }
    } catch {
        Write-Host "❌ Failed to install packages from requirements.txt" -ForegroundColor Red
        Write-Host "🔄 Trying manual installation..." -ForegroundColor Yellow
        try {
            python -m pip install requests beautifulsoup4 lxml selenium --quiet
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Manual installation successful" -ForegroundColor Green
            } else {
                throw "Manual installation failed"
            }
        } catch {
            Write-Host "❌ Failed to install required packages" -ForegroundColor Red
            Write-Host ""
            Write-Host "🔧 Troubleshooting tips:" -ForegroundColor Yellow
            Write-Host "   - Try running PowerShell as Administrator" -ForegroundColor White
            Write-Host "   - Check your internet connection" -ForegroundColor White
            Write-Host "   - Try: python -m pip install --user requests beautifulsoup4 lxml selenium" -ForegroundColor White
            Write-Host ""
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
} else {
    Write-Host "📋 Installing packages manually..." -ForegroundColor Cyan
    try {
        python -m pip install requests beautifulsoup4 lxml selenium --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Manual installation successful" -ForegroundColor Green
        } else {
            throw "Manual installation failed"
        }
    } catch {
        Write-Host "❌ Failed to install required packages" -ForegroundColor Red
        Write-Host ""
        Write-Host "🔧 Troubleshooting tips:" -ForegroundColor Yellow
        Write-Host "   - Try running PowerShell as Administrator" -ForegroundColor White
        Write-Host "   - Check your internet connection" -ForegroundColor White
        Write-Host "   - Try: python -m pip install --user requests beautifulsoup4 lxml selenium" -ForegroundColor White
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "✅ All packages installed successfully!" -ForegroundColor Green
Write-Host ""

# Check if Chrome/Chromium is available for Selenium
Write-Host "🔍 Checking for Chrome/Chromium browser..." -ForegroundColor Yellow

$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
)

$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "✅ Chrome found at: $path" -ForegroundColor Green
        $chromeFound = $true
        break
    }
}

if (-not $chromeFound) {
    Write-Host "⚠️  Chrome not found in common locations" -ForegroundColor Yellow
    Write-Host "💡 Selenium will attempt to find Chrome automatically" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎉 Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 To start GOOJARA MASTER:" -ForegroundColor Cyan
Write-Host "   python goojara_master.py" -ForegroundColor White
Write-Host ""
Write-Host "📖 For help and usage:" -ForegroundColor Cyan
Write-Host "   python goojara_master.py" -ForegroundColor White
Write-Host "   Then choose option 11 (Show Help)" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎬 Ready to build your movie collection!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
