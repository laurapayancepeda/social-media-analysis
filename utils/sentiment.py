from transformers import pipeline

# Sentiment analysis
model = pipeline(
    "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment"
)


def sentiment_score(text):
    if not text or not text.strip():
        return 0
    try:
        result = model(text)[0]["label"]
        if "positive" in result.lower():
            return 1
        elif "negative" in result.lower():
            return -1
        else:
            return 0
    except Exception as e:
        return 0
