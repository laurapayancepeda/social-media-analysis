from transformers import pipeline

# lazy loaded model
sentiment_model = None


def get_model():
    global sentiment_model

    if sentiment_model is None:
        sentiment_model = pipeline(
            "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment"
        )

    return sentiment_model


def sentiment_score(text: str) -> int:
    """
    Return sentiment score:
    +1 positive
    0 neutral
    -1 negative
    """
    if not text or text.strip() == "":
        return 0

    try:
        model = get_model()
        result = model(text[:512])[0]

        label = result["label"].lower()

        if "positive" in label:
            return 1
        elif "neutral" in label:
            return 0
        else:
            return -1

    except Exception:
        return 0
