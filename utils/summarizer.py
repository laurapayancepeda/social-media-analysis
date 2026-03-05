# utils/summarizer.py
import spacy
from spacy.cli import download as spacy_download


def load_spacy_model():
    """
    Load SpaCy model, download automatically if not found.
    """
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        spacy_download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    return nlp


nlp = load_spacy_model()


def summarize_post(text: str) -> str:
    """
    Naive summarization: return the first 2 sentences.
    """
    if not text.strip():
        return ""
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return " ".join(sentences[:2])
