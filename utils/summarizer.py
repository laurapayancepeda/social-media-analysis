import spacy

nlp = spacy.load("en_core_web_sm")


def summarize_post(text: str) -> str:
    """
    Simple summarization using first two sentences
    """
    if not text or text.strip() == "":
        return ""

    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    return " ".join(sentences[:2])
