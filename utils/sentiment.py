# utils/sentiment.py
from transformers import pipeline
import streamlit as st


@st.cache_resource
def load_sentiment_model():
    """Load the sentiment analysis model once"""
    return pipeline(
        "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment"
    )


sentiment_model = load_sentiment_model()


def sentiment_score(text: str) -> int:
    """
    Return sentiment score: +1 positive, 0 neutral, -1 negative
    """
    if not text or text.strip() == "":
        return 0
    try:
        result = sentiment_model(text)[0]
        label = result["label"].lower()
        if "positive" in label:
            return 1
        elif "neutral" in label:
            return 0
        else:
            return -1
    except Exception as e:
        print(f"Sentiment error: {e}")
        return 0
