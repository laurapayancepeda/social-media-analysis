# utils/summarizer.py


def summarize_post(text: str) -> str:
    """
    Simple summarization: return first 200 characters with ellipsis
    """
    if not text.strip():
        return ""
    return text[:200] + ("..." if len(text) > 200 else "")
