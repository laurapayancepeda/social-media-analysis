# utils/metadata.py
from langdetect import detect, DetectorFactory
from geotext import GeoText

# Make langdetect deterministic
DetectorFactory.seed = 0


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
    Removed spaCy NER — always returns empty list
    """
    return []


def detect_country(text: str) -> list:
    """Detect countries mentioned in the text using GeoText"""
    if not text or text.strip() == "":
        return []
    places = GeoText(text)
    return list(places.countries)
