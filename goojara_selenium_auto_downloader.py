#!/usr/bin/env python3
"""
Goojara Selenium Auto Downloader
Uses Selenium to automatically find and download video URLs
"""

import time
import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests

class GoojaraSeleniumAutoDownloader:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with anti-detection options"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Anti-detection options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Window size
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Use the original working approach - no Service specification
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute anti-detection script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver setup complete")
            
        except Exception as e:
            print(f"❌ Error setting up Chrome driver: {e}")
            print("💡 Make sure Chrome and ChromeDriver are installed")
            sys.exit(1)
    
    def navigate_to_movie_page(self, movie_url):
        """Navigate to the movie page and wait for video to load"""
        try:
            print(f"🌐 Navigating to: {movie_url}")
            self.driver.get(movie_url)
            
            # Wait for page to load and JavaScript to execute
            print("⏳ Waiting for page to load and JavaScript to execute...")
            time.sleep(5)
            
            # Wait for video player to appear
            print("⏳ Waiting for video player to load...")
            
            # Try multiple approaches to find the video player
            video_element = None
            
            # Method 1: Look for video tag (might appear after JavaScript loads)
            try:
                video_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
                print("✅ Video player found (video tag)")
            except TimeoutException:
                print("⚠️  Video tag not found, trying other methods...")
            
            # Method 2: Look for iframe with video (created by JavaScript)
            if not video_element:
                try:
                    # Continuously monitor for iframe to be created by JavaScript
                    print("⏳ Continuously monitoring for iframe to be created by JavaScript...")
                    max_wait_time = 30  # Maximum wait time in seconds
                    start_time = time.time()
                    
                    while time.time() - start_time < max_wait_time and not video_element:
                        iframe_elements = self.driver.find_elements(By.TAG_NAME, "iframe")
                        print(f"    🔍 Check {int(time.time() - start_time)}s: Found {len(iframe_elements)} iframe elements")
                        
                        if iframe_elements:
                            for i, iframe in enumerate(iframe_elements):
                                src = iframe.get_attribute("src")
                                print(f"        🔍 Iframe {i+1}: src='{src}'")
                                
                                if src and ("player" in src.lower() or "video" in src.lower() or "embed" in src.lower()):
                                    print(f"        ✅ Found video iframe: {src}")
                                    video_element = iframe
                                    break
                                
                                # Try to switch to iframe and look for video elements inside
                                try:
                                    print(f"        🔍 Switching to iframe {i+1} to look for video...")
                                    self.driver.switch_to.frame(iframe)
                                    
                                    # Wait a bit for iframe content to load
                                    time.sleep(3)
                                    
                                    # Debug: See what's actually in the iframe
                                    print(f"        🔍 Iframe {i+1} page title: {self.driver.title}")
                                    print(f"        🔍 Iframe {i+1} current URL: {self.driver.current_url}")
                                    
                                    # Look for any elements to understand the structure
                                    all_elements = self.driver.find_elements(By.XPATH, "//*")
                                    print(f"        🔍 Iframe {i+1} contains {len(all_elements)} total elements")
                                    
                                    # Debug: List all elements to understand structure
                                    print(f"        🔍 Listing all elements in iframe {i+1}:")
                                    for j, element in enumerate(all_elements[:10]):  # Show first 10 elements
                                        tag = element.tag_name
                                        class_attr = element.get_attribute("class") or ""
                                        id_attr = element.get_attribute("id") or ""
                                        text = element.text[:50] if element.text else ""
                                        print(f"            {j+1}. <{tag}> class='{class_attr}' id='{id_attr}' text='{text}'")
                                    
                                    if len(all_elements) > 10:
                                        print(f"            ... and {len(all_elements) - 10} more elements")
                                    
                                    # Look for video elements inside the iframe
                                    iframe_videos = self.driver.find_elements(By.TAG_NAME, "video")
                                    if iframe_videos:
                                        print(f"        ✅ Found {len(iframe_videos)} video elements inside iframe {i+1}")
                                        video_element = iframe_videos[0]
                                        break
                                    
                                    # If no video found, try to trigger video element creation by interacting with the video container
                                    if not iframe_videos:
                                        print(f"        🔍 No video element found, trying to trigger video creation...")
                                        
                                        # Try clicking on the video container
                                        try:
                                            video_container = self.driver.find_element(By.ID, "video-container")
                                            print(f"        🔍 Found video container, clicking to trigger video...")
                                            video_container.click()
                                            time.sleep(2)
                                        except:
                                            print(f"        ⚠️  Could not find video container")
                                        
                                        # Try clicking on the video holder
                                        try:
                                            video_holder = self.driver.find_element(By.CLASS_NAME, "vid-holder")
                                            print(f"        🔍 Found video holder, clicking to trigger video...")
                                            video_holder.click()
                                            time.sleep(2)
                                        except:
                                            print(f"        ⚠️  Could not find video holder")
                                        
                                        # Try clicking on the play holder
                                        try:
                                            play_holder = self.driver.find_element(By.CLASS_NAME, "playh")
                                            print(f"        🔍 Found play holder, clicking to trigger video...")
                                            play_holder.click()
                                            time.sleep(2)
                                        except:
                                            print(f"        ⚠️  Could not find play holder")
                                        
                                        # Look for video elements again after interactions
                                        print(f"        🔍 Checking for video elements after interactions...")
                                        iframe_videos = self.driver.find_elements(By.TAG_NAME, "video")
                                        if iframe_videos:
                                            print(f"        ✅ Found {len(iframe_videos)} video elements after interactions!")
                                            video_element = iframe_videos[0]
                                            break
                                    
                                    # If no video found immediately, wait and try again
                                    if not iframe_videos:
                                        print(f"        ⏳ No video found immediately, waiting for iframe content to load...")
                                        time.sleep(5)
                                        
                                        # Try again after waiting
                                        iframe_videos = self.driver.find_elements(By.TAG_NAME, "video")
                                        if iframe_videos:
                                            print(f"        ✅ Found {len(iframe_videos)} video elements after waiting")
                                            video_element = iframe_videos[0]
                                            break
                                    
                                    # Look for video containers inside the iframe
                                    iframe_containers = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'video') or contains(@class, 'player')]")
                                    if iframe_containers:
                                        print(f"        ✅ Found {len(iframe_containers)} video containers inside iframe {i+1}")
                                        for container in iframe_containers:
                                            nested_videos = container.find_elements(By.TAG_NAME, "video")
                                            if nested_videos:
                                                video_element = nested_videos[0]
                                                print(f"        ✅ Found nested video in iframe container")
                                                break
                                    
                                    # Switch back to main content
                                    self.driver.switch_to.default_content()
                                    
                                except Exception as e:
                                    print(f"        ⚠️  Error checking iframe {i+1}: {e}")
                                    # Make sure we're back to main content
                                    try:
                                        self.driver.switch_to.default_content()
                                    except:
                                        pass
                                
                                if video_element:
                                    break
                        
                        if not video_element:
                            print(f"    ⏳ No video found yet, waiting 3 seconds...")
                            time.sleep(3)
                    
                    if video_element:
                        print(f"    ✅ Video element found after {int(time.time() - start_time)} seconds")
                    else:
                        print(f"    ⚠️  No video element found after {max_wait_time} seconds of monitoring")
                            
                except Exception as e:
                    print(f"    ⚠️  Error checking iframes: {e}")
            
            # Method 3: Look for video container divs
            if not video_element:
                try:
                    video_containers = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'video') or contains(@class, 'player') or contains(@id, 'video') or contains(@id, 'player')]")
                    print(f"🔍 Found {len(video_containers)} video container elements")
                    for container in video_containers:
                        print(f"    🔍 Container: class='{container.get_attribute('class')}', id='{container.get_attribute('id')}'")
                        # Look for video elements inside containers
                        nested_videos = container.find_elements(By.TAG_NAME, "video")
                        if nested_videos:
                            video_element = nested_videos[0]
                            print(f"    ✅ Found nested video in container")
                            break
                except Exception as e:
                    print(f"    ⚠️  Error checking video containers: {e}")
            
            # Method 4: Look for any clickable elements that might be the video player
            if not video_element:
                try:
                    clickable_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'video') or contains(@class, 'player') or contains(@class, 'embed')]")
                    print(f"🔍 Found {len(clickable_elements)} potential video elements")
                    for element in clickable_elements:
                        print(f"    🔍 Element: {element.tag_name}, class='{element.get_attribute('class')}', id='{element.get_attribute('id')}'")
                except Exception as e:
                    print(f"    ⚠️  Error checking potential video elements: {e}")
            
            if video_element:
                print("✅ Video player found, attempting to play...")
                
                # Try to play the video to trigger video source loading
                print("▶️  Attempting to play video...")
                try:
                    # Click on video to start playing
                    video_element.click()
                    print("✅ Video clicked to start playing")
                    
                    # Try to force autoplay using JavaScript
                    try:
                        print("🔧 Attempting to force autoplay with JavaScript...")
                        self.driver.execute_script("arguments[0].play();", video_element)
                        print("✅ JavaScript autoplay executed")
                    except Exception as e:
                        print(f"⚠️  JavaScript autoplay failed: {e}")
                    
                    # Wait a bit for any popups
                    time.sleep(2)
                    
                    # Handle advertisement popups by closing them
                    print("🔍 Looking for advertisement popups...")
                    self.handle_popups()
                    
                    # After handling popups, we need to re-find the video element since we might have lost the iframe context
                    print("🔄 Re-finding video element after popup handling...")
                    try:
                        # Switch back to main content first
                        self.driver.switch_to.default_content()
                        
                        # Find the iframe again
                        iframe_elements = self.driver.find_elements(By.TAG_NAME, "iframe")
                        if iframe_elements:
                            iframe = iframe_elements[0]  # Use the first iframe
                            self.driver.switch_to.frame(iframe)
                            
                            # Look for video elements again
                            iframe_videos = self.driver.find_elements(By.TAG_NAME, "video")
                            if iframe_videos:
                                video_element = iframe_videos[0]
                                print("✅ Video element re-found after popup handling")
                            else:
                                print("⚠️  Video element not found after popup handling")
                        else:
                            print("⚠️  Iframe not found after popup handling")
                    except Exception as e:
                        print(f"⚠️  Error re-finding video element: {e}")
                    
                    # Try to play again after closing popups
                    if video_element:
                        print("🔄 Trying to play video again...")
                        try:
                            video_element.click()
                            
                            # Force autoplay again
                            try:
                                self.driver.execute_script("arguments[0].play();", video_element)
                                print("✅ Video clicked and autoplay executed again")
                            except Exception as e:
                                print(f"⚠️  Second autoplay attempt failed: {e}")
                        except Exception as e:
                            print(f"⚠️  Could not click video after popup handling: {e}")
                    else:
                        print("⚠️  Cannot play video - video element not available after popup handling")
                    
                    # Wait for video to start loading and check play state
                    time.sleep(3)
                    
                    # Check if video is actually playing
                    try:
                        is_playing = self.driver.execute_script("return !arguments[0].paused;", video_element)
                        if is_playing:
                            print("✅ Video is now playing!")
                        else:
                            print("⚠️  Video is not playing, trying one more time...")
                            # One more attempt
                            video_element.click()
                            self.driver.execute_script("arguments[0].play();", video_element)
                            time.sleep(2)
                    except Exception as e:
                        print(f"⚠️  Could not check play state: {e}")
                    
                    # Check if video has a src attribute
                    if video_element.tag_name == "video":
                        src = video_element.get_attribute("src")
                        if src:
                            print(f"✅ Video source found: {src}")
                        else:
                            print("⚠️  Video source not yet loaded, waiting...")
                            time.sleep(5)
                    else:
                        print("⚠️  Video element is not a video tag, checking page source...")
                        
                except Exception as e:
                    print(f"⚠️  Could not click video: {e}")
            else:
                print("⚠️  No video player found, but continuing...")
            
            # Wait a bit more for JavaScript to fully execute and video to load
            print("⏳ Waiting for video source to fully load...")
            time.sleep(8)
            
            return True
            
        except Exception as e:
            print(f"❌ Error navigating to page: {e}")
            return False
    
    def handle_popups(self):
        """Handle advertisement popups by closing them"""
        try:
            # Look for common popup close buttons
            popup_selectors = [
                "//button[contains(@class, 'close')]",
                "//button[contains(@class, 'popup')]",
                "//button[contains(@class, 'ad')]",
                "//div[contains(@class, 'close')]//button",
                "//div[contains(@class, 'popup')]//button",
                "//span[contains(@class, 'close')]",
                "//a[contains(@class, 'close')]",
                "//*[contains(text(), '×')]",
                "//*[contains(text(), 'X')]",
                "//*[contains(text(), 'Close')]",
                "//*[contains(text(), 'close')]"
            ]
            
            for selector in popup_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            print(f"    🔍 Found popup close button: {element.text or element.get_attribute('class')}")
                            try:
                                element.click()
                                print(f"    ✅ Closed popup: {element.text or element.get_attribute('class')}")
                                time.sleep(1)
                            except:
                                pass
                except:
                    continue
            
            # Also try to close any new tabs/windows that might have opened
            current_window = self.driver.current_window_handle
            all_windows = self.driver.window_handles
            
            if len(all_windows) > 1:
                print(f"    🔍 Found {len(all_windows)} windows, closing popup windows...")
                for window in all_windows:
                    if window != current_window:
                        try:
                            self.driver.switch_to.window(window)
                            print(f"    ✅ Closing popup window: {self.driver.title}")
                            self.driver.close()
                        except:
                            pass
                
                # Switch back to main window
                self.driver.switch_to.window(current_window)
                print("    ✅ Switched back to main window")
            
        except Exception as e:
            print(f"    ⚠️  Error handling popups: {e}")
    
    def find_video_sources(self):
        """Find video sources from the rendered HTML"""
        print("🔍 Looking for video sources in rendered HTML...")
        
        video_sources = []
        
        try:
            # Method 1: Look for video tags with src attributes (PRIORITY)
            print("  📹 Method 1: Looking for video tags with src...")
            video_elements = self.driver.find_elements(By.TAG_NAME, "video")
            
            for video in video_elements:
                src = video.get_attribute("src")
                if src:
                    # Clean up HTML entities
                    src = src.replace('&amp;', '&')
                    print(f"    ✅ Found video tag with src: {src}")
                    
                    if 'wootly.ch' in src and 'source' in src:
                        video_sources.append(('wootly_video_tag', src))
                    elif 'nebula.to' in src:
                        video_sources.append(('nebula_video_tag', src))
                    else:
                        video_sources.append(('video_tag', src))
            
            # Method 2: Look for wootly.ch URLs in page source (filter for actual video sources)
            print("  🌐 Method 2: Looking for wootly.ch video sources...")
            page_source = self.driver.page_source
            wootly_pattern = r'https?://[^"\'\s]*wootly\.ch[^"\'\s]*'
            wootly_urls = re.findall(wootly_pattern, page_source)
            
            for url in wootly_urls:
                url = url.replace('&amp;', '&')
                # Look for actual video sources, not JavaScript files
                if ('source' in url or 'video' in url) and not url.endswith('.js') and 'netmin.js' not in url:
                    if url not in [src[1] for src in video_sources]:
                        video_sources.append(('wootly_video_source', url))
                        print(f"    ✅ Found wootly.ch video source: {url}")
            
            # Method 3: Look for nebula.to URLs
            print("  🌟 Method 3: Looking for nebula.to URLs...")
            nebula_pattern = r'https?://[^"\'\s]*nebula\.to[^"\'\s]*\.mp4[^"\'\s]*'
            nebula_urls = re.findall(nebula_pattern, page_source)
            
            for url in nebula_urls:
                url = url.replace('&amp;', '&')
                if url not in [src[1] for src in video_sources]:
                    video_sources.append(('nebula_download', url))
                    print(f"    ✅ Found nebula.to URL: {url}")
            
            # Method 4: Look for any video URLs in the page
            print("  🔍 Method 4: Looking for any video URLs...")
            video_pattern = r'["\'](https?://[^"\']*\.(?:mp4|avi|mkv|mov|wmv|flv|webm))["\']'
            video_urls = re.findall(video_pattern, page_source)
            
            for url in video_urls:
                url = url.replace('&amp;', '&')
                if url not in [src[1] for src in video_sources]:
                    video_sources.append(('video_file', url))
                    print(f"    ✅ Found video file URL: {url}")
            
        except Exception as e:
            print(f"  ❌ Error finding video sources: {e}")
        
        return video_sources
    
    def try_download_button(self):
        """Try to click download button to get nebula.to URL"""
        print("🎯 Attempting to find and click download button...")
        
        try:
            # Look for various download button patterns
            download_selectors = [
                "//button[contains(text(), 'Download')]",
                "//a[contains(text(), 'Download')]",
                "//*[contains(@class, 'download')]",
                "//*[contains(@id, 'download')]",
                "//*[contains(@title, 'Download')]"
            ]
            
            for selector in download_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            print(f"    🔍 Found download element: {element.text or element.get_attribute('class')}")
                            # Note: We won't click it automatically to avoid unexpected behavior
                except:
                    continue
            
            return []
            
        except Exception as e:
            print(f"    ❌ Error with download button: {e}")
            return []
    
    def download_video(self, video_url, output_path):
        """Download video file"""
        try:
            print(f"📥 Downloading video from: {video_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://ww1.goojara.to/',
                'Accept': '*/*',
                'Accept-Encoding': 'identity',
                'Range': 'bytes=0-',
            }
            
            response = requests.get(video_url, stream=True, timeout=30, headers=headers)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '')
            print(f"  📋 Content-Type: {content_type}")
            
            # Get file size
            total_size = int(response.headers.get('content-length', 0))
            if total_size > 0:
                print(f"  📏 File Size: {total_size:,} bytes ({total_size / (1024*1024):.1f} MB)")
            
            with open(output_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Show progress
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r📊 Progress: {percent:.1f}% ({downloaded:,}/{total_size:,} bytes)", end='', flush=True)
                        else:
                            print(f"\r📊 Downloaded: {downloaded:,} bytes", end='', flush=True)
            
            print(f"\n✅ Download completed: {output_path}")
            
            # Check final file size
            final_size = os.path.getsize(output_path)
            print(f"📁 Final file size: {final_size:,} bytes ({final_size / (1024*1024):.1f} MB)")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error downloading video: {e}")
            return False
    
    def download_movie(self, movie_url, output_dir="downloads", custom_filename=None):
        """Main method to automatically download movie using Selenium"""
        print(f"🎬 Starting Selenium auto-download from: {movie_url}")
        print("=" * 80)
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Navigate to movie page
            if not self.navigate_to_movie_page(movie_url):
                return False
            
            # Find video sources
            video_sources = self.find_video_sources()
            
            if not video_sources:
                print("⚠️  No video sources found automatically")
                print("\n💡 Manual extraction still required:")
                print("   1. Right-click on the video player → Inspect Element")
                print("   2. Look for <video> tag with src attribute")
                print("   3. Copy the URL and use goojara_manual_downloader.py")
                return False
            
            print(f"\n🎯 Found {len(video_sources)} video source(s):")
            for i, (source_type, source) in enumerate(video_sources):
                print(f"  {i+1}. [{source_type}] {source}")
            
            # Try to download from available sources
            for i, (source_type, source) in enumerate(video_sources):
                print(f"\n🚀 Trying source {i+1} ({source_type}): {source}")
                
                # Generate filename
                if custom_filename:
                    # Use custom filename with source type and extension
                    filename = custom_filename
                    if '.' in source.split('/')[-1]:
                        ext = source.split('/')[-1].split('.')[-1]
                        if len(ext) <= 4 and ext.lower() in ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm']:
                            filename += f".{ext}"
                        else:
                            filename += ".mp4"
                    else:
                        filename += ".mp4"
                else:
                    # Fallback to original naming
                    timestamp = int(time.time())
                    filename = f"goojara_selenium_{timestamp}_{i+1}_{source_type}"
                    
                    # Try to determine file extension
                    if '.' in source.split('/')[-1]:
                        ext = source.split('/')[-1].split('.')[-1]
                        if len(ext) <= 4 and ext.lower() in ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm']:
                            filename += f".{ext}"
                        else:
                            filename += ".mp4"
                    else:
                        filename += ".mp4"
                
                output_path = os.path.join(output_dir, filename)
                
                if self.download_video(source, output_path):
                    print(f"🎉 Successfully downloaded: {output_path}")
                    return True
                else:
                    print(f"❌ Failed to download from source {i+1}")
            
            print("\n❌ All video sources failed")
            return False
            
        except Exception as e:
            print(f"❌ Error in download process: {e}")
            return False
        
        finally:
            # Automatically close the browser after finding the URL
            print("\n🌐 Closing browser automatically...")
            self.close()
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🎬 Goojara Selenium Auto Downloader")
        print("=" * 60)
        print("Usage: python goojara_selenium_auto_downloader.py <movie_url> [output_directory] [--headless]")
        print("Example: python goojara_selenium_auto_downloader.py https://ww1.goojara.to/myPg74")
        print("\nFeatures:")
        print("  - Uses Selenium to access rendered HTML")
        print("  - Automatically finds video URLs after JavaScript loads")
        print("  - Downloads videos directly")
        print("  - Falls back to manual extraction if needed")
        sys.exit(1)
    
    movie_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "downloads"
    headless = "--headless" in sys.argv
    
    if not movie_url.startswith('http'):
        print("❌ Error: Please provide a valid URL starting with http:// or https://")
        sys.exit(1)
    
    downloader = GoojaraSeleniumAutoDownloader(headless=headless)
    
    try:
        success = downloader.download_movie(movie_url, output_dir)
        
        if success:
            print("\n🎉 Movie download completed successfully!")
            print("📁 Check the 'downloads' folder for your movie file.")
        else:
            print("\n❌ Movie download failed.")
            print("\n🔧 Manual extraction methods:")
            print("   1. HTML Inspection: Right-click video → Inspect Element → Find <video> src")
            print("   2. Download Button: Hover over video → Click DOWNLOAD → Copy nebula.to URL")
            print("   3. More Options: Click ⋮ in video controls → Download")
        
        # Browser closes automatically after finding the URL
        print("\n🌐 Browser closed automatically")
        
    except KeyboardInterrupt:
        print("\n⏹️  Download interrupted by user")
    finally:
        downloader.close()

if __name__ == "__main__":
    main()
