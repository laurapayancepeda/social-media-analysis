from deep_translator import GoogleTranslator


def translate_text(text: str, target: str = "en") -> str:
    """Translate text to target language"""
    if not text or text.strip() == "":
        return ""

    try:
        return GoogleTranslator(source="auto", target=target).translate(text)

    except Exception:
        return text
