def detect_target_language(query: str, detected_language: str):
    q = query.lower()

    # explicit instructions
    if "in english" in q:
        return "en"
    if "in russian" in q or "на русском" in q:
        return "ru"
    if "in chinese" in q or "中文" in q:
        return "zh"

    # fallback
    return detected_language