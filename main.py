from parse_content import HTMLTextExtractor
from analyze_content import generate_analysis
from mongo_client import MongoConnector
import urllib.parse
import pyperclip 

if __name__ == "__main__":
    url = "https://press.hulu.com/privacy-policy/"
    mongo_reader = MongoConnector()
    text_extractor = HTMLTextExtractor()
    text, stats = text_extractor.process_url(url)
    text = ' '.join(text)
    analysis = generate_analysis(text)
    # mongo_reader.insert_data(url, analysis)