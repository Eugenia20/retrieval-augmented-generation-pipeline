from app.rag.language.detector import detect_language
from app.rag.language.translator import translate_to_english, translate_from_english
from app.rag.components.retriever import retrieve_documents
from app.rag.components.generator import generate_answer
from app.services.evaluation_service import evaluate_response
from app.rag.language.language_controller import detect_target_language
from app.rag.components.reranker import rerank
from app.core.cache import get_from_cache, save_to_cache
from app.rag.components.query_rewriter import rewrite_query

SUPPORTED_LANGUAGES = ["en", "ru", "zh"]


async def process_query(query: str, user_department: str):

    # =========================
    # 0. CACHE CHECK
    # =========================
    cached = get_from_cache(query)
    if cached:
        return cached

    # =========================
    # 1. Detect language
    # =========================
    detected_language = detect_language(query)

    if detected_language not in SUPPORTED_LANGUAGES:
        detected_language = "en"

    target_language = detect_target_language(query, detected_language)

    # =========================
    # 2. Translate
    # =========================
    translated_query = (
        translate_to_english(query)
        if detected_language != "en"
        else query
    )

    translated_query = rewrite_query(translated_query)

    # =========================
    # 3. Retrieve + Rerank
    # =========================
    candidates = retrieve_documents(
        translated_query,
        "en",
        user_department,
        k=10
    )

    docs = rerank(translated_query, candidates, top_k=5)

    # 🔥 strict filter
    docs = [d for d in docs if d["score"] > 0.4]

    if not docs:
        result = {
            "query": query,
            "answer": "I don't have enough information",
            "confidence": 0,
            "sources": [],
            "evaluation": {}
        }

        save_to_cache(query, result)
        return result

    # =========================
    # 4. Build context
    # =========================
    texts = [d["text"] for d in docs]
    context = "\n\n---\n\n".join(texts)

    # =========================
    # 5. Generate answer (ASYNC)
    # =========================
    answer_en = await generate_answer(translated_query, context, target_language)

    # =========================
    # 6. Translate back
    # =========================
    final_answer = (
        translate_from_english(answer_en, target_language)
        if target_language != "en"
        else answer_en
    )

    # =========================
    # 7. Confidence
    # =========================
    confidence = min(1.0, len(docs) / 5)

    # =========================
    # 8. Evaluation
    # =========================
    evaluation = evaluate_response(
        query=translated_query,
        response=answer_en,
        docs=docs
    )

    # =========================
    # 9. Final result
    # =========================
    result = {
        "query": query,
        "translated_query": translated_query,
        "detected_language": detected_language,
        "target_language": target_language,
        "answer": final_answer,
        "confidence": confidence,
        "sources": docs,
        "evaluation": evaluation
    }

    # =========================
    # SAVE TO CACHE
    # =========================
    save_to_cache(query, result)

    return result