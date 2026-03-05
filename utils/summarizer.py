# utils/summarizer.py
from transformers import pipeline

# Use text-generation pipeline for summarization
summarizer = pipeline(
    "summarization", model="sshleifer/distilbart-cnn-12-6", framework="tf"
)


def summarize_post(text: str, max_length: int = 60) -> str:
    """
    Summarize the input text using a text-generation model.
    """
    if not text or text.strip() == "":
        return ""
    try:
        summary = summarizer(
            text,
            max_new_tokens=max_length,
            do_sample=False,  # deterministic summary
        )
        # The model outputs a dict with 'generated_text'
        return summary[0]["generated_text"]
    except Exception as e:
        print(f"Summarization error: {e}")
        return text
