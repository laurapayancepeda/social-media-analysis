# utils/translator.py
from deep_translator import GoogleTranslator


def translate_text(text: str, target: str = "en") -> str:
    if not text or text.strip() == "":
        return ""
    try:
        return GoogleTranslator(source="auto", target=target).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text
