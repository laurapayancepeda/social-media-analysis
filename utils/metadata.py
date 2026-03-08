import spacy
from langdetect import detect, DetectorFactory
from geotext import GeoText

# deterministic language detection
DetectorFactory.seed = 0

# load spaCy model
nlp = spacy.load("en_core_web_sm")


def detect_language(text: str) -> str:
    """Detect language of text"""
    if not text or text.strip() == "":
        return ""
    try:
        return detect(text)
    except Exception:
        return "unknown"


def extract_entities(text: str, entity_type: str = None) -> list:
    """
    Extract named entities.
    Example entity types: ORG, PERSON, GPE
    """
    if not text or text.strip() == "":
        return []

    doc = nlp(text)

    if entity_type:
        return [ent.text for ent in doc.ents if ent.label_ == entity_type]

    return [ent.text for ent in doc.ents]


def detect_country(text: str) -> list:
    """Detect countries mentioned in text"""
    if not text or text.strip() == "":
        return []

    places = GeoText(text)
    countries = list(places.countries)

    doc = nlp(text)
    gpe_entities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    return list(set(countries + gpe_entities))
