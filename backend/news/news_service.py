import requests
from textblob import TextBlob
from config import NEWS_API_KEY
from stocks.stock_service import get_stock_trend


# Industry keywords (expanded)
industry_keywords = {
    "technology": [
        "ai", "software", "tech", "it", "cloud", "semiconductor",
        "chip", "startup", "saas", "google", "microsoft", "apple"
    ],
    "banking": [
        "bank", "loan", "interest", "finance", "credit", "nbfc",
        "mortgage", "lending", "repo rate", "rbi"
    ],
    "energy": [
        "oil", "gas", "energy", "crude", "power", "electricity",
        "renewable", "solar", "wind"
    ],
    "crypto": [
        "bitcoin", "crypto", "blockchain", "ethereum", "token", "web3"
    ],
    "pharma": [
        "drug", "health", "pharma", "hospital", "medicine",
        "vaccine", "biotech"
    ],
    "auto": [
        "car", "vehicle", "auto", "ev", "electric vehicle",
        "automobile", "tesla"
    ],
    "fmcg": [
        "consumer", "fmcg", "retail", "food", "beverage",
        "packaged goods"
    ],
    "metal": [
        "steel", "metal", "mining", "aluminium", "copper",
        "iron", "ore"
    ]
}


# Industry to stocks (expanded)
industry_stocks = {
    "technology": [
        "TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS",
        "TECHM.NS", "LTIM.NS"
    ],
    "banking": [
        "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS",
        "AXISBANK.NS", "KOTAKBANK.NS"
    ],
    "energy": [
        "RELIANCE.NS", "ONGC.NS", "IOC.NS",
        "BPCL.NS", "GAIL.NS", "NTPC.NS"
    ],
    "pharma": [
        "SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS",
        "DIVISLAB.NS"
    ],
    "auto": [
        "TATAMOTORS.NS", "MARUTI.NS", "M&M.NS",
        "BAJAJ-AUTO.NS"
    ],
    "fmcg": [
        "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS",
        "BRITANNIA.NS"
    ],
    "metal": [
        "TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS",
        "VEDL.NS"
    ],
    "crypto": [
        "BTC-USD", "ETH-USD"
    ]
}


def fetch_news():
    url = f"https://newsapi.org/v2/everything?q=stock%20market&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])

    news_list = []
    for article in articles[:10]:
        news_list.append({
            "title": article["title"]
        })

    return news_list


def analyze_sentiment(text):
    if not text:
        return "neutral"

    score = TextBlob(text).sentiment.polarity

    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    return "neutral"


def detect_industry(text):
    if not text:
        return "other"

    text = text.lower()

    for industry, keywords in industry_keywords.items():
        for word in keywords:
            if word in text:
                return industry

    return "other"


def get_recommendation(sentiment, trend):
    if sentiment == "positive" and trend == "uptrend":
        return "STRONG BUY"
    elif sentiment == "positive":
        return "BUY"
    elif sentiment == "negative" and trend == "downtrend":
        return "STRONG SELL"
    elif sentiment == "negative":
        return "SELL"
    return "HOLD"


def get_confidence(sentiment, trend):
    score = 50

    if sentiment == "positive":
        score += 20
    elif sentiment == "negative":
        score += 20

    if trend == "uptrend":
        score += 20
    elif trend == "downtrend":
        score += 20

    return min(score, 100)


def get_reason(sentiment, trend, industry):
    return f"{sentiment.capitalize()} sentiment and {trend} observed in {industry} sector"


def get_news_analysis():
    news = fetch_news()
    result = []

    for item in news:
        title = item["title"]

        sentiment = analyze_sentiment(title)
        industry = detect_industry(title)

        stocks = industry_stocks.get(industry, [])

        stock_trends = {}
        trend = "unknown"

        for stock in stocks[:2]:
            t = get_stock_trend(stock)
            stock_trends[stock] = t

        if len(stock_trends) > 0:
            trend = list(stock_trends.values())[0]

        recommendation = get_recommendation(sentiment, trend)
        confidence = get_confidence(sentiment, trend)
        reason = get_reason(sentiment, trend, industry)

        result.append({
            "title": title,
            "sentiment": sentiment,
            "industry": industry,
            "stocks": stocks[:3],
            "trend": stock_trends,
            "recommendation": recommendation,
            "confidence": confidence,
            "reason": reason
        })

    return result