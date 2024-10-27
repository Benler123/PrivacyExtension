from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi

MONGO_URI = "mongodb+srv://sunidhi:TRzCMl4WHp6CcTdT@privacy.kieyt.mongodb.net/?retryWrites=true&w=majority&appName=Privacy"

class MongoConnector: 
    def __init__(self):
        self.client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        self.db = self.client["PrivacyExtensionDB"]
        self.collection = self.db["UrlToAnalysis"]

    def fetch_data(self, url):
        mongo_object = self.collection.find_one({"url": url})
        if mongo_object:
            mongo_object.pop("_id")
        return mongo_object
        # return self.collection.find_one({"url": url})
    
    def fetch_all(self):
        cursor = self.collection.find({})
        result = {doc["url"]: doc["analysis"] for doc in cursor}
        return result
    
    def insert_data(self, url, analysis):
        self.collection.insert_one({"url": url, "analysis": analysis})
       
if __name__ == "__main__":
    mongo_connector = MongoConnector()
    mongo_connector.insert_data("weinies.com", "This is a test")
