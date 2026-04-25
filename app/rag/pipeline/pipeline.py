from app.rag.language.detector import detect_language
from app.rag.language.translator import translate_to_english, translate_from_english
from app.rag.components.retriever import retrieve_documents
from app.rag.components.generator import generate_answer
from app.services.evaluation_service import evaluate_response


SUPPORTED_LANGUAGES = ["en", "ru", "zh"]


def process_query(query: str):
    # =========================
    # 1. Detect language
    # =========================
    language = detect_language(query)

    if language not in SUPPORTED_LANGUAGES:
        language = "en"  # fallback

    # =========================
    # 2. Translate only if needed
    # =========================
    if language != "en":
        translated_query = translate_to_english(query)
    else:
        translated_query = query

    # =========================
    # 3. Retrieve documents
    # =========================
    docs = retrieve_documents(translated_query, "en", k=5)
    docs = [d for d in docs if d.strip()]

    # =========================
    # 4. Build context
    # =========================
    context = "\n\n---\n\n".join(docs)

    # =========================
    # 5. Generate answer
    # =========================
    context = "\n\n---\n\n".join(docs)
    answer_en = generate_answer(translated_query, context, "en")

    # =========================
    # 6. Translate back ONLY if needed
    # =========================
    if language != "en":
        final_answer = translate_from_english(answer_en, language)
    else:
        final_answer = answer_en

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
    # 9. Return structured output
    # =========================
    return {
        "query": query,
        "translated_query": translated_query,
        "language": language,
        "answer": final_answer,
        "confidence": confidence,
        "sources": docs,
        "evaluation": evaluation
    }