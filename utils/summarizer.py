# utils/summarizer.py
from transformers import pipeline

# Initialize summarization pipeline using text-generation
# Works with Streamlit Cloud / CPU
summarizer = pipeline(
    "text-generation",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1,  # Use CPU; change to 0 for GPU if available
    max_new_tokens=150,  # Max tokens in the summary
)


def summarize_post(text: str) -> str:
    """
    Summarize a given text using the BART model.
    Args:
        text (str): The text to summarize
    Returns:
        str: Generated summary
    """
    if not text or text.strip() == "":
        return ""

    try:
        # Run the pipeline
        summary_output = summarizer(text, max_new_tokens=150)
        summary_text = summary_output[0].get("generated_text", "")
        return summary_text
    except Exception as e:
        # In case something goes wrong
        return f"Error summarizing text: {e}"
