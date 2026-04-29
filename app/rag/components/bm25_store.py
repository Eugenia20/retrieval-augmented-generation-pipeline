from rank_bm25 import BM25Okapi

bm25 = None
tokenized_corpus = []


def build_bm25(documents: list[dict]):
    global bm25, tokenized_corpus

    texts = [doc["text"] for doc in documents]

    tokenized_corpus = [t.lower().split() for t in texts]

    bm25 = BM25Okapi(tokenized_corpus)


def search_bm25(query: str, documents: list[dict], k: int = 5):
    global bm25, tokenized_corpus

    if bm25 is None:
        return []

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked[:k]]