from bs4 import BeautifulSoup
import requests
import re
import pyperclip


class URLContentParser:
    def parse_html_content(url=None, html_content=None):
        """
        Parse HTML content either from a URL or direct HTML string.
        Returns a dictionary containing different types of content found.
        
        Args:
            url (str, optional): URL of the webpage to parse
            html_content (str, optional): Raw HTML content to parse
        
        Returns:
            dict: Dictionary containing parsed content
        """
        if not url and not html_content:
            raise ValueError("Either URL or HTML content must be provided")
        
        # Get HTML content
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                html_content = response.text
            except requests.RequestException as e:
                raise Exception(f"Error fetching URL: {e}")
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Initialize dictionary for parsed content
        parsed_content = {
            'title': None,
            'meta_description': None,
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': [],
            'lists': [],
            'tables': []
        }
        
        # Get title
        title_tag = soup.find('title')
        if title_tag:
            parsed_content['title'] = title_tag.string.strip()
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            parsed_content['meta_description'] = meta_desc.get('content', '').strip()
        
        # Get all headings (h1-h6)
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            for heading in headings:
                parsed_content['headings'].append({
                    'level': i,
                    'text': heading.get_text().strip()
                })
        
        # Get paragraphs
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text:  # Only add non-empty paragraphs
                parsed_content['paragraphs'].append(text)
        
        # Get links
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:  # Only add links with href attribute
                parsed_content['links'].append({
                    'text': link.get_text().strip(),
                    'href': href
                })
        
        # Get images
        for img in soup.find_all('img'):
            image_data = {
                'src': img.get('src'),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            }
            parsed_content['images'].append(image_data)
        
        # Get lists (both ordered and unordered)
        for list_tag in soup.find_all(['ul', 'ol']):
            list_items = []
            for item in list_tag.find_all('li'):
                list_items.append(item.get_text().strip())
            if list_items:  # Only add non-empty lists
                parsed_content['lists'].append({
                    'type': list_tag.name,
                    'items': list_items
                })
        
        # Get tables
        for table in soup.find_all('table'):
            table_data = []
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                row_data = [col.get_text().strip() for col in cols]
                if row_data:  # Only add non-empty rows
                    table_data.append(row_data)
            if table_data:  # Only add non-empty tables
                parsed_content['tables'].append(table_data)
        
        return parsed_content
