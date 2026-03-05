from transformers import pipeline

# Use smaller model to avoid memory issues
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def summarize_post(text):
    if not text.strip():
        return ""
    try:
        result = summarizer(text, max_length=60, min_length=20, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        return f"Summarization error: {e}"
