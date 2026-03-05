# utils/metadata.py
import spacy
from langdetect import detect, DetectorFactory
from geotext import GeoText

# Make langdetect deterministic
DetectorFactory.seed = 0

# Load spaCy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli

    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def detect_language(text: str) -> str:
    """Detect language of a text"""
    if not text or text.strip() == "":
        return ""
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection error: {e}")
        return "unknown"


def extract_entities(text: str, entity_type: str = None) -> list:
    """
    Extract named entities. Filter by entity_type if provided.
    Example entity_type: "ORG", "GPE", "PERSON"
    """
    if not text or text.strip() == "":
        return []
    doc = nlp(text)
    if entity_type:
        return [ent.text for ent in doc.ents if ent.label_ == entity_type]
    return [ent.text for ent in doc.ents]


def detect_country(text: str) -> list:
    """Detect countries mentioned in the text using GeoText + spaCy GPE"""
    if not text or text.strip() == "":
        return []
    places = GeoText(text)
    countries = list(places.countries)

    # Include GPE entities as additional country info
    doc = nlp(text)
    gpe_countries = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    return list(set(countries + gpe_countries))
