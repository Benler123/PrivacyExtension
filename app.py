from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.params import Query
import fastapi
import urllib.parse
from typing import List
import uvicorn
import asyncio

from analyze_content import *
from parse_content import HTMLTextExtractor
from mongo_client import MongoConnector

app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_reader = MongoConnector()
text_extractor = HTMLTextExtractor()

@app.get("/url/{encoded_url:path}")
async def single_encoded(encoded_url: str):
    url = urllib.parse.unquote(encoded_url)
    results = await fetch_single_url(url)
    return results

@app.get("/urls/{encoded_urls:path}")
async def multiple_encoded(encoded_urls: str):
    decoded_string = urllib.parse.unquote(encoded_urls)
    decoded_urls = decoded_string.split("||")
    # Fetch all URLs concurrently
    results = await asyncio.gather(
        *[fetch_single_url(url) for url in decoded_urls]
    )
    combined_results = combine_analysis_dicts(results)
    return combined_results
    

@app.get("/")
def fetch_all():
    return mongo_reader.fetch_all()  

@app.get('/favicon.ico')
async def favicon():
    return FileResponse('static/favicon.ico')

async def fetch_single_url(url):
    mongo_data = mongo_reader.fetch_data(url)
    if(mongo_data):
        return mongo_data["analysis"]
    text, stats = text_extractor.process_url(url)
    text = ' '.join(text)
    analysis = generate_analysis(text)
    mongo_reader.insert_data(url, analysis)
    return analysis

def combine_analysis_dicts(results):
    if not results:
        return {}
        
    combined_dict = {
        "scores": {},
        "metadata": {
            "risk_percentage": 0,
            "risk_level": ""
        }
    }
    
    # Combine scores
    for result in results:
        if not result or "scores" not in result:
            continue
            
        for category, data in result["scores"].items():
            if category not in combined_dict["scores"]:
                combined_dict["scores"][category] = {
                    "quotes": [],
                    "score": 0
                }
            
            # Add unique quotes
            existing_quotes = set(combined_dict["scores"][category]["quotes"])
            for quote in data["quotes"]:
                if quote not in existing_quotes:
                    combined_dict["scores"][category]["quotes"].append(quote)
                    existing_quotes.add(quote)
            
            # Update score to be the average
            current_score = combined_dict["scores"][category]["score"]
            new_score = data["score"]
            if current_score == 0:
                combined_dict["scores"][category]["score"] = new_score
            else:
                combined_dict["scores"][category]["score"] = (current_score + new_score) / 2
    
    total_score = 0
    num_categories = len(combined_dict["scores"])
    
    if num_categories > 0:
        for category_data in combined_dict["scores"].values():
            total_score += category_data["score"]
        
        risk_percentage = round((1 - (total_score / (num_categories * 5))) * 100)
        if risk_percentage >= 70:
            risk_level = "Very High Risk"
        elif risk_percentage >= 50:
            risk_level = "High Risk"
        elif risk_percentage >= 30:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"
            
        combined_dict["metadata"] = {
            "risk_percentage": risk_percentage,
            "risk_level": risk_level
        }
    
    return combined_dict

    return combined

if __name__ == "__main__":
    uvicorn.run(app)