import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from string import punctuation

class HTMLTextExtractor:
    def __init__(self):
        self.unwanted_tags = [
            'script', 'style', 'meta', 'link', 'noscript', 
            'header', 'footer', 'nav', '[document]'
        ]
    
    def fetch_html(self, url):
        """Fetch HTML content from URL"""
        try:
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                # noqa
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Dnt": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                # noqa
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None

    def clean_text(self, text):
        """Clean extracted text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove punctuation
        text = text.translate(str.maketrans('', '', punctuation))
        # Convert to lowercase
        return text.lower()
    
    def extract_words(self, html_content, min_word_length=2):
        """Extract words from HTML content"""
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted tags
        for tag in self.unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Get text content
        text = soup.get_text(separator=' ')
        
        # Clean text
        text = self.clean_text(text)
        
        # Split into words and filter
        words = [word for word in text.split() 
                if len(word) >= min_word_length 
                and not word.isnumeric()]
        
        return words
    
    def get_word_stats(self, words):
        """Get statistics about the words"""
        return {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'word_frequency': Counter(words).most_common(10)
        }
    
    def process_url(self, url, min_word_length=2, get_stats=True):
        """Process URL and return words and optionally stats"""
        html_content = self.fetch_html(url)
        if not html_content:
            return None
        
        words = self.extract_words(html_content, min_word_length)
        
        if get_stats:
            stats = self.get_word_stats(words)
            return words, stats
        return words
    
    def process_html(self, html_content, min_word_length=2, get_stats=True):
        """Process HTML content directly and return words and optionally stats"""
        words = self.extract_words(html_content, min_word_length)
        
        if get_stats:
            stats = self.get_word_stats(words)
            return words, stats
        return words

    