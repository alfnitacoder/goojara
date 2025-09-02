# 🎬 GOOJARA MASTER - Complete Movie Collection System

Your all-in-one solution for scraping, downloading, and managing movies from goojara.to.

## 🚀 **Quick Start**

```bash
python goojara_master.py
```

## 📁 **What You Get**

- **🎯 1,015+ Movies** - Automatically scraped from goojara.to
- **📥 Smart Downloads** - Uses proven selenium technique
- **📊 Real-time Tracking** - Always know your progress
- **🔄 Auto-sync** - Keeps database and files in sync
- **🎨 Beautiful Interface** - Menu-driven, user-friendly

## 🎬 **Features**

### **📥 Scraping**

- Scrape all movie pages automatically
- Update existing movie list
- Handle pagination and duplicates

### **🎬 Downloading**

- Download movies with title filenames
- Resume interrupted downloads
- Track success/failure status

### **📊 Management**

- View download statistics
- Search through your collection
- Sync existing downloads
- Clear failed downloads

## 📋 **File Structure**

```
goojara_master.py              # 🎯 Main program (run this!)
goojara_movie_scraper.py       # 📥 Movie scraper
goojara_movie_downloader.py    # 🎬 Movie downloader
goojara_selenium_auto_downloader.py  # 🌐 Selenium engine
requirements.txt                # 📦 Dependencies
goojara_movies_temp.json       # 💾 Movie database
downloads/                     # 📁 Downloaded movies
```

## 🛠️ **Installation**

### **🚀 Quick Install (Recommended)**

**Windows:**
```cmd
install.ps1
```

**macOS/Linux:**
```bash
./install.sh
```

### **📦 Manual Installation**

```bash
pip install -r requirements.txt
```

### **🔧 System Requirements**

- **Python 3.7+** (automatically detected)
- **Chrome/Chromium** browser (for Selenium)
- **Internet connection** (for package installation)

## 🎯 **Usage**

1. **Start**: `python goojara_master.py`
2. **Scrape**: Option 1 - Build your movie database
3. **Download**: Option 3 - Download movies
4. **Monitor**: Option 2 - Check progress
5. **Sync**: Option 9 - Update existing downloads

## 💡 **Pro Tips**

- Start with scraping to build your database
- Download in small batches (5-10 movies)
- Use sync function to update existing downloads
- Check statistics regularly

## 🔧 **Troubleshooting**

### **Installation Issues**
- **Python not found**: Run the installation script or install Python 3.7+
- **Package installation fails**: Try `pip install --user` or run as administrator
- **Chrome not found**: Install Google Chrome or Chromium browser

### **Download Issues**
- **No video sources found**: Some movies may be temporarily unavailable
- **Selenium errors**: Ensure Chrome/Chromium is installed and up to date
- **Permission errors**: Check folder permissions and run as administrator if needed

## 🎉 **Ready to Use**

Your complete movie collection system is ready! Run `python goojara_master.py` and start building your movie library.

---

**Built with ❤️ for movie collectors**
