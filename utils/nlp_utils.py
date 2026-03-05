import spacy
import country_converter as coco
import re

nlp = spacy.load("en_core_web_sm")


def extract_orgs(text):
    """Extract organization names from text using NER."""
    doc = nlp(text)
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    return orgs if orgs else ["Unknown"]


def detect_country(text):
    """Detect country names in text using country_converter."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            try:
                cc = coco.convert(names=ent.text, to="name_short")
                if cc != "not found":
                    return cc
            except:
                continue
    return "Unknown"
