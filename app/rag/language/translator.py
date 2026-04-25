from deep_translator import GoogleTranslator


SUPPORTED_LANGUAGES = ["en", "ru", "zh"]


def translate_to_english(text: str) -> str:
    try:
        if len(text) < 3:
            return text
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception:
        return text


def translate_from_english(text: str, target_lang: str) -> str:
    try:
        if target_lang not in SUPPORTED_LANGUAGES:
            return text  # fallback

        return GoogleTranslator(source='en', target=target_lang).translate(text)

    except Exception as e:
        print(f"[TRANSLATION ERROR ← EN]: {e}")
        return text   # fallback