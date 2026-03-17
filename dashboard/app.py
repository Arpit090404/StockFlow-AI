import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/news"

st.set_page_config(page_title="AI Financial Insights", layout="wide")

st.title("AI Financial Insights Dashboard")

st.write("Real-time news analysis with stock recommendations")

try:
    response = requests.get(API_URL)
    data = response.json()

    for item in data:
        st.markdown("---")

        st.subheader(item["title"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Industry:", item["industry"])
            st.write("Sentiment:", item["sentiment"])

        with col2:
            st.write("Recommendation:", item["recommendation"])
            st.write("Confidence:", item["confidence"])

        with col3:
            st.write("Stocks:", ", ".join(item["stocks"]))

        st.write("Trend:")
        st.json(item["trend"])

        st.write("Reason:")
        st.info(item["reason"])

except Exception as e:
    st.error("Failed to fetch data. Make sure FastAPI server is running.")