# utils/summarizer.py
from transformers import pipeline

# Use latest transformers-compatible pipeline
summarizer = pipeline(
    "text2text-generation",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1,  # Use CPU, set 0 if using GPU
)


def summarize_post(text, max_new_tokens=150):
    """
    Summarize a given text.
    Returns the summarized string.
    """
    if not text or text.strip() == "":
        return ""
    result = summarizer(text, max_new_tokens=max_new_tokens)
    return result[0]["generated_text"]
