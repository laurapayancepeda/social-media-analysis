# utils/translator.py
from deep_translator import GoogleTranslator


def translate_text(text: str, target_lang: str = "en") -> str:
    if not text or text.strip() == "":
        return ""
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        return f"Translation error: {e}"
