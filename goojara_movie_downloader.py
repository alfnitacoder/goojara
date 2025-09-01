#!/usr/bin/env python3
"""
Goojara Movie Downloader
Downloads movies from the scraped list and updates JSON with download status
"""

import json
import os
import sys
import time
import re
from pathlib import Path
from goojara_selenium_auto_downloader import GoojaraSeleniumAutoDownloader

class GoojaraMovieDownloader:
    def __init__(self, json_file="goojara_movies_temp.json"):
        self.json_file = json_file
        self.movies_data = {}
        self.downloader = None  # Will initialize when needed
        self.download_dir = "downloads"
        self.load_movies_data()
        
    def load_movies_data(self):
        """Load the scraped movies data from JSON"""
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.movies_data = json.load(f)
                print(f"✅ Loaded {self.movies_data['metadata']['total_movies']} movies from {self.json_file}")
            else:
                print(f"❌ JSON file {self.json_file} not found!")
                print("Please run the movie scraper first: python goojara_movie_scraper.py")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading JSON file: {e}")
            sys.exit(1)
    
    def save_movies_data(self):
        """Save the updated movies data back to JSON"""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.movies_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Updated movie data saved to {self.json_file}")
        except Exception as e:
            print(f"❌ Error saving JSON file: {e}")
    
    def sanitize_filename(self, title):
        """Convert movie title to a safe filename"""
        # Remove or replace invalid filename characters
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        # Replace multiple spaces with single space
        filename = re.sub(r'\s+', ' ', filename)
        # Remove leading/trailing spaces
        filename = filename.strip()
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        return filename
    
    def get_download_status(self, movie_id):
        """Get download status for a movie"""
        if 'download_status' not in self.movies_data['movies'][movie_id]:
            return 'not_downloaded'
        return self.movies_data['movies'][movie_id]['download_status']
    
    def mark_as_downloaded(self, movie_id, file_path):
        """Mark a movie as downloaded in the JSON"""
        if movie_id in self.movies_data['movies']:
            self.movies_data['movies'][movie_id]['download_status'] = 'downloaded'
            self.movies_data['movies'][movie_id]['download_path'] = file_path
            self.movies_data['movies'][movie_id]['download_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            self.movies_data['metadata']['downloaded_count'] = self.movies_data['metadata'].get('downloaded_count', 0) + 1
    
    def mark_as_failed(self, movie_id, error_msg):
        """Mark a movie as failed in the JSON"""
        if movie_id in self.movies_data['movies']:
            self.movies_data['movies'][movie_id]['download_status'] = 'failed'
            self.movies_data['movies'][movie_id]['download_error'] = error_msg
            self.movies_data['movies'][movie_id]['download_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_movies_to_download(self, count=None, status='not_downloaded'):
        """Get list of movies to download"""
        movies_to_download = []
        
        for movie_id, movie_data in self.movies_data['movies'].items():
            if self.get_download_status(movie_id) == status:
                movies_to_download.append((movie_id, movie_data))
                if count and len(movies_to_download) >= count:
                    break
        
        return movies_to_download
    
    def download_movie(self, movie_id, movie_data):
        """Download a single movie"""
        title = movie_data['title']
        link = movie_data['link']
        
        print(f"\n🎬 Downloading: {title}")
        print(f"🔗 Link: {link}")
        
        # Create safe filename
        safe_filename = self.sanitize_filename(title)
        print(f"📁 Filename: {safe_filename}")
        
        try:
            # Initialize selenium downloader if not already done
            if self.downloader is None:
                print("🌐 Initializing Selenium downloader...")
                self.downloader = GoojaraSeleniumAutoDownloader(headless=True)
            
            # Use the selenium downloader with custom filename
            success = self.downloader.download_movie(link, self.download_dir, safe_filename)
            
            if success:
                # Find the downloaded file
                downloaded_files = list(Path(self.download_dir).glob(f"*{safe_filename}*"))
                if downloaded_files:
                    file_path = str(downloaded_files[0])
                    self.mark_as_downloaded(movie_id, file_path)
                    print(f"✅ Successfully downloaded: {title}")
                    print(f"📁 File: {file_path}")
                    return True
                else:
                    # If no exact match, mark as downloaded anyway
                    self.mark_as_downloaded(movie_id, "unknown_path")
                    print(f"✅ Successfully downloaded: {title}")
                    return True
            else:
                error_msg = "Download failed - no video sources found"
                self.mark_as_failed(movie_id, error_msg)
                print(f"❌ Failed to download: {title}")
                return False
                
        except Exception as e:
            error_msg = str(e)
            self.mark_as_failed(movie_id, error_msg)
            print(f"❌ Error downloading {title}: {error_msg}")
            return False
    
    def download_movies(self, count=None, status='not_downloaded'):
        """Download multiple movies"""
        movies_to_download = self.get_movies_to_download(count, status)
        
        if not movies_to_download:
            print(f"🎉 No movies to download with status: {status}")
            return
        
        print(f"🚀 Starting download of {len(movies_to_download)} movies...")
        print("=" * 60)
        
        successful_downloads = 0
        failed_downloads = 0
        
        for i, (movie_id, movie_data) in enumerate(movies_to_download, 1):
            print(f"\n📥 Progress: {i}/{len(movies_to_download)}")
            
            if self.download_movie(movie_id, movie_data):
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # Save progress after each download
            self.save_movies_data()
            
            # Small delay between downloads
            if i < len(movies_to_download):
                time.sleep(2)
        
        print("\n" + "=" * 60)
        print(f"🎉 Download session completed!")
        print(f"✅ Successful: {successful_downloads}")
        print(f"❌ Failed: {failed_downloads}")
        print(f"📊 Total movies in database: {self.movies_data['metadata']['total_movies']}")
        print(f"📥 Downloaded so far: {self.movies_data['metadata'].get('downloaded_count', 0)}")
    
    def show_download_stats(self):
        """Show current download statistics"""
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
        
        print(f"\n📊 Download Statistics:")
        print(f"   Total movies: {total_movies}")
        print(f"   ✅ Downloaded: {downloaded}")
        print(f"   ❌ Failed: {failed}")
        print(f"   ⏳ Pending: {not_downloaded}")
        print(f"   📈 Progress: {(downloaded / total_movies * 100):.1f}%")
    
    def list_recent_downloads(self, limit=10):
        """List recently downloaded movies"""
        downloaded_movies = []
        
        for movie_id, movie_data in self.movies_data['movies'].items():
            if movie_data.get('download_status') == 'downloaded':
                downloaded_movies.append(movie_data)
        
        # Sort by download date (most recent first)
        downloaded_movies.sort(key=lambda x: x.get('download_date', ''), reverse=True)
        
        print(f"\n📥 Recently Downloaded Movies (last {min(limit, len(downloaded_movies))}):")
        for i, movie in enumerate(downloaded_movies[:limit]):
            date = movie.get('download_date', 'Unknown')
            path = movie.get('download_path', 'Unknown path')
            print(f"   {i+1}. {movie['title']}")
            print(f"      📅 {date}")
            print(f"      📁 {path}")
            print()
    
    def cleanup(self):
        """Clean up selenium driver"""
        if self.downloader:
            try:
                self.downloader.close()
                print("🌐 Selenium driver closed")
            except:
                pass

def main():
    """Main function"""
    print("🎬 Goojara Movie Downloader")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python goojara_movie_downloader.py <count>")
        print("  python goojara_movie_downloader.py all")
        print("  python goojara_movie_downloader.py stats")
        print("  python goojara_movie_downloader.py recent")
        print("\nExamples:")
        print("  python goojara_movie_downloader.py 3     # Download 3 movies")
        print("  python goojara_movie_downloader.py all   # Download all pending movies")
        print("  python goojara_movie_downloader.py stats # Show download statistics")
        print("  python goojara_movie_downloader.py recent # Show recent downloads")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Initialize downloader
    downloader = GoojaraMovieDownloader()
    
    if command == "stats":
        downloader.show_download_stats()
    elif command == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        downloader.list_recent_downloads(limit)
    elif command == "all":
        print("🚀 Downloading all pending movies...")
        downloader.download_movies()
    elif command.isdigit():
        count = int(command)
        print(f"🚀 Downloading {count} movies...")
        downloader.download_movies(count)
    else:
        print(f"❌ Invalid command: {command}")
        print("Use: <number>, 'all', 'stats', or 'recent'")
        sys.exit(1)
    
    # Show final stats
    downloader.show_download_stats()
    
    # Cleanup
    downloader.cleanup()

if __name__ == "__main__":
    main()
