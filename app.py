import fastapi
from fastapi.middleware.cors import CORSMiddleware
from analyze_content import *
from parse_content import HTMLTextExtractor
from mongo_client import MongoReader

app = fastapi.FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_reader = MongoReader()
text_extractor = HTMLTextExtractor()

@app.get("/{url}")
def fetch_from_url(url: str):
    mongo_data = mongo_reader.fetch_data(url)
    if(mongo_data):
        return mongo_data
    text, stats = text_extractor.process_url(url)
    text = ' '.join(text)
    analysis = generate_analysis(text)
    mongo_reader.insert_data(url, analysis)
    return text
    

@app.get("/")
def fetch_all():
    return MongoReader.fetch_all()  
    
