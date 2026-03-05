from deep_translator import GoogleTranslator


def translate_text(text, target_lang="en"):
    """
    Translate text to target language.
    """
    if not text or text.strip() == "":
        return ""
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text
