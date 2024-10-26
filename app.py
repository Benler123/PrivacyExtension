from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import fastapi
import urllib.parse
import uvicorn

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
def fetch_from_url(encoded_url: str):
    url = urllib.parse.unquote(encoded_url)
    print(url)
    mongo_data = mongo_reader.fetch_data(url)
    if(mongo_data):
        return mongo_data["analysis"]
    text, stats = text_extractor.process_url(url)
    text = ' '.join(text)
    analysis = generate_analysis(text)
    mongo_reader.insert_data(url, analysis)
    return analysis
    

@app.get("/")
def fetch_all():
    return mongo_reader.fetch_all()  

@app.get('/favicon.ico')
async def favicon():
    return FileResponse('static/favicon.ico')

if __name__ == "__main__":
    uvicorn.run(app)