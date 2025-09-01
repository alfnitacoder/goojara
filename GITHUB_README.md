# 🎬 GOOJARA MASTER - Complete Movie Collection System

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/yourusername/goojara-master)

> **Your all-in-one solution for scraping, downloading, and managing movies from goojara.to**

## 🌟 **Features**

### **📥 Smart Scraping**
- **Automatic pagination** through all movie pages
- **Duplicate detection** using MD5 hashing
- **Real-time progress** tracking
- **Database management** with JSON storage

### **🎬 Intelligent Downloading**
- **Selenium-powered** video source detection
- **Title-based filenames** for easy organization
- **Download status tracking** (downloaded/failed/pending)
- **Resume capability** for interrupted downloads
- **Search by name** functionality

### **📊 Comprehensive Management**
- **Download statistics** and progress tracking
- **Search and filter** through your collection
- **Folder synchronization** with existing downloads
- **Failed download management** and retry options
- **Database backup** and recovery

## 🚀 **Quick Start**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/goojara-master.git
cd goojara-master
```

### **2. Run Installation Script**
**Windows:**
```cmd
install.bat
```

**macOS/Linux:**
```bash
./install.sh
```

### **3. Start GOOJARA MASTER**
```bash
python goojara_master.py
```

## 📋 **System Requirements**

- **Python 3.7+** (automatically detected)
- **Google Chrome** or **Chromium** browser
- **Internet connection** for package installation
- **Windows 10+**, **macOS 10.14+**, or **Linux**

## 🎯 **Usage Guide**

### **Main Menu Options**
1. **📥 Scrape/Update Movie List** - Build your movie database
2. **📊 View Download Statistics** - Check progress and completion
3. **🎬 Download Movies** - Multiple download options
4. **📋 View Recent Downloads** - See what you've downloaded
5. **🔍 Search Movies** - Find specific movies in your collection
6. **📁 Open Downloads Folder** - Access your movie files
7. **🗑️ Clear Failed Downloads** - Reset failed download statuses
8. **🔄 Reset Download Status** - Start fresh with all movies
9. **🔍 Sync Downloads Folder** - Update database with existing files
10. **📖 Show Help** - Comprehensive usage information

### **Download Options**
- **Download by number** (e.g., download 5 movies)
- **Download all pending** movies
- **Download failed** movies only
- **Download by year** (coming soon)
- **Download by genre** (coming soon)
- **Download by name** - Search and download specific movies

## 🏗️ **Architecture**

```
goojara_master.py              # 🎯 Main program & menu system
├── goojara_movie_scraper.py   # 📥 Web scraping engine
├── goojara_movie_downloader.py # 🎬 Download coordinator
├── goojara_selenium_auto_downloader.py # 🌐 Selenium automation
└── requirements.txt            # 📦 Python dependencies
```

## 🔧 **Installation Details**

### **Automatic Installation**
The installation scripts automatically:
- ✅ Detect Python version and compatibility
- ✅ Install/upgrade pip package manager
- ✅ Install all required Python packages
- ✅ Detect Chrome/Chromium browser
- ✅ Provide troubleshooting guidance

### **Manual Installation**
```bash
pip install -r requirements.txt
```

### **Required Packages**
- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML parsing and navigation
- `lxml` - Fast XML/HTML processing
- `selenium` - Web browser automation

## 📁 **File Structure**

```
goojara-master/
├── goojara_master.py              # 🎯 Main program
├── goojara_movie_scraper.py       # 📥 Movie scraper
├── goojara_movie_downloader.py    # 🎬 Movie downloader
├── goojara_selenium_auto_downloader.py # 🌐 Selenium engine
├── requirements.txt                # 📦 Dependencies
├── install.bat                     # 🪟 Windows installer
├── install.sh                      # 🐧 Unix installer
├── README.md                       # 📖 User documentation
├── GITHUB_README.md               # 📚 GitHub documentation
├── .gitignore                     # 🚫 Git exclusions
├── downloads/                      # 📁 Downloaded movies
├── goojara_movies_temp.json       # 💾 Movie database
└── goojara_movies_temp.txt        # 📋 Human-readable list
```

## 🎨 **Screenshots**

*[Add screenshots of the main menu, download progress, and statistics here]*

## 🔍 **How It Works**

### **1. Scraping Process**
- Fetches movie pages from goojara.to
- Extracts movie titles and links
- Handles pagination automatically
- Prevents duplicate entries
- Saves to both JSON and text formats

### **2. Download Process**
- Uses Selenium WebDriver for automation
- Navigates to movie pages
- Detects video sources automatically
- Downloads with title-based filenames
- Updates database with status

### **3. Management Features**
- Real-time progress tracking
- Search and filter capabilities
- Folder synchronization
- Error handling and recovery

## 🛠️ **Development**

### **Contributing**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Local Development**
```bash
# Clone and setup
git clone https://github.com/yourusername/goojara-master.git
cd goojara-master

# Install development dependencies
pip install -r requirements.txt

# Run tests (when implemented)
python -m pytest

# Run the application
python goojara_master.py
```

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ **Legal Notice**

**Important**: This tool is for educational purposes only. Please ensure you have the right to download any content and respect copyright laws. The developers are not responsible for any misuse of this tool.

## 🙏 **Acknowledgments**

- **Selenium** - Web automation framework
- **BeautifulSoup** - HTML parsing library
- **Requests** - HTTP library for Python
- **Goojara.to** - Movie source website

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/goojara-master/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/goojara-master/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/goojara-master/wiki)

## 🌟 **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/goojara-master&type=Date)](https://star-history.com/#yourusername/goojara-master&Date)

---

**Made with ❤️ for movie collectors**

*If this project helps you, please give it a ⭐ star!*
