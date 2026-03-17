import yfinance as yf

def get_stock_trend(ticker):
    print("Function called for:", ticker)

    try:
        data = yf.download(ticker, period="1mo", interval="1d")
        print("Data fetched")

        if data is None or data.shape[0] == 0:
            print("No data")
            return "unknown"

        close_prices = data["Close"]

        if hasattr(close_prices, "columns"):
            close_prices = close_prices.iloc[:, 0]

        short_ma = close_prices.rolling(window=5).mean()
        long_ma = close_prices.rolling(window=20).mean()

        short_val = short_ma.iloc[-1]
        long_val = long_ma.iloc[-1]

        print("Short MA:", short_val)
        print("Long MA:", long_val)

        if short_val > long_val:
            return "uptrend"
        else:
            return "downtrend"

    except Exception as e:
        print("ERROR:", e)
        return "unknown"


# ✅ TEST BLOCK (IMPORTANT)
if __name__ == "__main__":
    print("Running test...")

    trend = get_stock_trend("TCS.NS")
    print("Final Trend:", trend)