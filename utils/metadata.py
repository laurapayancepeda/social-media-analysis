# utils/metadata.py
import langdetect
import spacy
from geotext import GeoText

# Load small English model (faster)
nlp = spacy.load("en_core_web_sm")


def detect_language(text: str) -> str:
    if not text or text.strip() == "":
        return ""
    try:
        return langdetect.detect(text)
    except:
        return "unknown"


def extract_entities(text: str) -> list:
    if not text or text.strip() == "":
        return []
    doc = nlp(text)
    return [ent.text for ent in doc.ents]


def detect_country(text: str) -> list:
    if not text or text.strip() == "":
        return []
    places = GeoText(text)
    countries = list(places.countries)
    return countries
