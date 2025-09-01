#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "🎬 GOOJARA MASTER - Installation Script"
echo "========================================"
echo

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}💡 $1${NC}"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed"
        echo
        echo "📥 Please install Python 3.7+ using your package manager:"
        echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "   CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "   macOS: brew install python3"
        echo "   Or download from: https://python.org"
        echo
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Show Python version
print_status "Python found:"
$PYTHON_CMD --version
echo

# Check Python version (3.7+)
$PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    print_error "Python 3.7+ is required"
    echo "📥 Please upgrade Python using your package manager"
    echo
    exit 1
fi

# Check if pip is available
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    print_error "pip is not available"
    echo "📥 Please install pip or upgrade Python"
    echo
    exit 1
fi

print_status "pip found:"
$PYTHON_CMD -m pip --version
echo

# Install/upgrade pip
echo "🔄 Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip
echo

# Install required packages
echo "📦 Installing required packages..."
echo

if [ -f "requirements.txt" ]; then
    echo "📋 Installing from requirements.txt..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_warning "Failed to install packages from requirements.txt"
        echo "🔄 Trying manual installation..."
        $PYTHON_CMD -m pip install requests beautifulsoup4 lxml selenium
    fi
else
    echo "📋 Installing packages manually..."
    $PYTHON_CMD -m pip install requests beautifulsoup4 lxml selenium
fi

if [ $? -ne 0 ]; then
    print_error "Failed to install required packages"
    echo
    echo "🔧 Troubleshooting tips:"
    echo "   - Try: $PYTHON_CMD -m pip install --user requests beautifulsoup4 lxml selenium"
    echo "   - Check your internet connection"
    echo "   - Try running with sudo (Linux/macOS)"
    echo
    exit 1
fi

echo
print_status "All packages installed successfully!"
echo

# Check for Chrome/Chromium (different methods for different OS)
echo "🔍 Checking for Chrome/Chromium browser..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [ -d "/Applications/Google Chrome.app" ]; then
        print_status "Chrome found in Applications"
    elif [ -d "/Applications/Chromium.app" ]; then
        print_status "Chromium found in Applications"
    else
        print_warning "Chrome/Chromium not found in Applications"
        print_info "Selenium will attempt to find Chrome automatically"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v google-chrome &> /dev/null; then
        print_status "Chrome found in PATH"
    elif command -v chromium-browser &> /dev/null; then
        print_status "Chromium found in PATH"
    elif [ -f "/usr/bin/google-chrome" ]; then
        print_status "Chrome found in /usr/bin"
    elif [ -f "/usr/bin/chromium-browser" ]; then
        print_status "Chromium found in /usr/bin"
    else
        print_warning "Chrome/Chromium not found"
        print_info "Selenium will attempt to find Chrome automatically"
        echo "💡 To install Chrome on Ubuntu/Debian:"
        echo "   wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -"
        echo "   sudo sh -c 'echo \"deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main\" >> /etc/apt/sources.list.d/google.list'"
        echo "   sudo apt update && sudo apt install google-chrome-stable"
    fi
else
    print_info "OS detection failed, Selenium will attempt to find Chrome automatically"
fi

echo
echo "🎉 Installation completed successfully!"
echo
echo "🚀 To start GOOJARA MASTER:"
echo "   $PYTHON_CMD goojara_master.py"
echo
echo "📖 For help and usage:"
echo "   $PYTHON_CMD goojara_master.py"
echo "   Then choose option 10 (Show Help)"
echo
echo "========================================"
echo "🎬 Ready to build your movie collection!"
echo "========================================"
echo
