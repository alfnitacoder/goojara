#!/usr/bin/env python3
"""
Goojara Movie List Scraper
Scrapes all movie pages and stores unique movie links with titles
"""

import requests
import re
import os
import sys
import time
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib

class GoojaraMovieScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://ww1.goojara.to/',
        })
        self.base_url = "https://ww1.goojara.to"
        self.movies = {}  # Store unique movies by title and URL
        self.duplicate_count = 0
        self.total_found = 0
        
    def get_page_content(self, url):
        """Fetch page content with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"📡 Fetching page: {url}")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"❌ Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"❌ Failed to fetch {url} after {max_retries} attempts")
                    return None
    
    def extract_movie_info(self, movie_element):
        """Extract movie title and link from a movie element"""
        try:
            title = None
            link = None
            
            # Look for the link element first (this contains both title and link)
            link_elem = movie_element.find('a')
            if link_elem:
                # Get the link
                link = link_elem.get('href')
                if link and not link.startswith('http'):
                    link = urljoin(self.base_url, link)
                
                # Get the title from the span with class 'mtl' (movie title)
                title_span = link_elem.find('span', class_='mtl')
                if title_span:
                    title = title_span.get_text(strip=True)
                else:
                    # Fallback: get title from link text
                    title = link_elem.get_text(strip=True)
                
                # Also try to get title from the title attribute
                if not title:
                    title = link_elem.get('title', '')
            
            # Clean up the title
            if title:
                # Remove year if it's in parentheses at the end
                title = re.sub(r'\s*\(\d{4}\)\s*$', '', title)
                title = re.sub(r'\s+', ' ', title).strip()
            
            return title, link
            
        except Exception as e:
            print(f"⚠️  Error extracting movie info: {e}")
            return None, None
    
    def scrape_movies_from_page(self, html_content, page_url):
        """Extract all movies from a single page"""
        print(f"🔍 Scraping movies from page: {page_url}")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Common selectors for movie containers
        movie_selectors = [
            '.mxwd .dflex div',  # Main movie container structure
            '.mxwd div',         # Fallback to any div in mxwd
            '.dflex div',        # Direct dflex divs
            '.movie-item',
            '.movie',
            '.item',
            '.post',
            '.entry',
            '[class*="movie"]',
            '[class*="post"]',
            '[class*="item"]'
        ]
        
        movies_found = []
        
        for selector in movie_selectors:
            movie_elements = soup.select(selector)
            if movie_elements:
                print(f"  ✅ Found {len(movie_elements)} movies with selector: {selector}")
                break
        
        if not movie_elements:
            # Fallback: look for any div that might contain movie info
            movie_elements = soup.find_all('div', class_=re.compile(r'movie|post|item|entry', re.I))
            if movie_elements:
                print(f"  ✅ Found {len(movie_elements)} potential movie elements with fallback selector")
        
        if not movie_elements:
            # Last resort: look for any element with movie-like content
            movie_elements = soup.find_all(['div', 'article'], class_=True)
            movie_elements = [elem for elem in movie_elements if any(word in elem.get('class', []) for word in ['movie', 'post', 'item', 'entry'])]
            if movie_elements:
                print(f"  ✅ Found {len(movie_elements)} movie elements with broad search")
        
        for i, movie_elem in enumerate(movie_elements):
            title, link = self.extract_movie_info(movie_elem)
            
            if title and link:
                # Clean the title
                title = re.sub(r'\s+', ' ', title).strip()
                
                # Create a unique identifier for the movie
                movie_id = self.create_movie_id(title, link)
                
                if movie_id not in self.movies:
                    self.movies[movie_id] = {
                        'title': title,
                        'link': link,
                        'page_found': page_url,
                        'timestamp': time.time()
                    }
                    movies_found.append({
                        'title': title,
                        'link': link,
                        'id': movie_id
                    })
                    self.total_found += 1
                else:
                    self.duplicate_count += 1
                    print(f"    ⚠️  Duplicate found: {title}")
        
        print(f"  📊 Page summary: {len(movies_found)} new movies, {self.duplicate_count} duplicates so far")
        return movies_found
    
    def create_movie_id(self, title, link):
        """Create a unique identifier for a movie"""
        # Combine title and link to create a unique hash
        combined = f"{title.lower().strip()}|{link}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def find_next_page(self, html_content, current_page):
        """Find the next page URL"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Common pagination selectors
        pagination_selectors = [
            '#pgs',              # Main pagination container
            '.pagination',
            '.pager',
            '.nav-links',
            '[class*="pagination"]',
            '[class*="pager"]'
        ]
        
        next_page = None
        
        for selector in pagination_selectors:
            pagination = soup.select_one(selector)
            if pagination:
                # Look for next page link (specific to goojara structure)
                next_links = pagination.find_all('a', string=re.compile(r'next|>|»|Next', re.I))
                if next_links:
                    next_page = next_links[0].get('href')
                    break
                
                # Look for page numbers (specific to goojara structure)
                page_links = pagination.find_all('a', href=re.compile(r'p=\d+'))
                if page_links:
                    current_page_num = int(re.search(r'p=(\d+)', current_page).group(1))
                    for link in page_links:
                        href = link.get('href')
                        page_match = re.search(r'p=(\d+)', href)
                        if page_match:
                            page_num = int(page_match.group(1))
                            if page_num == current_page_num + 1:
                                next_page = href
                                break
                
                # If no next page found, look for the last page number to determine if we should continue
                if not next_page:
                    all_page_numbers = []
                    for link in page_links:
                        href = link.get('href')
                        page_match = re.search(r'p=(\d+)', href)
                        if page_match:
                            all_page_numbers.append(int(page_match.group(1)))
                    
                    if all_page_numbers:
                        max_page = max(all_page_numbers)
                        current_page_num = int(re.search(r'p=(\d+)', current_page).group(1))
                        if current_page_num < max_page:
                            # Construct next page URL
                            next_page = re.sub(r'p=\d+', f'p={current_page_num + 1}', current_page)
        
        if next_page and not next_page.startswith('http'):
            next_page = urljoin(self.base_url, next_page)
        
        return next_page
    
    def scrape_all_movies(self, start_url, max_pages=None):
        """Scrape movies from all pages"""
        print("🎬 Starting comprehensive movie scraping...")
        print("=" * 60)
        
        current_url = start_url
        page_count = 0
        
        while current_url and (max_pages is None or page_count < max_pages):
            page_count += 1
            print(f"\n📄 Processing page {page_count}: {current_url}")
            
            html_content = self.get_page_content(current_url)
            if not html_content:
                print(f"❌ Failed to get content from page {page_count}")
                break
            
            # Scrape movies from current page
            movies_found = self.scrape_movies_from_page(html_content, current_url)
            
            if movies_found:
                print(f"  🎯 Found {len(movies_found)} new movies on page {page_count}")
                for movie in movies_found[:5]:  # Show first 5 movies
                    print(f"    - {movie['title']}")
                if len(movies_found) > 5:
                    print(f"    ... and {len(movies_found) - 5} more")
            
            # Find next page
            next_page = self.find_next_page(html_content, current_url)
            if next_page:
                current_url = next_page
                print(f"  ➡️  Next page found: {next_page}")
                time.sleep(1)  # Be respectful to the server
            else:
                print(f"  🏁 No more pages found. Reached end of pagination.")
                break
        
        print(f"\n🎉 Scraping completed!")
        print(f"📊 Total pages processed: {page_count}")
        print(f"📊 Total unique movies found: {len(self.movies)}")
        print(f"📊 Total duplicates skipped: {self.duplicate_count}")
        
        return self.movies
    
    def save_to_temp_file(self, filename="goojara_movies_temp.txt"):
        """Save scraped movies to a temporary text file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Goojara Movies - Scraped Data\n")
                f.write("=" * 50 + "\n")
                f.write(f"Total unique movies: {len(self.movies)}\n")
                f.write(f"Scraped on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for movie_id, movie_data in self.movies.items():
                    f.write(f"Title: {movie_data['title']}\n")
                    f.write(f"Link: {movie_data['link']}\n")
                    f.write(f"Page found: {movie_data['page_found']}\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(movie_data['timestamp']))}\n")
                    f.write("-" * 40 + "\n\n")
            
            print(f"💾 Movies saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving to file: {e}")
            return None
    
    def save_to_json(self, filename="goojara_movies_temp.json"):
        """Save scraped movies to a JSON file"""
        try:
            data = {
                'metadata': {
                    'total_movies': len(self.movies),
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'base_url': self.base_url
                },
                'movies': self.movies
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Movies saved to JSON: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
            return None

def main():
    """Main function"""
    print("🎬 Goojara Movie List Scraper")
    print("=" * 40)
    
    # Default start URL
    start_url = "https://ww1.goojara.to/watch-movies?p=1"
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
    
    max_pages = None
    if len(sys.argv) > 2:
        try:
            max_pages = int(sys.argv[2])
        except ValueError:
            print("⚠️  Invalid max pages number, will scrape all available pages")
    
    if not start_url.startswith('http'):
        print("❌ Error: Please provide a valid URL starting with http:// or https://")
        sys.exit(1)
    
    # Create scraper and start scraping
    scraper = GoojaraMovieScraper()
    
    try:
        movies = scraper.scrape_all_movies(start_url, max_pages)
        
        if movies:
            # Save to both text and JSON formats
            txt_file = scraper.save_to_temp_file()
            json_file = scraper.save_to_json()
            
            print(f"\n🎉 Scraping completed successfully!")
            print(f"📁 Text file: {txt_file}")
            print(f"📁 JSON file: {json_file}")
            print(f"📊 Total unique movies: {len(movies)}")
            
            # Show some sample movies
            print(f"\n📋 Sample movies found:")
            for i, (movie_id, movie_data) in enumerate(list(movies.items())[:5]):
                print(f"  {i+1}. {movie_data['title']}")
                print(f"     Link: {movie_data['link']}")
            
        else:
            print("❌ No movies found during scraping")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        if scraper.movies:
            print(f"💾 Saving {len(scraper.movies)} movies found so far...")
            scraper.save_to_temp_file()
            scraper.save_to_json()
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        if scraper.movies:
            print(f"💾 Saving {len(scraper.movies)} movies found before error...")
            scraper.save_to_temp_file()
            scraper.save_to_json()

if __name__ == "__main__":
    main()
