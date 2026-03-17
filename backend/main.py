from fastapi import FastAPI
from news.news_service import get_news_analysis

app = FastAPI(title="AI Financial Insights API")

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test")
def test():
    return {"msg": "Backend working perfectly"}

@app.get("/news")
def news():
    return get_news_analysis()