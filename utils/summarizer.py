# utils/summarizer.py
from transformers import pipeline

# Use the latest text2text model supported by Transformers
# distilbart-cnn-12-6 works with text2text-generation
summarizer_pipeline = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1,  # CPU, set 0 for GPU
)


def summarize_post(text: str) -> str:
    """
    Summarize text using BART model.
    """
    if not text or text.strip() == "":
        return ""
    try:
        summary_output = summarizer_pipeline(text, max_new_tokens=150)
        return summary_output[0]["summary_text"]
    except Exception as e:
        return f"Error summarizing text: {e}"
