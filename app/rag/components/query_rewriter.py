def rewrite_query(query: str):
    query = query.strip()

    if len(query.split()) < 3:
        return f"Explain in detail: {query}"

    if "?" not in query:
        return f"{query} (provide a detailed explanation)"

    return query