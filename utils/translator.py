from deep_translator import GoogleTranslator


def translate_text(text, target="en"):
    try:
        return GoogleTranslator(source="auto", target=target).translate(text)
    except Exception as e:
        return f"Translation error: {e}"
