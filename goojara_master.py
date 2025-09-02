#!/usr/bin/env python3
"""
Goojara Master - All-in-One Movie Management System
Provides a menu-driven interface for scraping, viewing, and downloading movies
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

class GoojaraMaster:
    def __init__(self):
        self.json_file = "goojara_movies_temp.json"
        self.movies_data = {}
        self.load_movies_data()
        
    def load_movies_data(self):
        """Load the scraped movies data from JSON"""
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.movies_data = json.load(f)
                print(f"✅ Loaded {self.movies_data['metadata']['total_movies']} movies from database")
            else:
                print("⚠️  No movie database found. You'll need to scrape movies first.")
        except Exception as e:
            print(f"❌ Error loading database: {e}")
    
    def show_main_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 60)
        print("🎬 GOOJARA MASTER - Movie Collection Manager")
        print("=" * 60)
        print("1. 📥 Scrape/Update Movie List")
        print("2. 📊 View Download Statistics")
        print("3. 🎬 Download Movies")
        print("4. 📋 View Recent Downloads")
        print("5. 🔍 Search Movies")
        print("6. 📁 Open Downloads Folder")
        print("7. 🗑️  Clear Failed Downloads")
        print("8. 🔄 Reset Download Status")
        print("9. 🔍 Sync Downloads Folder")
        print("10. 🔧 Fix Database Inconsistencies")
        print("11. 📖 Show Help")
        print("0. 🚪 Exit")
        print("=" * 60)
    
    def scrape_movies(self):
        """Option 1: Scrape/Update movie list"""
        print("\n📥 SCRAPE/UPDATE MOVIE LIST")
        print("-" * 40)
        
        if not os.path.exists("goojara_movie_scraper.py"):
            print("❌ Movie scraper script not found!")
            return
        
        print("Choose scraping option:")
        print("1. Scrape all pages (recommended)")
        print("2. Scrape specific number of pages")
        print("3. Scrape from specific page")
        print("0. Back to main menu")
        
        choice = input("\nEnter your choice (1-3, 0): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting full movie scraping...")
            try:
                subprocess.run([sys.executable, "goojara_movie_scraper.py"], check=True)
                print("\n✅ Scraping completed! Reloading database...")
                self.load_movies_data()
            except subprocess.CalledProcessError as e:
                print(f"❌ Scraping failed: {e}")
            except KeyboardInterrupt:
                print("\n⚠️  Scraping interrupted by user")
        
        elif choice == "2":
            try:
                pages = int(input("Enter number of pages to scrape: "))
                print(f"\n🚀 Starting scraping of {pages} pages...")
                subprocess.run([sys.executable, "goojara_movie_scraper.py", "https://ww1.goojara.to/watch-movies?p=1", str(pages)], check=True)
                print("\n✅ Scraping completed! Reloading database...")
                self.load_movies_data()
            except ValueError:
                print("❌ Invalid number of pages")
            except subprocess.CalledProcessError as e:
                print(f"❌ Scraping failed: {e}")
            except KeyboardInterrupt:
                print("\n⚠️  Scraping interrupted by user")
        
        elif choice == "3":
            page_url = input("Enter page URL to start from: ").strip()
            if page_url:
                print(f"\n🚀 Starting scraping from: {page_url}")
                try:
                    subprocess.run([sys.executable, "goojara_movie_scraper.py", page_url], check=True)
                    print("\n✅ Scraping completed! Reloading database...")
                    self.load_movies_data()
                except subprocess.CalledProcessError as e:
                    print(f"❌ Scraping failed: {e}")
                except KeyboardInterrupt:
                    print("\n⚠️  Scraping interrupted by user")
            else:
                print("❌ Invalid URL")
        
        elif choice == "0":
            return
        
        else:
            print("❌ Invalid choice")
    
    def view_statistics(self):
        """Option 2: View download statistics"""
        print("\n📊 DOWNLOAD STATISTICS")
        print("-" * 40)
        
        if not self.movies_data:
            print("❌ No movie database loaded")
            return
        
        total_movies = self.movies_data['metadata']['total_movies']
        downloaded = 0
        failed = 0
        not_downloaded = 0
        
        for movie_data in self.movies_data['movies'].values():
            status = movie_data.get('download_status', 'not_downloaded')
            if status == 'downloaded':
                downloaded += 1
            elif status == 'failed':
                failed += 1
            else:
                not_downloaded += 1
        
        print(f"📈 Overall Progress:")
        print(f"   Total movies: {total_movies}")
        print(f"   ✅ Downloaded: {downloaded}")
        print(f"   ❌ Failed: {failed}")
        print(f"   ⏳ Pending: {not_downloaded}")
        print(f"   📊 Completion: {(downloaded / total_movies * 100):.1f}%")
        
        if downloaded > 0:
            print(f"\n📁 Downloaded movies location: downloads/")
            print(f"💾 Database file: {self.json_file}")
        
        if failed > 0:
            print(f"\n⚠️  {failed} downloads failed. You can retry them later.")
    
    def download_movies(self):
        """Option 3: Download movies"""
        print("\n🎬 DOWNLOAD MOVIES")
        print("-" * 40)
        
        if not os.path.exists("goojara_movie_downloader.py"):
            print("❌ Movie downloader script not found!")
            return
        
        print("Choose download option:")
        print("1. Download specific number of movies")
        print("2. Download all pending movies")
        print("3. Download failed movies only")
        print("4. Download movies by year")
        print("5. Download movies by genre")
        print("6. Download movie by name")
        print("0. Back to main menu")
        
        choice = input("\nEnter your choice (1-6, 0): ").strip()
        
        if choice == "1":
            try:
                count = int(input("Enter number of movies to download: "))
                print(f"\n🚀 Starting download of {count} movies...")
                subprocess.run([sys.executable, "goojara_movie_downloader.py", str(count)], check=True)
                print("\n✅ Download completed! Reloading database...")
                self.load_movies_data()
            except ValueError:
                print("❌ Invalid number")
            except subprocess.CalledProcessError as e:
                print(f"❌ Download failed: {e}")
            except KeyboardInterrupt:
                print("\n⚠️  Download interrupted by user")
        
        elif choice == "2":
            print("\n🚀 Starting download of all pending movies...")
            try:
                subprocess.run([sys.executable, "goojara_movie_downloader.py", "all"], check=True)
                print("\n✅ Download completed! Reloading database...")
                self.load_movies_data()
            except subprocess.CalledProcessError as e:
                print(f"❌ Download failed: {e}")
            except KeyboardInterrupt:
                print("\n⚠️  Download interrupted by user")
        
        elif choice == "3":
            print("\n🚀 Starting download of failed movies...")
            try:
                # This would need to be implemented in the downloader
                print("⚠️  Feature not yet implemented. Use option 1 with a large number instead.")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "4":
            year = input("Enter year (e.g., 2024): ").strip()
            if year.isdigit():
                print(f"\n🚀 Starting download of movies from {year}...")
                # This would need to be implemented
                print("⚠️  Feature not yet implemented. Use option 1 with a large number instead.")
            else:
                print("❌ Invalid year")
        
        elif choice == "5":
            print("Available genres: Action, Comedy, Drama, Horror, Sci-Fi, Thriller")
            genre = input("Enter genre: ").strip()
            if genre:
                print(f"\n🚀 Starting download of {genre} movies...")
                # This would need to be implemented
                print("⚠️  Feature not yet implemented. Use option 1 with a large number instead.")
            else:
                print("❌ Invalid genre")
        
        elif choice == "6":
            self.download_movie_by_name()
        
        elif choice == "0":
            return
        
        else:
            print("❌ Invalid choice")
    
    def view_recent_downloads(self):
        """Option 4: View recent downloads"""
        print("\n📋 RECENT DOWNLOADS")
        print("-" * 40)
        
        if not self.movies_data:
            print("❌ No movie database loaded")
            return
        
        downloaded_movies = []
        for movie_data in self.movies_data['movies'].values():
            if movie_data.get('download_status') == 'downloaded':
                downloaded_movies.append(movie_data)
        
        if not downloaded_movies:
            print("❌ No movies downloaded yet")
            return
        
        # Sort by download date (most recent first)
        downloaded_movies.sort(key=lambda x: x.get('download_date', ''), reverse=True)
        
        limit = input("Show last N downloads (default 10): ").strip()
        try:
            limit = int(limit) if limit else 10
        except ValueError:
            limit = 10
        
        print(f"\n📥 Recently Downloaded Movies (last {min(limit, len(downloaded_movies))}):")
        for i, movie in enumerate(downloaded_movies[:limit]):
            date = movie.get('download_date', 'Unknown')
            path = movie.get('download_path', 'Unknown path')
            print(f"   {i+1}. {movie['title']}")
            print(f"      📅 {date}")
            print(f"      📁 {path}")
            print()
    
    def search_movies(self):
        """Option 5: Search movies"""
        print("\n🔍 SEARCH MOVIES")
        print("-" * 40)
        
        if not self.movies_data:
            print("❌ No movie database loaded")
            return
        
        query = input("Enter search term (movie title): ").strip().lower()
        if not query:
            print("❌ No search term entered")
            return
        
        results = []
        for movie_id, movie_data in self.movies_data['movies'].items():
            if query in movie_data['title'].lower():
                results.append(movie_data)
        
        if not results:
            print(f"❌ No movies found matching '{query}'")
            return
        
        print(f"\n🔍 Found {len(results)} movies matching '{query}':")
        for i, movie in enumerate(results[:20]):  # Limit to first 20 results
            status = movie.get('download_status', 'not_downloaded')
            status_icon = "✅" if status == 'downloaded' else "❌" if status == 'failed' else "⏳"
            print(f"   {i+1}. {status_icon} {movie['title']} ({status})")
        
        if len(results) > 20:
            print(f"   ... and {len(results) - 20} more results")
    
    def open_downloads_folder(self):
        """Option 6: Open downloads folder"""
        print("\n📁 OPENING DOWNLOADS FOLDER")
        print("-" * 40)
        
        downloads_path = Path("downloads")
        if not downloads_path.exists():
            print("📁 Creating downloads folder...")
            downloads_path.mkdir(exist_ok=True)
        
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", str(downloads_path)])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["explorer", str(downloads_path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(downloads_path)])
            print(f"✅ Opened downloads folder: {downloads_path.absolute()}")
        except Exception as e:
            print(f"❌ Error opening folder: {e}")
            print(f"📁 Downloads folder location: {downloads_path.absolute()}")
    
    def clear_failed_downloads(self):
        """Option 7: Clear failed downloads"""
        print("\n🗑️  CLEAR FAILED DOWNLOADS")
        print("-" * 40)
        
        if not self.movies_data:
            print("❌ No movie database loaded")
            return
        
        failed_count = 0
        for movie_data in self.movies_data['movies'].values():
            if movie_data.get('download_status') == 'failed':
                failed_count += 1
        
        if failed_count == 0:
            print("✅ No failed downloads to clear")
            return
        
        print(f"⚠️  Found {failed_count} failed downloads")
        confirm = input("Are you sure you want to clear all failed download statuses? (y/N): ").strip().lower()
        
        if confirm == 'y':
            cleared = 0
            for movie_data in self.movies_data['movies'].values():
                if movie_data.get('download_status') == 'failed':
                    movie_data['download_status'] = 'not_downloaded'
                    if 'download_error' in movie_data:
                        del movie_data['download_error']
                    if 'download_date' in movie_data:
                        del movie_data['download_date']
                    cleared += 1
            
            # Update metadata
            if 'downloaded_count' in self.movies_data['metadata']:
                self.movies_data['metadata']['downloaded_count'] = max(0, self.movies_data['metadata']['downloaded_count'] - failed_count)
            
            # Save changes
            try:
                with open(self.json_file, 'w', encoding='utf-8') as f:
                    json.dump(self.movies_data, f, indent=2, ensure_ascii=False)
                print(f"✅ Cleared {cleared} failed download statuses")
            except Exception as e:
                print(f"❌ Error saving changes: {e}")
        else:
            print("❌ Operation cancelled")
    
    def reset_download_status(self):
        """Option 8: Reset all download statuses"""
        print("\n🔄 RESET DOWNLOAD STATUS")
        print("-" * 40)
        
        if not self.movies_data:
            print("❌ No movie database loaded")
            return
        
        downloaded_count = 0
        for movie_data in self.movies_data['movies'].values():
            if movie_data.get('download_status') == 'downloaded':
                downloaded_count += 1
        
        if downloaded_count == 0:
            print("✅ No downloaded movies to reset")
            return
        
        print(f"⚠️  Found {downloaded_count} downloaded movies")
        confirm = input("Are you sure you want to reset ALL download statuses? This will mark all movies as not downloaded! (y/N): ").strip().lower()
        
        if confirm == 'y':
            reset_count = 0
            for movie_data in self.movies_data['movies'].values():
                if movie_data.get('download_status') in ['downloaded', 'failed']:
                    movie_data['download_status'] = 'not_downloaded'
                    # Remove download-related fields
                    for field in ['download_path', 'download_date', 'download_error']:
                        if field in movie_data:
                            del movie_data[field]
                    reset_count += 1
            
            # Reset metadata
            if 'downloaded_count' in self.movies_data['metadata']:
                self.movies_data['metadata']['downloaded_count'] = 0
            
            # Save changes
            try:
                with open(self.json_file, 'w', encoding='utf-8') as f:
                    json.dump(self.movies_data, f, indent=2, ensure_ascii=False)
                print(f"✅ Reset {reset_count} download statuses")
            except Exception as e:
                print(f"❌ Error saving changes: {e}")
        else:
            print("❌ Operation cancelled")
    
    def sync_downloads_folder(self):
        """Option 9: Sync downloads folder with database"""
        print("\n🔍 SYNC DOWNLOADS FOLDER")
        print("-" * 40)
        
        if not self.movies_data:
            print("❌ No movie database loaded")
            return
        
        downloads_path = Path("downloads")
        if not downloads_path.exists():
            print("❌ Downloads folder not found")
            return
        
        print("🔍 Scanning downloads folder...")
        downloaded_files = list(downloads_path.glob("*.mp4")) + list(downloads_path.glob("*.avi")) + list(downloads_path.glob("*.mkv")) + list(downloads_path.glob("*.mov"))
        
        if not downloaded_files:
            print("❌ No video files found in downloads folder")
            return
        
        print(f"📁 Found {len(downloaded_files)} video files in downloads folder")
        
        # Create a mapping of filenames to movie titles
        filename_to_movie = {}
        for movie_data in self.movies_data['movies'].values():
            title = movie_data['title']
            # Create variations of the title for matching
            title_variations = [
                title,
                title.replace(":", " -"),
                title.replace("?", ""),
                title.replace("!", ""),
                title.replace("'", ""),
                title.replace('"', ""),
                title.replace("&", "and"),
                title.replace("  ", " ")
            ]
            
            for variation in title_variations:
                if variation.strip():
                    filename_to_movie[variation.strip()] = movie_data
        
        # Scan each downloaded file and try to match it with movies
        matched_count = 0
        unmatched_files = []
        
        for file_path in downloaded_files:
            filename = file_path.stem  # filename without extension
            print(f"  🔍 Checking: {filename}")
            
            # Try to find a match
            matched = False
            for title_variation, movie_data in filename_to_movie.items():
                if self.filename_matches_title(filename, title_variation):
                    # Update the movie in the database
                    movie_data['download_status'] = 'downloaded'
                    movie_data['download_path'] = str(file_path)
                    movie_data['download_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    print(f"    ✅ Matched: {movie_data['title']}")
                    matched_count += 1
                    matched = True
                    break
            
            if not matched:
                unmatched_files.append(filename)
                print(f"    ❌ No match found")
        
        # Update metadata
        if 'downloaded_count' not in self.movies_data['metadata']:
            self.movies_data['metadata']['downloaded_count'] = 0
        self.movies_data['metadata']['downloaded_count'] = matched_count
        
        # Save changes
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.movies_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Sync completed!")
            print(f"📊 Matched: {matched_count} movies")
            print(f"📁 Unmatched files: {len(unmatched_files)}")
            
            if unmatched_files:
                print(f"\n📋 Unmatched files:")
                for filename in unmatched_files[:10]:  # Show first 10
                    print(f"  - {filename}")
                if len(unmatched_files) > 10:
                    print(f"  ... and {len(unmatched_files) - 10} more")
            
            # Reload data to show updated statistics
            self.load_movies_data()
            
        except Exception as e:
            print(f"❌ Error saving changes: {e}")
    
    def filename_matches_title(self, filename, title):
        """Check if filename matches movie title"""
        # Normalize both strings for comparison
        filename_norm = filename.lower().strip()
        title_norm = title.lower().strip()
        
        # Direct match
        if filename_norm == title_norm:
            return True
        
        # Remove common file suffixes and clean up
        filename_clean = filename_norm
        for suffix in ['(2024)', '(2025)', '(2023)', '(2022)', '(2021)', '(2020)', '(2019)', '(2018)', '(2017)', '(2016)', '(2015)', '(2014)', '(2013)', '(2012)', '(2011)', '(2010)', '(2009)', '(2008)', '(2007)', '(2006)', '(2005)', '(2004)', '(2003)', '(2002)', '(2001)', '(2000)']:
            filename_clean = filename_clean.replace(suffix, '').strip()
        
        # Try matching with cleaned filename
        if filename_clean == title_norm:
            return True
        
        # Try partial matching (filename contains title or vice versa)
        if filename_clean in title_norm or title_norm in filename_clean:
            return True
        
        # Try matching with common variations
        variations = [
            title_norm.replace(":", " -"),
            title_norm.replace("?", ""),
            title_norm.replace("!", ""),
            title_norm.replace("'", ""),
            title_norm.replace('"', ""),
            title_norm.replace("&", "and"),
            title_norm.replace("  ", " ")
        ]
        
        for variation in variations:
            if variation.strip() and (filename_clean == variation.strip() or filename_clean in variation.strip() or variation.strip() in filename_clean):
                return True
        
        return False
    
    def download_movie_by_name(self):
        """Download a specific movie by searching for its name"""
        print("\n🎬 DOWNLOAD MOVIE BY NAME")
        print("-" * 40)
        
        if not self.movies_data:
            print("❌ No movie database loaded")
            return
        
        if not os.path.exists("goojara_movie_downloader.py"):
            print("❌ Movie downloader script not found!")
            return
        
        # Get search term from user
        search_term = input("Enter movie name to search for: ").strip().lower()
        if not search_term:
            print("❌ No search term entered")
            return
        
        # Search for matching movies
        matching_movies = []
        for movie_id, movie_data in self.movies_data['movies'].items():
            if search_term in movie_data['title'].lower():
                matching_movies.append((movie_id, movie_data))
        
        if not matching_movies:
            print(f"❌ No movies found matching '{search_term}'")
            print("\n💡 Tip: Your movie list might be outdated.")
            update_choice = input("Would you like to update the movie list? (y/N): ").strip().lower()
            if update_choice == 'y':
                print("\n🔄 Updating movie list...")
                self.scrape_movies()
                print("\n🔄 Reloading database...")
                self.load_movies_data()
                print("✅ Movie list updated! Try searching again.")
            return
        
        # Show search results
        print(f"\n🔍 Found {len(matching_movies)} movies matching '{search_term}':")
        for i, (movie_id, movie_data) in enumerate(matching_movies):
            status = movie_data.get('download_status', 'not_downloaded')
            status_icon = "✅" if status == 'downloaded' else "❌" if status == 'failed' else "⏳"
            print(f"  {i+1}. {status_icon} {movie_data['title']} ({status})")
        
        if len(matching_movies) > 10:
            print(f"  ... and {len(matching_movies) - 10} more results")
        
        # Let user select which movie to download
        if len(matching_movies) == 1:
            # Only one result, ask for confirmation
            movie_id, movie_data = matching_movies[0]
            confirm = input(f"\nDownload '{movie_data['title']}'? (y/N): ").strip().lower()
            if confirm == 'y':
                self.download_single_movie(movie_id, movie_data)
            else:
                print("❌ Download cancelled")
        else:
            # Multiple results, let user choose
            try:
                choice = int(input(f"\nSelect movie to download (1-{len(matching_movies)}): ").strip())
                if 1 <= choice <= len(matching_movies):
                    movie_id, movie_data = matching_movies[choice - 1]
                    self.download_single_movie(movie_id, movie_data)
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Invalid selection")
    
    def download_single_movie(self, movie_id, movie_data):
        """Download a single movie by ID"""
        title = movie_data['title']
        link = movie_data['link']
        
        print(f"\n🎬 Downloading: {title}")
        print(f"🔗 Link: {link}")
        
        # Check if already downloaded
        if movie_data.get('download_status') == 'downloaded':
            print(f"⚠️  '{title}' is already downloaded!")
            overwrite = input("Download again? (y/N): ").strip().lower()
            if overwrite != 'y':
                print("❌ Download cancelled")
                return
        
        # Check if previously failed
        if movie_data.get('download_status') == 'failed':
            print(f"⚠️  '{title}' previously failed to download")
            retry = input("Retry download? (y/N): ").strip().lower()
            if retry != 'y':
                print("❌ Download cancelled")
                return
        
        try:
            # Use the selenium downloader directly
            from goojara_selenium_auto_downloader import GoojaraSeleniumAutoDownloader
            
            print("🌐 Initializing Selenium downloader...")
            downloader = GoojaraSeleniumAutoDownloader(headless=True)
            
            # Create safe filename
            safe_filename = self.sanitize_filename(title)
            print(f"📁 Filename: {safe_filename}")
            
            # Download the movie
            success = downloader.download_movie(link, "downloads", safe_filename)
            
            if success:
                # Update the movie in the database
                movie_data['download_status'] = 'downloaded'
                movie_data['download_path'] = f"downloads/{safe_filename}.mp4"
                movie_data['download_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                
                # Update metadata
                if 'downloaded_count' not in self.movies_data['metadata']:
                    self.movies_data['metadata']['downloaded_count'] = 0
                self.movies_data['metadata']['downloaded_count'] += 1
                
                # Save changes
                try:
                    with open(self.json_file, 'w', encoding='utf-8') as f:
                        json.dump(self.movies_data, f, indent=2, ensure_ascii=False)
                    print(f"✅ Successfully downloaded: {title}")
                    print(f"📁 File: downloads/{safe_filename}.mp4")
                    print("💾 Database updated")
                except Exception as e:
                    print(f"❌ Error updating database: {e}")
            else:
                # Mark as failed
                movie_data['download_status'] = 'failed'
                movie_data['download_error'] = "Download failed - no video sources found"
                movie_data['download_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                
                # Save changes
                try:
                    with open(self.json_file, 'w', encoding='utf-8') as f:
                        json.dump(self.movies_data, f, indent=2, ensure_ascii=False)
                    print(f"❌ Failed to download: {title}")
                except Exception as e:
                    print(f"❌ Error updating database: {e}")
            
            # Cleanup
            downloader.close()
            
        except Exception as e:
            print(f"❌ Error downloading {title}: {e}")
            # Mark as failed
            movie_data['download_status'] = 'failed'
            movie_data['download_error'] = str(e)
            movie_data['download_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Save changes
            try:
                with open(self.json_file, 'w', encoding='utf-8') as f:
                    json.dump(self.movies_data, f, indent=2, ensure_ascii=False)
            except Exception as save_error:
                print(f"❌ Error updating database: {save_error}")
    
    def fix_database_inconsistencies(self):
        """Option 10: Fix database inconsistencies"""
        print("\n🔧 FIX DATABASE INCONSISTENCIES")
        print("-" * 40)
        
        if not self.movies_data:
            print("❌ No movie database loaded")
            return
        
        print("🔍 Analyzing database for inconsistencies...")
        
        # Check for duplicate movie titles
        title_count = {}
        duplicates = []
        
        for movie_id, movie_data in self.movies_data['movies'].items():
            title = movie_data.get('title', '').strip()
            if title:
                if title in title_count:
                    title_count[title].append(movie_id)
                    duplicates.append(title)
                else:
                    title_count[title] = [movie_id]
        
        # Check for movies with missing required fields
        missing_fields = []
        for movie_id, movie_data in self.movies_data['movies'].items():
            if not movie_data.get('title') or not movie_data.get('link'):
                missing_fields.append(movie_id)
        
        # Check for inconsistent download statuses
        inconsistent_statuses = []
        for movie_id, movie_data in self.movies_data['movies'].items():
            status = movie_data.get('download_status', 'not_downloaded')
            download_path = movie_data.get('download_path', '')
            
            if status == 'downloaded' and not download_path:
                inconsistent_statuses.append((movie_id, 'downloaded_without_path'))
            elif status == 'downloaded' and download_path and not os.path.exists(download_path):
                inconsistent_statuses.append((movie_id, 'downloaded_file_missing'))
        
        # Report findings
        print(f"📊 Database Analysis Results:")
        print(f"   Total movies: {len(self.movies_data['movies'])}")
        print(f"   Duplicate titles: {len(duplicates)}")
        print(f"   Missing required fields: {len(missing_fields)}")
        print(f"   Inconsistent statuses: {len(inconsistent_statuses)}")
        
        if not duplicates and not missing_fields and not inconsistent_statuses:
            print("\n✅ Database is clean! No inconsistencies found.")
            return
        
        # Show details
        if duplicates:
            print(f"\n⚠️  Duplicate titles found:")
            for title in set(duplicates):
                movie_ids = title_count[title]
                print(f"   '{title}' appears {len(movie_ids)} times (IDs: {', '.join(movie_ids)})")
        
        if missing_fields:
            print(f"\n⚠️  Movies with missing required fields:")
            for movie_id in missing_fields:
                movie_data = self.movies_data['movies'][movie_id]
                print(f"   ID {movie_id}: {movie_data.get('title', 'NO_TITLE')} - Missing: {[k for k, v in movie_data.items() if not v]}")
        
        if inconsistent_statuses:
            print(f"\n⚠️  Inconsistent download statuses:")
            for movie_id, issue_type in inconsistent_statuses:
                movie_data = self.movies_data['movies'][movie_id]
                if issue_type == 'downloaded_without_path':
                    print(f"   ID {movie_id}: {movie_data.get('title', 'NO_TITLE')} - Downloaded but no path recorded")
                elif issue_type == 'downloaded_file_missing':
                    print(f"   ID {movie_id}: {movie_data.get('title', 'NO_TITLE')} - Downloaded but file missing: {movie_data.get('download_path')}")
        
        # Ask if user wants to fix
        if duplicates or missing_fields or inconsistent_statuses:
            print(f"\n🔧 Would you like to fix these inconsistencies?")
            print("   This will:")
            if duplicates:
                print("   - Remove duplicate movie entries (keep the first one)")
            if missing_fields:
                print("   - Remove movies with missing required fields")
            if inconsistent_statuses:
                print("   - Fix inconsistent download statuses")
            
            choice = input("\nFix inconsistencies? (y/N): ").strip().lower()
            
            if choice == 'y':
                print("\n🔧 Fixing inconsistencies...")
                
                # Fix duplicates (keep first occurrence, remove others)
                if duplicates:
                    print("   Removing duplicate entries...")
                    for title in set(duplicates):
                        movie_ids = title_count[title]
                        # Keep the first one, remove the rest
                        for movie_id in movie_ids[1:]:
                            if movie_id in self.movies_data['movies']:
                                del self.movies_data['movies'][movie_id]
                                print(f"     Removed duplicate: {title} (ID: {movie_id})")
                
                # Fix missing fields
                if missing_fields:
                    print("   Removing movies with missing fields...")
                    for movie_id in missing_fields:
                        if movie_id in self.movies_data['movies']:
                            title = self.movies_data['movies'][movie_id].get('title', 'NO_TITLE')
                            del self.movies_data['movies'][movie_id]
                            print(f"     Removed incomplete entry: {title} (ID: {movie_id})")
                
                # Fix inconsistent statuses
                if inconsistent_statuses:
                    print("   Fixing inconsistent statuses...")
                    for movie_id, issue_type in inconsistent_statuses:
                        if movie_id in self.movies_data['movies']:
                            if issue_type == 'downloaded_without_path':
                                self.movies_data['movies'][movie_id]['download_status'] = 'not_downloaded'
                                self.movies_data['movies'][movie_id]['download_path'] = ''
                                print(f"     Fixed: {self.movies_data['movies'][movie_id].get('title')} - Reset to not downloaded")
                            elif issue_type == 'downloaded_file_missing':
                                self.movies_data['movies'][movie_id]['download_status'] = 'not_downloaded'
                                self.movies_data['movies'][movie_id]['download_path'] = ''
                                print(f"     Fixed: {self.movies_data['movies'][movie_id].get('title')} - Reset to not downloaded")
                
                # Update metadata
                self.movies_data['metadata']['total_movies'] = len(self.movies_data['movies'])
                
                # Save changes
                try:
                    with open(self.json_file, 'w', encoding='utf-8') as f:
                        json.dump(self.movies_data, f, indent=2, ensure_ascii=False)
                    print("\n✅ Database inconsistencies fixed and saved!")
                    print("💾 Reloading database...")
                    self.load_movies_data()
                except Exception as e:
                    print(f"❌ Error saving fixed database: {e}")
            else:
                print("\n⏭️  Skipping fixes. Database remains unchanged.")
    
    def show_help(self):
        """Option 11: Show help"""
        print("\n📖 HELP & USAGE")
        print("-" * 40)
        print("🎬 GOOJARA MASTER - Complete Movie Management System")
        print()
        print("📥 SCRAPING:")
        print("   - Scrape all movies from goojara.to")
        print("   - Updates your movie database")
        print("   - Run this first to build your movie list")
        print()
        print("🎬 DOWNLOADING:")
        print("   - Download movies using your selenium technique")
        print("   - Movies are saved with title filenames")
        print("   - Progress is tracked and saved")
        print("   - Failed downloads can be retried")
        print("   - Download specific movies by searching name")
        print()
        print("📊 TRACKING:")
        print("   - View download statistics")
        print("   - See recent downloads")
        print("   - Search through your movie collection")
        print()
        print("🔧 MANAGEMENT:")
        print("   - Clear failed download statuses")
        print("   - Reset all download progress")
        print("   - Sync downloads folder with database")
        print("   - Open downloads folder")
        print("   - Fix database inconsistencies")
        print()
        print("💡 TIPS:")
        print("   - Start with scraping to build your database")
        print("   - Download in small batches (5-10 movies)")
        print("   - Check statistics regularly")
        print("   - Use search to find specific movies")
        print("   - Use sync function to update existing downloads")
        print("   - Use database fixer to resolve inconsistencies")
    
    def run(self):
        """Main program loop"""
        print("🎬 Welcome to GOOJARA MASTER!")
        print("Your complete movie collection management system")
        
        while True:
            try:
                self.show_main_menu()
                choice = input("\nEnter your choice (0-9): ").strip()
                
                if choice == "1":
                    self.scrape_movies()
                elif choice == "2":
                    self.view_statistics()
                elif choice == "3":
                    self.download_movies()
                elif choice == "4":
                    self.view_recent_downloads()
                elif choice == "5":
                    self.search_movies()
                elif choice == "6":
                    self.open_downloads_folder()
                elif choice == "7":
                    self.clear_failed_downloads()
                elif choice == "8":
                    self.reset_download_status()
                elif choice == "9":
                    self.sync_downloads_folder()
                elif choice == "10":
                    self.fix_database_inconsistencies()
                elif choice == "11":
                    self.show_help()
                elif choice == "0":
                    print("\n👋 Goodbye! Happy movie collecting!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 0-11.")
                
                if choice != "0":
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Program interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("Press Enter to continue...")

def main():
    """Main function"""
    try:
        master = GoojaraMaster()
        master.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
