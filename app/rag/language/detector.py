from langdetect import detect


def detect_language(text: str) -> str:
    try:
        lang = detect(text)

        if lang not in ["en", "ru", "zh"]:
            return "en"

        return lang
    except:
        return "en"