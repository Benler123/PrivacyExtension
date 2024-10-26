from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

MONGO_URI = "mongodb+srv://sunidhi:TRzCMl4WHp6CcTdT@privacy.kieyt.mongodb.net/?retryWrites=true&w=majority&appName=Privacy"

class MongoReader: 
    def __init__(self):
        self.client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        self.db = self.client["PrivacyExtensionDB"]
        self.collection = self.db["UrlToAnalysis"]

    def fetch_data(self, url):
        return self.collection.find_one({"url": url})
    
    def fetch_all(self):
        return list(self.collection.find({}))
    
    def insert_data(self, url, analysis):
        self.collection.insert_one({"url": url, "analysis": analysis})
       
if __name__ == "__main__":
    reader = MongoReader()
    data = reader.fetch_all()
    specific_data = reader.fetch_data("someurl.com")
